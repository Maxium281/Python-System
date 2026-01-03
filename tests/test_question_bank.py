# -*- coding: utf-8 -*-
from app.core.question_bank import QuestionBank

def test_get_question_by_id(db_manager):
    qb = QuestionBank(db_manager)
    q = qb.get_question_by_id(1)
    assert q['id'] == 1
    assert 'correct_answer' in q
    assert q['correct_answer'] == 'A'

def test_get_questions_by_category(db_manager):
    qb = QuestionBank(db_manager)
    res = qb.get_questions_by_category('Python Basics')
    assert isinstance(res, dict)
    questions = res.get('questions', [])
    assert any(item['category'] == 'Python Basics' for item in questions)

def test_search_question(db_manager):
    qb = QuestionBank(db_manager)
    results = qb.search_question('print')
    assert isinstance(results, list)
    assert any('print' in item['title'].lower() for item in results)
