import sqlite3

conn = sqlite3.connect("python_learning.db")
cur = conn.cursor()

# 用户表
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
""")

# 学习大纲
cur.execute("""
CREATE TABLE IF NOT EXISTS syllabus (
    syllabus_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    source TEXT NOT NULL,
    description TEXT
);
""")

# 知识点
cur.execute("""
CREATE TABLE IF NOT EXISTS knowledge_points (
    kp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    syllabus_id INTEGER,
    title TEXT NOT NULL,
    content TEXT,
    difficulty INTEGER,
    FOREIGN KEY (syllabus_id) REFERENCES syllabus(syllabus_id)
);
""")

# 学习进度
cur.execute("""
CREATE TABLE IF NOT EXISTS learning_progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    kp_id INTEGER,
    status TEXT,
    last_update DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (kp_id) REFERENCES knowledge_points(kp_id)
);
""")

# 编程题（PTA / 力扣）
cur.execute("""
CREATE TABLE IF NOT EXISTS programming_problems (
    problem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    kp_id INTEGER,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    input_desc TEXT,
    output_desc TEXT,
    sample_input TEXT,
    sample_output TEXT,
    time_limit INTEGER DEFAULT 1,
    memory_limit INTEGER DEFAULT 64,
    FOREIGN KEY (kp_id) REFERENCES knowledge_points(kp_id)
);
""")

# 测试用例
cur.execute("""
CREATE TABLE IF NOT EXISTS test_cases (
    case_id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER,
    input_data TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    is_sample INTEGER DEFAULT 0,
    FOREIGN KEY (problem_id) REFERENCES programming_problems(problem_id)
);
""")

# 提交记录
cur.execute("""
CREATE TABLE IF NOT EXISTS code_submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    problem_id INTEGER,
    code TEXT NOT NULL,
    language TEXT DEFAULT 'python',
    result TEXT,
    runtime REAL,
    submit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (problem_id) REFERENCES programming_problems(problem_id)
);
""")

# 默认用户
cur.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('x', '1', 'student');
""")

# 默认大纲
cur.execute("""
INSERT OR IGNORE INTO syllabus (name, source, description)
VALUES (
    '全国计算机等级考试二级 Python',
    '教育部考试中心',
    '面向 Python 基础与数据处理能力的公开考试大纲'
);
""")

conn.commit()
conn.close()

print("数据库 python_learning.db 创建完成")