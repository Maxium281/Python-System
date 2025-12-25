# -*- coding: utf-8 -*-
from app.database.db_manager import DBManager
from app.utils.logger import Logger

logger = Logger()

class QuestionBank:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        self.category_list = ['Python Basics', 'Flask Framework', 'Project Experience', 'Data Structure', 'Algorithm', 'Database']

    def get_question_by_id(self, question_id: int) -> dict:
        try:
            sql_q = "SELECT * FROM questions WHERE id = ?"
            q = self.db_manager.query(sql_q, (question_id,)).fetchone()
            if not q:
                logger.error(f"Question ID {question_id} not found")
                return {}
            sql_a = "SELECT * FROM answers WHERE question_id = ?"
            a = self.db_manager.query(sql_a, (question_id,)).fetchone()
            
            res = {
                'id': q['id'],
                'category': q['category'],
                'title': q['title'],
                'option_a': q['option_a'],
                'option_b': q['option_b'],
                'option_c': q['option_c'],
                'option_d': q['option_d'],
                'difficulty': q['difficulty'],
                'is_high_frequency': q['is_high_frequency'],
                'correct_answer': a['correct_answer'] if a else '',
                'analysis': a['analysis'] if a else '',
                'knowledge_point': a['knowledge_point'] if a else ''
            }
            logger.info(f"Successfully retrieved question ID {question_id}")
            return res
        except Exception as e:
            logger.error(f"Failed to retrieve question: {e}")
            return {}

    def get_questions_by_category(self, category: str, page: int = 1, page_size: int = 20) -> list:
        try:
            offset = (page - 1) * page_size
            sql = "SELECT * FROM questions WHERE category = ? LIMIT ? OFFSET ?"
            rows = self.db_manager.query(sql, (category, page_size, offset)).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to retrieve questions by category: {e}")
            return []

    def search_question(self, keyword: str) -> list:
        try:
            sql = "SELECT * FROM questions WHERE title LIKE ?"
            rows = self.db_manager.query(sql, (f'%{keyword}%',)).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to search questions: {e}")
            return []

    def get_category_list(self) -> list:
        return self.category_list
