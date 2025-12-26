# Python学习教辅软件 - 数据库设计文档（B模块）

## 数据库文件
- 文件名：python_learning.db
- 类型：SQLite3

## 数据表设计

### 1. users（用户表）
| 字段名  | 类型    | 描述                |
|--------|--------|-------------------|
| id     | INTEGER PRIMARY KEY AUTOINCREMENT | 用户ID |
| username | TEXT UNIQUE | 用户名 |
| password | TEXT | 密码 |

### 2. problems（题目表）
| 字段名  | 类型    | 描述                |
|--------|--------|-------------------|
| id     | INTEGER PRIMARY KEY AUTOINCREMENT | 题目ID |
| title  | TEXT   | 题目标题           |
| description | TEXT | 题目描述 |

### 3. submissions（提交记录表）
| 字段名  | 类型    | 描述                |
|--------|--------|-------------------|
| id       | INTEGER PRIMARY KEY AUTOINCREMENT | 提交ID |
| user_id  | INTEGER | 用户ID，关联 users(id) |
| problem_id | INTEGER | 题目ID，关联 problems(id) |
| code     | TEXT   | 用户提交的代码      |
| result   | TEXT   | 判题结果            |
| submit_time | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | 提交时间 |