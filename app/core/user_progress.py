# -*- coding: utf-8 -*-
"""
用户进度管理模块
提供用户学习进度跟踪、统计、错题管理、收藏管理等功能
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from app.database.db_manager import DBManager
from app.utils.logger import Logger

logger = Logger()


class UserProgress:
    """用户进度管理类"""
    
    def __init__(self, db_manager: DBManager, user_id: int = 1):
        """初始化用户进度管理器"""
        self.db_manager = db_manager
        self.user_id = user_id
    
    def save_answer(self, question_id: int, user_answer: str, exam_id: int = 0,
                    answer_time: Optional[str] = None) -> bool:
        """保存用户答题记录"""
        try:
            from app.core.question_bank import QuestionBank
            qb = QuestionBank(self.db_manager)
            q = qb.get_question_by_id(question_id)
            
            if not q:
                logger.warning(f"题目ID {question_id} 不存在")
                return False
            
            correct_answer = q.get('correct_answer', '')
            is_correct = 1 if user_answer == correct_answer else 0
            
            if answer_time is None:
                answer_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            sql = """INSERT INTO user_records 
                     (question_id, user_answer, is_correct, answer_time, exam_id, user_id)
                     VALUES (?, ?, ?, ?, ?, ?)"""
            
            self.db_manager.execute(sql, (
                question_id, user_answer, is_correct, answer_time, exam_id, self.user_id
            ))
            self.db_manager.commit()
            
            logger.info(f"保存答题记录: 题目ID={question_id}, 正确={bool(is_correct)}")
            return True
        except Exception as e:
            logger.error(f"保存答题记录失败: {e}")
            self.db_manager.rollback()
            return False

    def get_progress(self) -> Dict[str, Any]:
        """获取用户学习进度统计"""
        try:
            # 基础统计
            total_sql = "SELECT COUNT(*) as total FROM user_records WHERE user_id = ?"
            total_result = self.db_manager.fetchone(total_sql, (self.user_id,))
            total = total_result['total'] if total_result else 0
            
            correct_sql = "SELECT COUNT(*) as correct FROM user_records WHERE user_id = ? AND is_correct = 1"
            correct_result = self.db_manager.fetchone(correct_sql, (self.user_id,))
            correct = correct_result['correct'] if correct_result else 0
            
            accuracy = round(correct / total * 100, 2) if total > 0 else 0.0
            
            # 分类统计
            category_sql = """
                SELECT q.category, 
                       COUNT(*) as count,
                       SUM(CASE WHEN ur.is_correct = 1 THEN 1 ELSE 0 END) as correct_count
                FROM user_records ur
                JOIN questions q ON ur.question_id = q.id
                WHERE ur.user_id = ?
                GROUP BY q.category
            """
            category_rows = self.db_manager.fetchall(category_sql, (self.user_id,))
            category_stats = {}
            for row in category_rows:
                category_stats[row['category']] = {
                    'total': row['count'],
                    'correct': row['correct_count'],
                    'accuracy': round(row['correct_count'] / row['count'] * 100, 2) if row['count'] > 0 else 0.0
                }
            
            # 难度统计
            difficulty_sql = """
                SELECT q.difficulty,
                       COUNT(*) as count,
                       SUM(CASE WHEN ur.is_correct = 1 THEN 1 ELSE 0 END) as correct_count
                FROM user_records ur
                JOIN questions q ON ur.question_id = q.id
                WHERE ur.user_id = ?
                GROUP BY q.difficulty
            """
            difficulty_rows = self.db_manager.fetchall(difficulty_sql, (self.user_id,))
            difficulty_stats = {}
            for row in difficulty_rows:
                difficulty_stats[row['difficulty']] = {
                    'total': row['count'],
                    'correct': row['correct_count'],
                    'accuracy': round(row['correct_count'] / row['count'] * 100, 2) if row['count'] > 0 else 0.0
                }
            
            # 最近7天统计
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
            recent_sql = """
                SELECT COUNT(*) as count,
                       SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_count
                FROM user_records
                WHERE user_id = ? AND answer_time >= ?
            """
            recent_result = self.db_manager.fetchone(recent_sql, (self.user_id, seven_days_ago))
            recent_total = recent_result['count'] if recent_result else 0
            recent_correct = recent_result['correct_count'] if recent_result else 0
            recent_accuracy = round(recent_correct / recent_total * 100, 2) if recent_total > 0 else 0.0
            
            # 考试次数
            exam_count_sql = "SELECT COUNT(DISTINCT exam_id) as count FROM user_records WHERE user_id = ? AND exam_id > 0"
            exam_count_result = self.db_manager.fetchone(exam_count_sql, (self.user_id,))
            exam_count = exam_count_result['count'] if exam_count_result else 0
            
            return {
                'total': total,
                'correct': correct,
                'wrong': total - correct,
                'accuracy': accuracy,
                'category_stats': category_stats,
                'difficulty_stats': difficulty_stats,
                'recent_7_days': {
                    'total': recent_total,
                    'correct': recent_correct,
                    'accuracy': recent_accuracy
                },
                'exam_count': exam_count,
                'favorite_count': len(self.get_favorite()),
                'error_count': len(self.get_error_questions())
            }
        except Exception as e:
            logger.error(f"获取学习进度失败: {e}")
            return {
                'total': 0, 'correct': 0, 'wrong': 0, 'accuracy': 0.0,
                'category_stats': {}, 'difficulty_stats': {},
                'recent_7_days': {'total': 0, 'correct': 0, 'accuracy': 0.0},
                'exam_count': 0, 'favorite_count': 0, 'error_count': 0
            }
    
    def get_error_questions(self, category: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取错题列表"""
        try:
            conditions = ["ur.user_id = ?", "ur.is_correct = 0"]
            params = [self.user_id]
            
            if category:
                conditions.append("q.category = ?")
                params.append(category)
            
            where_clause = " AND ".join(conditions)
            sql = f"""
                SELECT DISTINCT q.*, a.correct_answer, a.analysis, a.knowledge_point,
                       ur.user_answer, ur.answer_time, COUNT(*) as error_count
                FROM user_records ur
                JOIN questions q ON ur.question_id = q.id
                LEFT JOIN answers a ON q.id = a.question_id
                WHERE {where_clause}
                GROUP BY q.id
                ORDER BY error_count DESC, ur.answer_time DESC
                LIMIT ?
            """
            params.append(limit)
            
            rows = self.db_manager.fetchall(sql, tuple(params))
            return rows
        except Exception as e:
            logger.error(f"获取错题列表失败: {e}")
            return []

    def add_favorite(self, question_id: int) -> bool:
        """添加收藏"""
        try:
            existing = self.db_manager.fetchone(
                "SELECT id FROM favorite WHERE question_id = ? AND user_id = ?",
                (question_id, self.user_id)
            )
            
            if existing:
                logger.warning(f"题目ID {question_id} 已收藏")
                return False
            
            collect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "INSERT INTO favorite (question_id, user_id, collect_time) VALUES (?, ?, ?)"
            self.db_manager.execute(sql, (question_id, self.user_id, collect_time))
            self.db_manager.commit()
            
            logger.info(f"添加收藏: 题目ID={question_id}")
            return True
        except Exception as e:
            logger.error(f"添加收藏失败: {e}")
            self.db_manager.rollback()
            return False

    def remove_favorite(self, question_id: int) -> bool:
        """取消收藏"""
        try:
            existing = self.db_manager.fetchone(
                "SELECT id FROM favorite WHERE question_id = ? AND user_id = ?",
                (question_id, self.user_id)
            )
            
            if not existing:
                logger.warning(f"题目ID {question_id} 未收藏")
                return False
            
            sql = "DELETE FROM favorite WHERE question_id = ? AND user_id = ?"
            self.db_manager.execute(sql, (question_id, self.user_id))
            self.db_manager.commit()
            
            logger.info(f"取消收藏: 题目ID={question_id}")
            return True
        except Exception as e:
            logger.error(f"取消收藏失败: {e}")
            self.db_manager.rollback()
            return False

    def is_favorite(self, question_id: int) -> bool:
        """检查题目是否已收藏"""
        try:
            result = self.db_manager.fetchone(
                "SELECT 1 FROM favorite WHERE question_id = ? AND user_id = ?",
                (question_id, self.user_id)
            )
            return result is not None
        except Exception as e:
            logger.error(f"检查收藏状态失败: {e}")
            return False
    
    def get_favorite(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取收藏列表"""
        try:
            sql = """
                SELECT q.*, a.correct_answer, a.analysis, a.knowledge_point,
                       f.collect_time
                FROM favorite f
                JOIN questions q ON f.question_id = q.id
                LEFT JOIN answers a ON q.id = a.question_id
                WHERE f.user_id = ?
                ORDER BY f.collect_time DESC
                LIMIT ?
            """
            rows = self.db_manager.fetchall(sql, (self.user_id, limit))
            return rows
        except Exception as e:
            logger.error(f"获取收藏列表失败: {e}")
            return []
    
    def get_learning_trend(self, days: int = 30) -> List[Dict[str, Any]]:
        """获取学习趋势数据"""
        try:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            sql = """
                SELECT DATE(answer_time) as date,
                       COUNT(*) as total,
                       SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
                FROM user_records
                WHERE user_id = ? AND answer_time >= ?
                GROUP BY DATE(answer_time)
                ORDER BY date ASC
            """
            rows = self.db_manager.fetchall(sql, (self.user_id, start_date))
            
            trend_data = []
            for row in rows:
                trend_data.append({
                    'date': row['date'],
                    'total': row['total'],
                    'correct': row['correct'],
                    'accuracy': round(row['correct'] / row['total'] * 100, 2) if row['total'] > 0 else 0.0
                })
            
            return trend_data
        except Exception as e:
            logger.error(f"获取学习趋势失败: {e}")
            return []
    
    def get_streak_days(self) -> int:
        """获取连续学习天数"""
        try:
            sql = """
                SELECT DISTINCT DATE(answer_time) as date
                FROM user_records
                WHERE user_id = ?
                ORDER BY date DESC
            """
            rows = self.db_manager.fetchall(sql, (self.user_id,))
            
            if not rows:
                return 0
            
            streak = 0
            current_date = datetime.now().date()
            
            for row in rows:
                record_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                expected_date = current_date - timedelta(days=streak)
                
                if record_date == expected_date:
                    streak += 1
                elif record_date < expected_date:
                    break
            
            return streak
        except Exception as e:
            logger.error(f"获取连续学习天数失败: {e}")
            return 0
    
    def get_achievements(self) -> Dict[str, Any]:
        """获取用户成就"""
        try:
            progress = self.get_progress()
            achievements = {
                'total_answered': progress['total'],
                'total_correct': progress['correct'],
                'accuracy': progress['accuracy'],
                'streak_days': self.get_streak_days(),
                'exam_count': progress['exam_count'],
                'favorite_count': progress['favorite_count'],
                'error_count': progress['error_count'],
                'level': self._calculate_level(progress['total']),
                'badges': self._get_badges(progress)
            }
            return achievements
        except Exception as e:
            logger.error(f"获取成就信息失败: {e}")
            return {}
    
    def _calculate_level(self, total_answered: int) -> int:
        """计算用户等级"""
        if total_answered < 10:
            return 1
        elif total_answered < 50:
            return 2
        elif total_answered < 100:
            return 3
        elif total_answered < 200:
            return 4
        elif total_answered < 500:
            return 5
        elif total_answered < 1000:
            return 6
        else:
            return 7
    
    def _get_badges(self, progress: Dict[str, Any]) -> List[str]:
        """获取用户徽章"""
        badges = []
        total = progress.get('total', 0)
        accuracy = progress.get('accuracy', 0)
        streak = self.get_streak_days()
        exam_count = progress.get('exam_count', 0)
        
        if total >= 100:
            badges.append('百题达人')
        if total >= 500:
            badges.append('五百题大师')
        if total >= 1000:
            badges.append('千题之王')
        
        if accuracy >= 90:
            badges.append('准确率高手')
        if accuracy >= 95:
            badges.append('准确率大师')
        
        if streak >= 7:
            badges.append('一周坚持')
        if streak >= 30:
            badges.append('月度坚持')
        
        if exam_count >= 10:
            badges.append('考试达人')
        
        return badges
    
    def get_exam_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取考试历史记录"""
        try:
            sql = """
                SELECT exam_id,
                       COUNT(*) as total_questions,
                       SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_count,
                       MIN(answer_time) as start_time,
                       MAX(answer_time) as end_time
                FROM user_records
                WHERE user_id = ? AND exam_id > 0
                GROUP BY exam_id
                ORDER BY start_time DESC
                LIMIT ?
            """
            rows = self.db_manager.fetchall(sql, (self.user_id, limit))
            
            exam_history = []
            for row in rows:
                total = row['total_questions']
                correct = row['correct_count']
                exam_history.append({
                    'exam_id': row['exam_id'],
                    'total_questions': total,
                    'correct_count': correct,
                    'wrong_count': total - correct,
                    'accuracy': round(correct / total * 100, 2) if total > 0 else 0.0,
                    'start_time': row['start_time'],
                    'end_time': row['end_time']
                })
            
            return exam_history
        except Exception as e:
            logger.error(f"获取考试历史失败: {e}")
            return []
