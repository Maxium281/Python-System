# -*- coding: utf-8 -*-
"""
题库初始化脚本
生成样例题目并初始化 SQLite 数据库
"""
import os
import json
import random
import sqlite3
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
JSON_PATH = os.path.join(DATA_DIR, 'initial_questions.json')
DB_PATH = os.path.join(DATA_DIR, 'questions.db')

CATEGORIES = ['Python Basics', 'Flask Framework', 'Data Structure', 'Algorithm', 'Database']
DIFFICULTIES = ['Easy', 'Medium', 'Hard']
SAMPLE_TITLES = [
    "下列关于{topic}的说法中，哪一项是正确的？",
    "{topic} 的时间复杂度通常为多少？",
    "请指出下面代码的输出：\n\n{snippet}",
    "关于 {topic}，以下哪个选项是最佳实践？",
    "下面关于 {topic} 的描述中，错误的是："
]
SAMPLE_SNIPPETS = [
    "print(sum([i for i in range(3)]))",
    "a = [1,2,3]\nprint(a[::-1])",
    "def f(x):\n    return x*x\nprint(f(3))"
]
OPTIONS_TEMPLATE = ['A', 'B', 'C', 'D']

def gen_question(idx: int) -> dict:
    category = random.choice(CATEGORIES)
    difficulty = random.choices(DIFFICULTIES, weights=[0.4, 0.4, 0.2])[0]
    topic = category
    title_tpl = random.choice(SAMPLE_TITLES)
    snippet = random.choice(SAMPLE_SNIPPETS) if '{snippet}' in title_tpl else ''
    title = title_tpl.format(topic=topic, snippet=snippet)
    options = {
        'A': f"选项 A 描述 {idx}",
        'B': f"选项 B 描述 {idx}",
        'C': f"选项 C 描述 {idx}",
        'D': f"选项 D 描述 {idx}"
    }
    correct = random.choice(OPTIONS_TEMPLATE)
    tags = [category.split()[0].lower(), difficulty.lower()]
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'title': title,
        'content': snippet or f"请回答关于 {topic} 的问题。",
        'options': options,
        'correct_answer': correct,
        'category': category,
        'difficulty': difficulty,
        'tags': tags,
        'created_at': created_at,
        'frequency': 0
    }

def generate_questions(n: int = 200) -> list:
    questions = []
    # 保证各分类、难度有覆盖：先按类别和难度各生成一些，然后随机填充
    per_cat = max(1, n // len(CATEGORIES))
    for cat in CATEGORIES:
        for i in range(per_cat):
            q = gen_question(len(questions) + 1)
            q['category'] = cat
            questions.append(q)
    while len(questions) < n:
        questions.append(gen_question(len(questions) + 1))
    # 截取并随机打乱
    questions = questions[:n]
    random.shuffle(questions)
    return questions

def save_json(questions: list, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

def init_sqlite_db(db_path: str, questions: list):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        options TEXT,
        correct_answer TEXT,
        category TEXT,
        difficulty TEXT,
        tags TEXT,
        created_at TEXT,
        frequency INTEGER DEFAULT 0
    )
    """)
    insert_sql = """
    INSERT INTO questions
    (title, content, options, correct_answer, category, difficulty, tags, created_at, frequency)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = []
    for q in questions:
        params.append((
            q['title'],
            q['content'],
            json.dumps(q['options'], ensure_ascii=False),
            q['correct_answer'],
            q['category'],
            q['difficulty'],
            json.dumps(q.get('tags', []), ensure_ascii=False),
            q['created_at'],
            q.get('frequency', 0)
        ))
    cur.executemany(insert_sql, params)
    conn.commit()
    conn.close()

def main():
    n = 200
    questions = generate_questions(n)
    save_json(questions, JSON_PATH)
    init_sqlite_db(DB_PATH, questions)
    print(f"已生成 {n} 道题并保存为 JSON：{JSON_PATH}")
    print(f"已在本地 sqlite DB 初始化题库：{DB_PATH}")

if __name__ == '__main__':
    main()