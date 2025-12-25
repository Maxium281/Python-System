# -*- coding: utf-8 -*-
from app.core.user_progress import UserProgress
from app.core.question_bank import QuestionBank

def test_save_answer_and_progress(db_manager):
    up = UserProgress(db_manager)
    qb = QuestionBank(db_manager)
    ok = up.save_answer(1, 'A')
    assert ok is True
    ok2 = up.save_answer(2, 'B')
    assert ok2 is True
    progress = up.get_progress()
    assert progress['total'] >= 2
    assert 'accuracy' in progress

def test_error_and_favorite(db_manager):
    up = UserProgress(db_manager)
    up.save_answer(2, 'B')
    errors = up.get_error_questions()
    assert isinstance(errors, list)
    added = up.add_favorite(1)
    assert added is True
    favs = up.get_favorite()
    assert any(f['id'] == 1 for f in favs)
    removed = up.remove_favorite(1)
    assert removed is True
