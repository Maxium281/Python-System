# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import sqlite3
import pytest

# 将项目根目录加入模块搜索路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.database.db_manager import DBManager

@pytest.fixture(scope='session')
def tmp_db_path():
    tmpdir = tempfile.TemporaryDirectory(prefix='interview_test_')
    db_path = os.path.join(tmpdir.name, 'interview_test.db')
    conn = sqlite3.connect(db_path)
    conn.close()
    yield db_path
    try:
        tmpdir.cleanup()
    except Exception:
        pass

@pytest.fixture(scope='session')
def db_manager(tmp_db_path):
    dbm = DBManager(db_path=tmp_db_path)
    yield dbm
    dbm.close()

@pytest.fixture(scope='function', autouse=True)
def populate_db(db_manager):
    schema_sql = """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        difficulty TEXT,
        is_high_frequency INTEGER
    );
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        correct_answer TEXT,
        analysis TEXT,
        knowledge_point TEXT
    );
    CREATE TABLE IF NOT EXISTS user_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        user_answer TEXT,
        is_correct INTEGER,
        answer_time TIMESTAMP,
        exam_id INTEGER
    );
    CREATE TABLE IF NOT EXISTS favorite (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        collect_time TIMESTAMP
    );
    """
    cur = db_manager.conn.cursor()
    cur.executescript("DROP TABLE IF EXISTS user_records; DROP TABLE IF EXISTS favorite; DROP TABLE IF EXISTS answers; DROP TABLE IF EXISTS questions;")
    cur.executescript(schema_sql)
    
    sample_questions = [
        ('Python Basics', 'What is print function?', 'Output content', 'Input content', 'Format string', 'Create variable', 'Easy', 1),
        ('Flask Framework', 'How to define route?', 'app.route', 'flask.route', 'route.define', 'app.add_url', 'Medium', 0)
    ]
    cur.executemany(
        "INSERT INTO questions (category, title, option_a, option_b, option_c, option_d, difficulty, is_high_frequency) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        sample_questions
    )
    
    sample_answers = [
        (1, 'A', 'Output to console', 'Output'),
        (2, 'A', 'Use decorator app.route', 'Route definition')
    ]
    cur.executemany(
        "INSERT INTO answers (question_id, correct_answer, analysis, knowledge_point) VALUES (?, ?, ?, ?);",
        sample_answers
    )
    db_manager.commit()
    yield
    
    cur.executescript("DELETE FROM user_records; DELETE FROM favorite;")
    db_manager.commit()
