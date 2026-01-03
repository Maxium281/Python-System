# -*- coding: utf-8 -*-
"""
init_db.py
B模块：数据库初始化脚本（保持原表结构）
"""
from __future__ import annotations

import os
import sqlite3
from typing import Optional


def init_db(db_path: str = "python_learning.db") -> None:
	db_path = os.path.abspath(db_path)
	conn = sqlite3.connect(db_path)
	try:
		cursor = conn.cursor()

		cursor.execute(
			"""
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT UNIQUE,
				password TEXT
			)
			"""
		)

		cursor.execute(
			"""
			CREATE TABLE IF NOT EXISTS problems (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT,
				description TEXT
			)
			"""
		)

		cursor.execute(
			"""
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
			"""
		)

		conn.commit()
	finally:
		conn.close()


def main() -> None:
	print("init_db.py 正在运行")
	init_db("python_learning.db")
	print("数据库 python_learning.db 创建完成")


if __name__ == "__main__":
	main()