from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from app.database.db import fetch_all, fetch_one, get_conn, init_schema

bp = Blueprint("progress", __name__)


@bp.get("/")
def progress():
	init_schema()

	agg = fetch_one(
		"""
		SELECT
			COUNT(1) AS total,
			SUM(CASE WHEN is_correct=1 THEN 1 ELSE 0 END) AS correct,
			SUM(CASE WHEN is_correct=0 THEN 1 ELSE 0 END) AS wrong
		FROM attempts
		WHERE user_id=1
		"""
	) or {"total": 0, "correct": 0, "wrong": 0}

	total = int(agg.get("total") or 0)
	correct = int(agg.get("correct") or 0)
	wrong = int(agg.get("wrong") or 0)
	accuracy = int(round((correct / total) * 100, 0)) if total else 0

	category_rows = fetch_all(
		"""
		SELECT category,
			   COUNT(1) AS total,
			   SUM(CASE WHEN is_correct=1 THEN 1 ELSE 0 END) AS correct
		FROM attempts
		WHERE user_id=1
		GROUP BY category
		ORDER BY total DESC
		"""
	)
	category_stats = {}
	for r in category_rows:
		t = int(r["total"] or 0)
		c = int(r["correct"] or 0)
		category_stats[r["category"] or "未分类"] = {
			"total": t,
			"correct": c,
			"accuracy": int(round((c / t) * 100, 0)) if t else 0,
		}

	diff_rows = fetch_all(
		"""
		SELECT difficulty,
			   COUNT(1) AS total,
			   SUM(CASE WHEN is_correct=1 THEN 1 ELSE 0 END) AS correct
		FROM attempts
		WHERE user_id=1
		GROUP BY difficulty
		ORDER BY total DESC
		"""
	)
	difficulty_stats = {}
	for r in diff_rows:
		t = int(r["total"] or 0)
		c = int(r["correct"] or 0)
		difficulty_stats[r["difficulty"] or "未知"] = {
			"total": t,
			"correct": c,
			"accuracy": int(round((c / t) * 100, 0)) if t else 0,
		}

	recent = fetch_one(
		"""
		SELECT
			COUNT(1) AS total,
			SUM(CASE WHEN is_correct=1 THEN 1 ELSE 0 END) AS correct
		FROM attempts
		WHERE user_id=1 AND datetime(created_at) >= datetime('now','-7 day')
		"""
	) or {"total": 0, "correct": 0}
	r_total = int(recent.get("total") or 0)
	r_correct = int(recent.get("correct") or 0)
	r_accuracy = int(round((r_correct / r_total) * 100, 0)) if r_total else 0

	error_count = (fetch_one(
		"SELECT COUNT(DISTINCT question_id) AS c FROM attempts WHERE user_id=1 AND is_correct=0"
	) or {}).get("c", 0)

	favorite_count = (fetch_one(
		"SELECT COUNT(1) AS c FROM favorites WHERE user_id=1"
	) or {}).get("c", 0)

	return render_template(
		"progress.html",
		progress={
			"total": total,
			"correct": correct,
			"wrong": wrong,
			"accuracy": accuracy,
			"category_stats": category_stats,
			"difficulty_stats": difficulty_stats,
			"recent_7_days": {"total": r_total, "correct": r_correct, "accuracy": r_accuracy},
			"error_count": int(error_count or 0),
			"favorite_count": int(favorite_count or 0),
		},
	)


@bp.get("/favorite")
@bp.get("/favorites")
def favorite_questions():
	init_schema()
	rows = fetch_all(
		"""
		SELECT q.id, q.title, q.category, q.difficulty, f.collect_time
		FROM favorites f
		JOIN questions q ON q.id=f.question_id
		WHERE f.user_id=1
		ORDER BY f.collect_time DESC
		"""
	)
	return render_template("favorite_questions.html", favorite_questions=rows)


@bp.get("/errors")
@bp.get("/error_questions")
def error_questions():
	init_schema()
	rows = fetch_all(
		"""
		SELECT q.id, q.title, q.category, q.difficulty, MAX(a.created_at) AS last_time
		FROM attempts a
		JOIN questions q ON q.id=a.question_id
		WHERE a.user_id=1 AND a.is_correct=0
		GROUP BY q.id, q.title, q.category, q.difficulty
		ORDER BY last_time DESC
		"""
	)
	return render_template("error_questions.html", error_questions=rows)


@bp.post("/api/favorite/toggle")
def api_toggle_favorite():
	init_schema()
	payload = request.get_json(silent=True) or {}
	try:
		question_id = int(payload.get("question_id"))
	except Exception:
		return jsonify({"success": False, "msg": "question_id 无效"}), 400

	with get_conn() as conn:
		exists = conn.execute(
			"SELECT 1 FROM favorites WHERE user_id=1 AND question_id=?",
			(question_id,),
		).fetchone()

		if exists:
			conn.execute(
				"DELETE FROM favorites WHERE user_id=1 AND question_id=?",
				(question_id,),
			)
			return jsonify({"success": True, "data": {"is_favorite": False}})
		else:
			conn.execute(
				"INSERT OR IGNORE INTO favorites(user_id, question_id) VALUES(1, ?)",
				(question_id,),
			)
			return jsonify({"success": True, "data": {"is_favorite": True}})
