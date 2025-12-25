# -*- coding: utf-8 -*-
from app.core.interview_simulator import InterviewSimulator
from app.core.question_bank import QuestionBank

def test_generate_and_save_exam(db_manager):
    qb = QuestionBank(db_manager)
    sim = InterviewSimulator(qb, db_manager)
    questions = sim.generate_exam(category='Python Basics')
    assert isinstance(questions, list)
    sim.start_exam()
    sim.end_exam()
    user_answers = []
    for q in questions:
        user_answers.append({'question_id': q['id'], 'user_answer': q.get('correct_answer', '') or 'A'})
    sim.save_exam_record(user_answers)
    row = db_manager.query("SELECT COUNT(*) as cnt FROM user_records WHERE exam_id = ?;", (sim.exam_id,)).fetchone()
    assert row['cnt'] == len(user_answers)
