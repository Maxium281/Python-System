# -*- coding: utf-8 -*-
import random
import time
from app.core.question_bank import QuestionBank
from app.database.db_manager import DBManager
from app.utils.logger import Logger

logger = Logger()

class InterviewSimulator:
    def __init__(self, question_bank: QuestionBank, db_manager: DBManager):
        self.question_bank = question_bank
        self.db_manager = db_manager
        self.exam_id = int(time.time())
        self.question_count = 20
        self.time_limit = 30 * 60
        self.start_time = 0
        self.end_time = 0
        self.question_list = []

    def generate_exam(self, category: str = None) -> list:
        try:
            if category:
                questions = self.question_bank.get_questions_by_category(category)
            else:
                category = random.choice(self.question_bank.get_category_list())
                questions = self.question_bank.get_questions_by_category(category)
            if len(questions) < self.question_count:
                self.question_list = questions
            else:
                self.question_list = random.sample(questions, self.question_count)
            logger.info(f"Generated exam with {len(self.question_list)} questions")
            return self.question_list
        except Exception as e:
            logger.error(f"Failed to generate exam: {e}")
            return []

    def start_exam(self):
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_limit
        logger.info(f"Exam started, ID: {self.exam_id}")

    def end_exam(self):
        self.end_time = time.time()
        logger.info(f"Exam ended, ID: {self.exam_id}, Time: {self.end_time - self.start_time:.2f}s")

    def save_exam_record(self, user_answers: list):
        try:
            for ans in user_answers:
                qid = ans['question_id']
                uans = ans['user_answer']
                q = self.question_bank.get_question_by_id(qid)
                is_corr = 1 if uans == q.get('correct_answer', '') else 0
                sql = "INSERT INTO user_records (question_id, user_answer, is_correct, answer_time, exam_id) VALUES (?, ?, ?, ?, ?)"
                self.db_manager.execute(sql, (qid, uans, is_corr, time.strftime('%Y-%m-%d %H:%M:%S'), self.exam_id))
            self.db_manager.commit()
            logger.info(f"Exam record saved, ID: {self.exam_id}")
        except Exception as e:
            logger.error(f"Failed to save exam record: {e}")
            self.db_manager.rollback()
