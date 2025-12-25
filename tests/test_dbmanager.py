# -*- coding: utf-8 -*-

def test_dbmanager_execute_and_query(db_manager):
    cur = db_manager.execute("INSERT INTO user_records (question_id, user_answer, is_correct, answer_time, exam_id) VALUES (?, ?, ?, datetime('now'), ?);", (1, 'A', 1, 0))
    db_manager.commit()
    row = db_manager.query("SELECT COUNT(*) as cnt FROM user_records WHERE question_id = ?;", (1,)).fetchone()
    assert row['cnt'] >= 1

def test_dbmanager_rollback(db_manager):
    db_manager.execute("INSERT INTO user_records (question_id, user_answer, is_correct, answer_time, exam_id) VALUES (?, ?, ?, datetime('now'), ?);", (2, 'B', 0, 0))
    db_manager.rollback()
    row = db_manager.query("SELECT COUNT(*) as cnt FROM user_records WHERE question_id = ?;", (2,)).fetchone()
    assert row['cnt'] == 0
