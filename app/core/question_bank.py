# -*- coding: utf-8 -*-
"""
??????
????????????????
"""
import random
from typing import List, Dict, Optional, Any
from datetime import datetime
from app.database.db_manager import DBManager
from app.utils.logger import Logger

logger = Logger()


class QuestionBank:
    """?????"""
    
    DEFAULT_CATEGORIES = [
        'Python Basics', 'Flask Framework', 'Project Experience',
        'Data Structure', 'Algorithm', 'Database', 'Web Development',
        'API Design', 'Testing', 'Security', 'Performance', 'Best Practices'
    ]
    
    DIFFICULTY_LEVELS = {'Easy': 1, 'Medium': 2, 'Hard': 3, 'Expert': 4}
    
    def __init__(self, db_manager: DBManager):
        """????????"""
        self.db_manager = db_manager
        self.category_list = self.DEFAULT_CATEGORIES.copy()
        self._load_categories_from_db()
    
    def _load_categories_from_db(self):
        """?????????????"""
        try:
            sql = "SELECT DISTINCT category FROM questions WHERE category IS NOT NULL"
            results = self.db_manager.fetchall(sql)
            db_categories = [r['category'] for r in results]
            all_categories = list(set(self.category_list + db_categories))
            self.category_list = sorted(all_categories)
            logger.info(f"???{len(self.category_list)}???")
        except Exception as e:
            logger.warning(f"?????????????????: {e}")
    
    def get_question_by_id(self, question_id: int, include_answer: bool = True) -> Dict[str, Any]:
        """??ID??????"""
        try:
            sql_q = "SELECT * FROM questions WHERE id = ?"
            q = self.db_manager.fetchone(sql_q, (question_id,))
            
            if not q:
                logger.warning(f"??ID {question_id} ???")
                return {}
            
            result = {
                'id': q['id'],
                'category': q.get('category', ''),
                'title': q.get('title', ''),
                'option_a': q.get('option_a', ''),
                'option_b': q.get('option_b', ''),
                'option_c': q.get('option_c', ''),
                'option_d': q.get('option_d', ''),
                'difficulty': q.get('difficulty', 'Easy'),
                'is_high_frequency': bool(q.get('is_high_frequency', 0)),
                'create_time': q.get('create_time', ''),
                'update_time': q.get('update_time', '')
            }
            
            if include_answer:
                sql_a = "SELECT * FROM answers WHERE question_id = ?"
                a = self.db_manager.fetchone(sql_a, (question_id,))
                if a:
                    result.update({
                        'correct_answer': a.get('correct_answer', ''),
                        'analysis': a.get('analysis', ''),
                        'knowledge_point': a.get('knowledge_point', ''),
                        'reference': a.get('reference', '')
                    })
                else:
                    result.update({
                        'correct_answer': '', 'analysis': '', 'knowledge_point': '', 'reference': ''
                    })
            
            return result
        except Exception as e:
            logger.error(f"??????: {e}")
            return {}
    
    def get_questions_by_category(self, category: str, page: int = 1, 
                                   page_size: int = 20, difficulty: Optional[str] = None,
                                   high_frequency_only: bool = False) -> Dict[str, Any]:
        """??????????????????"""
        try:
            conditions = ["category = ?"]
            params = [category]
            
            if difficulty:
                conditions.append("difficulty = ?")
                params.append(difficulty)
            
            if high_frequency_only:
                conditions.append("is_high_frequency = 1")
            
            where_clause = " AND ".join(conditions)
            
            count_sql = f"SELECT COUNT(*) as total FROM questions WHERE {where_clause}"
            total_result = self.db_manager.fetchone(count_sql, tuple(params))
            total = total_result['total'] if total_result else 0
            
            offset = (page - 1) * page_size
            sql = f"SELECT * FROM questions WHERE {where_clause} ORDER BY id DESC LIMIT ? OFFSET ?"
            params.extend([page_size, offset])
            
            questions = self.db_manager.fetchall(sql, tuple(params))
            
            return {
                'questions': questions,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size if total > 0 else 0
            }
        except Exception as e:
            logger.error(f"?????????: {e}")
            return {'questions': [], 'total': 0, 'page': page, 'page_size': page_size, 'total_pages': 0}
    
    def search_question(self, keyword: str, category: Optional[str] = None,
                        difficulty: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """???????????"""
        try:
            conditions = ["(title LIKE ? OR option_a LIKE ? OR option_b LIKE ? OR option_c LIKE ? OR option_d LIKE ?)"]
            search_pattern = f'%{keyword}%'
            params = [search_pattern] * 5
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            if difficulty:
                conditions.append("difficulty = ?")
                params.append(difficulty)
            
            where_clause = " AND ".join(conditions)
            sql = f"SELECT * FROM questions WHERE {where_clause} LIMIT ?"
            params.append(limit)
            
            results = self.db_manager.fetchall(sql, tuple(params))
            logger.info(f"???{len(results)}???????: {keyword}")
            return results
        except Exception as e:
            logger.error(f"??????: {e}")
            return []
    
    def get_category_list(self) -> List[str]:
        """????????"""
        return self.category_list.copy()
    
    def get_category_stats(self) -> Dict[str, Dict[str, int]]:
        """??????????"""
        try:
            stats = {}
            for category in self.category_list:
                total = self.db_manager.get_count('questions', 'category = ?', (category,))
                easy = self.db_manager.get_count('questions', 'category = ? AND difficulty = ?', (category, 'Easy'))
                medium = self.db_manager.get_count('questions', 'category = ? AND difficulty = ?', (category, 'Medium'))
                hard = self.db_manager.get_count('questions', 'category = ? AND difficulty = ?', (category, 'Hard'))
                
                stats[category] = {'total': total, 'easy': easy, 'medium': medium, 'hard': hard}
            return stats
        except Exception as e:
            logger.error(f"????????: {e}")
            return {}
    
    def get_random_questions(self, count: int = 10, category: Optional[str] = None,
                             difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """??????"""
        try:
            conditions = []
            params = []
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            if difficulty:
                conditions.append("difficulty = ?")
                params.append(difficulty)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            sql = f"SELECT id FROM questions WHERE {where_clause}"
            all_ids = self.db_manager.fetchall(sql, tuple(params))
            
            if not all_ids:
                return []
            
            selected_ids = random.sample([r['id'] for r in all_ids], min(count, len(all_ids)))
            
            questions = []
            for qid in selected_ids:
                q = self.get_question_by_id(qid, include_answer=False)
                if q:
                    questions.append(q)
            
            logger.info(f"?????{len(questions)}???")
            return questions
        except Exception as e:
            logger.error(f"????????: {e}")
            return []
    
    def get_high_frequency_questions(self, count: int = 20, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """??????"""
        try:
            conditions = ["is_high_frequency = 1"]
            params = []
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            where_clause = " AND ".join(conditions)
            sql = f"SELECT * FROM questions WHERE {where_clause} ORDER BY id DESC LIMIT ?"
            params.append(count)
            
            questions = self.db_manager.fetchall(sql, tuple(params))
            logger.info(f"???{len(questions)}?????")
            return questions
        except Exception as e:
            logger.error(f"????????: {e}")
            return []
    
    def get_questions_by_difficulty(self, difficulty: str, limit: int = 50) -> List[Dict[str, Any]]:
        """???????"""
        try:
            sql = "SELECT * FROM questions WHERE difficulty = ? LIMIT ?"
            questions = self.db_manager.fetchall(sql, (difficulty, limit))
            return questions
        except Exception as e:
            logger.error(f"?????????: {e}")
            return []
    
    def add_question(self, question_data: Dict[str, Any]) -> Optional[int]:
        """?????"""
        try:
            sql = """INSERT INTO questions 
                     (category, title, option_a, option_b, option_c, option_d, 
                      difficulty, is_high_frequency, create_time, update_time)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = (
                question_data.get('category', ''),
                question_data.get('title', ''),
                question_data.get('option_a', ''),
                question_data.get('option_b', ''),
                question_data.get('option_c', ''),
                question_data.get('option_d', ''),
                question_data.get('difficulty', 'Easy'),
                int(question_data.get('is_high_frequency', False)),
                now, now
            )
            
            cursor = self.db_manager.execute(sql, params)
            question_id = cursor.lastrowid
            
            if 'correct_answer' in question_data:
                self.add_answer(question_id, question_data)
            
            self.db_manager.commit()
            logger.info(f"???????ID: {question_id}")
            return question_id
        except Exception as e:
            logger.error(f"??????: {e}")
            self.db_manager.rollback()
            return None
    
    def add_answer(self, question_id: int, answer_data: Dict[str, Any]):
        """?????????"""
        try:
            existing = self.db_manager.fetchone(
                "SELECT id FROM answers WHERE question_id = ?", (question_id,)
            )
            
            if existing:
                sql = """UPDATE answers SET 
                         correct_answer = ?, analysis = ?, knowledge_point = ?, reference = ?
                         WHERE question_id = ?"""
                params = (
                    answer_data.get('correct_answer', ''),
                    answer_data.get('analysis', ''),
                    answer_data.get('knowledge_point', ''),
                    answer_data.get('reference', ''),
                    question_id
                )
            else:
                sql = """INSERT INTO answers 
                         (question_id, correct_answer, analysis, knowledge_point, reference)
                         VALUES (?, ?, ?, ?, ?)"""
                params = (
                    question_id,
                    answer_data.get('correct_answer', ''),
                    answer_data.get('analysis', ''),
                    answer_data.get('knowledge_point', ''),
                    answer_data.get('reference', '')
                )
            
            self.db_manager.execute(sql, params)
            self.db_manager.commit()
            logger.info(f"?????????ID: {question_id}")
        except Exception as e:
            logger.error(f"??????: {e}")
            self.db_manager.rollback()
    
    def update_question(self, question_id: int, question_data: Dict[str, Any]) -> bool:
        """??????"""
        try:
            update_fields = []
            params = []
            
            for field in ['category', 'title', 'option_a', 'option_b', 'option_c', 
                         'option_d', 'difficulty', 'is_high_frequency']:
                if field in question_data:
                    update_fields.append(f"{field} = ?")
                    params.append(question_data[field])
            
            if not update_fields:
                return False
            
            update_fields.append("update_time = ?")
            params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            params.append(question_id)
            
            sql = f"UPDATE questions SET {', '.join(update_fields)} WHERE id = ?"
            self.db_manager.execute(sql, tuple(params))
            self.db_manager.commit()
            
            if any(key in question_data for key in ['correct_answer', 'analysis', 'knowledge_point']):
                self.add_answer(question_id, question_data)
            
            logger.info(f"???????ID: {question_id}")
            return True
        except Exception as e:
            logger.error(f"??????: {e}")
            self.db_manager.rollback()
            return False
    
    def delete_question(self, question_id: int) -> bool:
        """????"""
        try:
            with self.db_manager.transaction():
                self.db_manager.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))
                self.db_manager.execute("DELETE FROM questions WHERE id = ?", (question_id,))
            
            logger.info(f"???????ID: {question_id}")
            return True
        except Exception as e:
            logger.error(f"??????: {e}")
            return False
    
    def get_total_count(self) -> int:
        """??????"""
        return self.db_manager.get_count('questions')
    
    def get_questions_by_ids(self, question_ids: List[int]) -> List[Dict[str, Any]]:
        """??ID????????"""
        if not question_ids:
            return []
        
        try:
            placeholders = ','.join(['?'] * len(question_ids))
            sql = f"SELECT * FROM questions WHERE id IN ({placeholders})"
            questions = self.db_manager.fetchall(sql, tuple(question_ids))
            return questions
        except Exception as e:
            logger.error(f"????????: {e}")
            return []
