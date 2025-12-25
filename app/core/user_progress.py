# -*- coding: utf-8 -*-
import time
from app.database.db_manager import DBManager
from app.utils.logger import Logger

logger = Logger()

class UserProgress:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        self.user_id = 1

    def save_answer(self, question_id: int, user_answer: str) -> bool:
        try:
            from app.core.question_bank import QuestionBank
            qb = QuestionBank(self.db_manager)
            q = qb.get_question_by_id(question_id)
            is_correct = 1 if user_answer == q.get('correct_answer', '') else 0
            sql = "INSERT INTO user_records (question_id, user_answer, is_correct, answer_time, exam_id) VALUES (?, ?, ?, ?, ?)"
            self.db_manager.execute(sql, (question_id, user_answer, is_correct, time.strftime('%Y-%m-%d %H:%M:%S'), 0))
            self.db_manager.commit()
            logger.info(f"Saved answer: {question_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save answer: {e}")
            self.db_manager.rollback()
            return False

    def get_progress(self) -> dict:
        try:
            total = self.db_manager.query("SELECT COUNT(*) as total FROM user_records").fetchone()['total'] or 0
            correct = self.db_manager.query("SELECT COUNT(*) as correct FROM user_records WHERE is_correct = 1").fetchone()['correct'] or 0
            accuracy = round(correct / total, 2) if total > 0 else 0
            rows = self.db_manager.query("""
                SELECT q.category, COUNT(*) as count
                FROM user_records ur
                JOIN questions q ON ur.question_id = q.id
                GROUP BY q.category
            """).fetchall()
            category_count = {r['category']: r['count'] for r in rows}
            return {'total': total, 'correct': correct, 'accuracy': accuracy, 'category_count': category_count}
        except Exception as e:
            logger.error(f"Failed to get progress: {e}")
            return {}

    def get_error_questions(self) -> list:
        try:
            sql = """
                SELECT DISTINCT q.*, a.correct_answer, a.analysis
                FROM user_records ur
                JOIN questions q ON ur.question_id = q.id
                JOIN answers a ON q.id = a.question_id
                WHERE ur.is_correct = 0
            """
            rows = self.db_manager.query(sql).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to get error questions: {e}")
            return []

    def add_favorite(self, question_id: int) -> bool:
        try:
            if self.db_manager.query("SELECT 1 FROM favorite WHERE question_id = ?", (question_id,)).fetchone():
                return False
            self.db_manager.execute("INSERT INTO favorite (question_id, collect_time) VALUES (?, ?)", (question_id, time.strftime('%Y-%m-%d %H:%M:%S')))
            self.db_manager.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add favorite: {e}")
            self.db_manager.rollback()
            return False

    def remove_favorite(self, question_id: int) -> bool:
        try:
            if not self.db_manager.query("SELECT 1 FROM favorite WHERE question_id = ?", (question_id,)).fetchone():
                return False
            self.db_manager.execute("DELETE FROM favorite WHERE question_id = ?", (question_id,))
            self.db_manager.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to remove favorite: {e}")
            self.db_manager.rollback()
            return False

    def get_favorite(self) -> list:
        try:
            sql = """
                SELECT q.*, a.correct_answer, a.analysis
                FROM favorite f
                JOIN questions q ON f.question_id = q.id
                JOIN answers a ON q.id = a.question_id
                ORDER BY f.collect_time DESC
            """
            rows = self.db_manager.query(sql).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to get favorites: {e}")
            return []
