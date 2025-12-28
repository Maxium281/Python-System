# -*- coding: utf-8 -*-
"""
面试模拟器模块
提供智能出题、考试管理、评分系统等功能
"""
import random
import time
from typing import List, Dict, Optional, Any
from datetime import datetime
from collections import defaultdict
from app.core.question_bank import QuestionBank
from app.database.db_manager import DBManager
from app.utils.logger import Logger

logger = Logger()


class InterviewSimulator:
    """面试模拟器类"""
    
    DIFFICULTY_WEIGHTS = {'Easy': 0.2, 'Medium': 0.5, 'Hard': 0.3}
    CATEGORY_WEIGHTS = {
        'Python Basics': 0.3, 'Flask Framework': 0.25, 'Data Structure': 0.2,
        'Algorithm': 0.15, 'Database': 0.1
    }
    
    def __init__(self, question_bank: QuestionBank, db_manager: DBManager,
                 question_count: int = 20, time_limit: int = 30 * 60, user_id: int = 1):
        """初始化面试模拟器"""
        self.question_bank = question_bank
        self.db_manager = db_manager
        self.user_id = user_id
        self.exam_id = int(time.time())
        self.question_count = question_count
        self.time_limit = time_limit
        self.start_time = 0
        self.end_time = 0
        self.question_list = []
        self.user_answers = {}
    
    def generate_exam(self, category: Optional[str] = None,
                     difficulty: Optional[str] = None,
                     adaptive: bool = True) -> List[Dict[str, Any]]:
        """生成考试题目"""
        try:
            if adaptive and not category and not difficulty:
                questions = self._generate_adaptive_exam()
            elif category:
                questions = self._generate_by_category(category, difficulty)
            else:
                questions = self._generate_random_exam(difficulty)
            
            if len(questions) < self.question_count:
                self.question_list = questions
                logger.warning(f"可用题目数量({len(questions)})少于请求数量({self.question_count})")
            else:
                self.question_list = random.sample(questions, self.question_count)
            
            random.shuffle(self.question_list)
            
            logger.info(f"生成考试，题目数量: {len(self.question_list)}, 考试ID: {self.exam_id}")
            return self.question_list
        except Exception as e:
            logger.error(f"生成考试失败: {e}")
            return []

    def _generate_adaptive_exam(self) -> List[Dict[str, Any]]:
        """生成自适应难度考试"""
        try:
            from app.core.user_progress import UserProgress
            user_progress = UserProgress(self.db_manager, self.user_id)
            progress = user_progress.get_progress()
            
            accuracy = progress.get('accuracy', 50)
            
            if accuracy >= 80:
                difficulty_dist = {'Easy': 0.1, 'Medium': 0.4, 'Hard': 0.5}
            elif accuracy >= 60:
                difficulty_dist = {'Easy': 0.2, 'Medium': 0.5, 'Hard': 0.3}
            else:
                difficulty_dist = {'Easy': 0.4, 'Medium': 0.5, 'Hard': 0.1}
            
            all_questions = []
            for diff, ratio in difficulty_dist.items():
                count = int(self.question_count * ratio)
                if count > 0:
                    questions = self.question_bank.get_questions_by_difficulty(diff, limit=count * 3)
                    all_questions.extend(questions)
            
            if len(all_questions) < self.question_count:
                high_freq = self.question_bank.get_high_frequency_questions(
                    count=self.question_count - len(all_questions)
                )
                all_questions.extend(high_freq)
            
            return all_questions
        except Exception as e:
            logger.error(f"生成自适应考试失败: {e}")
            return self._generate_random_exam()
    
    def _generate_by_category(self, category: str, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """按分类生成题目"""
        result = self.question_bank.get_questions_by_category(
            category, page=1, page_size=self.question_count * 2, difficulty=difficulty
        )
        return result.get('questions', [])
    
    def _generate_random_exam(self, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """随机生成题目"""
        questions = []
        categories = self.question_bank.get_category_list()
        
        for category in categories:
            weight = self.CATEGORY_WEIGHTS.get(category, 0.1)
            count = int(self.question_count * weight)
            if count > 0:
                cat_questions = self.question_bank.get_questions_by_category(
                    category, page=1, page_size=count * 2, difficulty=difficulty
                )
                questions.extend(cat_questions.get('questions', []))
        
        return questions if questions else self.question_bank.get_random_questions(
            count=self.question_count * 2, difficulty=difficulty
        )
    
    def start_exam(self):
        """开始考试"""
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_limit
        self.user_answers = {}
        logger.info(f"考试开始，ID: {self.exam_id}, 时间限制: {self.time_limit}秒")

    def end_exam(self):
        """结束考试"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        logger.info(f"考试结束，ID: {self.exam_id}, 耗时: {duration:.2f}秒")
    
    def get_remaining_time(self) -> int:
        """获取剩余时间（秒）"""
        if self.end_time == 0:
            return self.time_limit
        
        remaining = int(self.end_time - time.time())
        return max(0, remaining)
    
    def is_time_up(self) -> bool:
        """检查是否时间到"""
        return self.get_remaining_time() == 0
    
    def submit_answer(self, question_id: int, user_answer: str):
        """提交答案"""
        self.user_answers[question_id] = {
            'answer': user_answer,
            'submit_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        logger.debug(f"提交答案: 题目ID={question_id}, 答案={user_answer}")
    
    def save_exam_record(self, user_answers: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """保存考试记录并返回评分结果"""
        try:
            if user_answers is None:
                user_answers = [
                    {'question_id': qid, 'user_answer': ans['answer']}
                    for qid, ans in self.user_answers.items()
                ]
            
            correct_count = 0
            total_count = len(user_answers)
            category_stats = defaultdict(lambda: {'total': 0, 'correct': 0})
            difficulty_stats = defaultdict(lambda: {'total': 0, 'correct': 0})
            
            answer_records = []
            
            for ans in user_answers:
                qid = ans['question_id']
                uans = ans.get('user_answer', '')
                q = self.question_bank.get_question_by_id(qid, include_answer=True)
                
                if not q:
                    continue
                
                correct_answer = q.get('correct_answer', '')
                is_correct = 1 if uans == correct_answer else 0
                
                if is_correct:
                    correct_count += 1
                
                category = q.get('category', 'Unknown')
                difficulty = q.get('difficulty', 'Easy')
                category_stats[category]['total'] += 1
                category_stats[category]['correct'] += is_correct
                difficulty_stats[difficulty]['total'] += 1
                difficulty_stats[difficulty]['correct'] += is_correct
                
                answer_time = ans.get('answer_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                answer_records.append((qid, uans, is_correct, answer_time, self.exam_id, self.user_id))
            
            if answer_records:
                sql = """INSERT INTO user_records 
                         (question_id, user_answer, is_correct, answer_time, exam_id, user_id)
                         VALUES (?, ?, ?, ?, ?, ?)"""
                self.db_manager.executemany(sql, answer_records)
            self.db_manager.commit()
            
            score = round(correct_count / total_count * 100, 2) if total_count > 0 else 0.0
            duration = self.end_time - self.start_time if self.end_time > 0 else 0
            
            result = {
                'exam_id': self.exam_id,
                'total_questions': total_count,
                'correct_count': correct_count,
                'wrong_count': total_count - correct_count,
                'score': score,
                'duration': round(duration, 2),
                'start_time': datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': datetime.fromtimestamp(self.end_time).strftime('%Y-%m-%d %H:%M:%S') if self.end_time > 0 else None,
                'category_stats': dict(category_stats),
                'difficulty_stats': dict(difficulty_stats),
                'grade': self._calculate_grade(score)
            }
            
            logger.info(f"考试记录已保存，ID: {self.exam_id}, 得分: {score}分")
            return result
        except Exception as e:
            logger.error(f"保存考试记录失败: {e}")
            self.db_manager.rollback()
            return {}
    
    def _calculate_grade(self, score: float) -> str:
        """计算等级"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_exam_report(self, exam_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成考试报告"""
        try:
            report = {
                'summary': {
                    'exam_id': exam_result.get('exam_id'),
                    'score': exam_result.get('score'),
                    'grade': exam_result.get('grade'),
                    'total_questions': exam_result.get('total_questions'),
                    'correct_count': exam_result.get('correct_count'),
                    'wrong_count': exam_result.get('wrong_count'),
                    'duration': exam_result.get('duration'),
                    'start_time': exam_result.get('start_time'),
                    'end_time': exam_result.get('end_time')
                },
                'category_analysis': {},
                'difficulty_analysis': {},
                'recommendations': []
            }
            
            category_stats = exam_result.get('category_stats', {})
            for category, stats in category_stats.items():
                accuracy = round(stats['correct'] / stats['total'] * 100, 2) if stats['total'] > 0 else 0.0
                report['category_analysis'][category] = {
                    'total': stats['total'],
                    'correct': stats['correct'],
                    'accuracy': accuracy
                }
            
            difficulty_stats = exam_result.get('difficulty_stats', {})
            for difficulty, stats in difficulty_stats.items():
                accuracy = round(stats['correct'] / stats['total'] * 100, 2) if stats['total'] > 0 else 0.0
                report['difficulty_analysis'][difficulty] = {
                    'total': stats['total'],
                    'correct': stats['correct'],
                    'accuracy': accuracy
                }
            
            score = exam_result.get('score', 0)
            if score < 60:
                report['recommendations'].append('建议加强基础知识学习')
                report['recommendations'].append('多做简单难度的题目')
            elif score < 80:
                report['recommendations'].append('继续巩固已掌握的知识点')
                report['recommendations'].append('适当增加中等难度题目练习')
            else:
                report['recommendations'].append('可以挑战更高难度的题目')
                report['recommendations'].append('建议关注薄弱分类的深入学习')
            
            weak_categories = [
                cat for cat, stats in category_stats.items()
                if stats['total'] > 0 and stats['correct'] / stats['total'] < 0.6
            ]
            if weak_categories:
                report['recommendations'].append(f'建议重点复习以下分类: {", ".join(weak_categories)}')
            
            return report
        except Exception as e:
            logger.error(f"生成考试报告失败: {e}")
            return {}
    
    def get_wrong_questions(self, exam_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取考试中的错题"""
        try:
            wrong_questions = []
            for q in self.question_list:
                qid = q.get('id')
                user_answer = self.user_answers.get(qid, {}).get('answer', '')
                question_detail = self.question_bank.get_question_by_id(qid, include_answer=True)
                
                if question_detail:
                    correct_answer = question_detail.get('correct_answer', '')
                    if user_answer != correct_answer:
                        wrong_questions.append({
                            'question': question_detail,
                            'user_answer': user_answer,
                            'correct_answer': correct_answer
                        })
            
            return wrong_questions
        except Exception as e:
            logger.error(f"获取错题失败: {e}")
            return []
    
    def reset_exam(self):
        """重置考试状态"""
        self.exam_id = int(time.time())
        self.start_time = 0
        self.end_time = 0
        self.question_list = []
        self.user_answers = {}
        logger.info("考试状态已重置")
    
    def get_exam_info(self) -> Dict[str, Any]:
        """获取当前考试信息"""
        return {
            'exam_id': self.exam_id,
            'question_count': len(self.question_list),
            'total_questions': self.question_count,
            'time_limit': self.time_limit,
            'remaining_time': self.get_remaining_time(),
            'started': self.start_time > 0,
            'ended': self.end_time > 0,
            'answered_count': len(self.user_answers)
        }
