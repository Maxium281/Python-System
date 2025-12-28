# -*- coding: utf-8 -*-
"""
init_db.py
B模块：数据库初始化脚本
功能：
- 创建 SQLite 数据库文件 python_learning.db
- 建立初始表（如用户表、题目表、提交记录表等）
"""

import sqlite3

print("init_db.py 正在运行")

# 连接数据库，如果不存在则创建
conn = sqlite3.connect("python_learning.db")
cursor = conn.cursor()

# 创建用户表
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# 创建题目表（示例）
cursor.execute("""
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT
)
""")

# 创建提交记录表（判题系统示例）
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    problem_id INTEGER,
    code TEXT,
    result TEXT,
    submit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(problem_id) REFERENCES problems(id)
)
""")

conn.commit()
conn.close()

print("数据库 python_learning.db 创建完成")