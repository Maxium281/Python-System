from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional, Tuple

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "interview.db")


def _connect() -> sqlite3.Connection:
	os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	conn.execute("PRAGMA foreign_keys = ON;")
	return conn


def init_schema() -> None:
	conn = _connect()
	try:
		conn.executescript(
			"""
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT UNIQUE,
				created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
			);

			CREATE TABLE IF NOT EXISTS questions (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				category TEXT NOT NULL,
				title TEXT NOT NULL,
				option_a TEXT,
				option_b TEXT,
				option_c TEXT,
				option_d TEXT,
				difficulty TEXT DEFAULT 'Easy',
				is_high_frequency INTEGER DEFAULT 0
			);

			CREATE TABLE IF NOT EXISTS answers (
				question_id INTEGER PRIMARY KEY,
				correct_answer TEXT NOT NULL,
				analysis TEXT,
				knowledge_point TEXT,
				FOREIGN KEY(question_id) REFERENCES questions(id) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS attempts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER NOT NULL DEFAULT 1,
				question_id INTEGER NOT NULL,
				user_answer TEXT NOT NULL,
				is_correct INTEGER NOT NULL,
				category TEXT,
				difficulty TEXT,
				created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY(user_id) REFERENCES users(id),
				FOREIGN KEY(question_id) REFERENCES questions(id)
			);

			CREATE TABLE IF NOT EXISTS favorites (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER NOT NULL DEFAULT 1,
				question_id INTEGER NOT NULL,
				collect_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				UNIQUE(user_id, question_id),
				FOREIGN KEY(user_id) REFERENCES users(id),
				FOREIGN KEY(question_id) REFERENCES questions(id)
			);
			"""
		)
		conn.execute("INSERT OR IGNORE INTO users(id, username) VALUES(1, 'local_user');")
		conn.commit()
	finally:
		conn.close()


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
	conn = _connect()
	try:
		yield conn
		conn.commit()
	except Exception:
		conn.rollback()
		raise
	finally:
		conn.close()


def fetch_one(sql: str, params: Tuple[Any, ...] = ()) -> Optional[Dict[str, Any]]:
	with get_conn() as conn:
		row = conn.execute(sql, params).fetchone()
		return dict(row) if row else None


def fetch_all(sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
	with get_conn() as conn:
		rows = conn.execute(sql, params).fetchall()
		return [dict(r) for r in rows]
