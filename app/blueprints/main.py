from __future__ import annotations

from flask import Blueprint, render_template

from app.database.db import fetch_one, init_schema

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
	init_schema()

	total_questions = (
		fetch_one(
			"""
			SELECT COUNT(1) AS c
			FROM questions
			WHERE
				category LIKE '%Basics%' OR category LIKE '%基础%'
				OR category LIKE '%Flask%' OR category LIKE '%框架%'
				OR category LIKE '%Project%' OR category LIKE '%项目%'
			"""
		)
		or {}
	).get("c", 0)
	total_users = (fetch_one("SELECT COUNT(1) AS c FROM users") or {}).get("c", 1)

	agg = fetch_one(
		"""
		SELECT
			COUNT(1) AS total,
			SUM(CASE WHEN is_correct=1 THEN 1 ELSE 0 END) AS correct
		FROM attempts
		WHERE user_id=1
		"""
	) or {"total": 0, "correct": 0}

	practiced_count = int(agg.get("total") or 0)
	correct = int(agg.get("correct") or 0)
	accuracy_rate = int(round((correct / practiced_count) * 100, 0)) if practiced_count else 0
	completion_rate = int(round((practiced_count / total_questions) * 100, 0)) if total_questions else 0

	user_progress = {
		"completion_rate": completion_rate,
		"practiced_count": practiced_count,
		"accuracy_rate": accuracy_rate,
		"mock_interview_count": 0,
	}

	return render_template(
		"index.html",
		total_questions=total_questions,
		total_users=total_users,
		user_progress=user_progress,
	)
