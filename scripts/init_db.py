#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3

def get_db_path():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_dir = os.path.join(base_dir, 'database')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'interview.db')

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        difficulty INTEGER DEFAULT 1,
        is_high_frequency INTEGER DEFAULT 0
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        correct_answer TEXT,
        analysis TEXT,
        knowledge_point TEXT,
        FOREIGN KEY(question_id) REFERENCES questions(id)
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS user_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        user_answer TEXT,
        is_correct INTEGER,
        answer_time TEXT,
        exam_id INTEGER
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS favorite (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        collect_time TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_path = get_db_path()
    init_db(db_path)
    print(f"Initialized database at: {db_path}")
