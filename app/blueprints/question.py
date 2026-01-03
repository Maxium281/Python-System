from __future__ import annotations

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from app.database.db import fetch_all, fetch_one, get_conn, init_schema

bp = Blueprint("question", __name__)


def _normalize_answer(ans: str) -> str:
	if not ans:
		return ""
	ans = ans.upper()
	ans = "".join([c for c in ans if c in "ABCD"])
	return "".join(sorted(ans))


def _category_filter(category_key: str):
	# 前端传 basic/framework/project
	key = (category_key or "").lower().strip()
	if key == "basic":
		return "(category LIKE '%Basics%' OR category LIKE '%基础%')"
	if key == "framework":
		return "(category LIKE '%Flask%' OR category LIKE '%框架%')"
	if key == "project":
		return "(category LIKE '%Project%' OR category LIKE '%项目%')"
	return "1=1"


@bp.get("/category")
def question_category():
	init_schema()
	return render_template("question_category.html")


@bp.get("/answer")
def answer_page():
	init_schema()
	question_id = request.args.get("question_id", "1")
	return render_template("answer_page.html", question_id=question_id)


@bp.get("/detail/<int:question_id>")
def detail(question_id: int):
	# 前端列表硬编码 /question/detail/<id>，这里兼容到 /question/answer?question_id=...
	return redirect(url_for("question.answer_page", question_id=question_id))


@bp.get("/explanation/<int:question_id>")
def explanation(question_id: int):
	init_schema()
	# explanation.html 由前端 JS 调 API 填充，模板只负责 UI 容器
	return render_template("explanation.html", question_id=question_id)


# ---------------- API ----------------

@bp.get("/api/questions")
def api_questions():
	init_schema()
	category = request.args.get("category", "")
	where = _category_filter(category)

	rows = fetch_all(
		f"SELECT id, title, category FROM questions WHERE {where} ORDER BY id ASC"
	)
	return jsonify({"success": True, "data": rows})


@bp.get("/api/question/<int:question_id>")
def api_question(question_id: int):
	init_schema()
	q = fetch_one(
		"""
		SELECT id, category, title, option_a, option_b, option_c, option_d, difficulty
		FROM questions
		WHERE id=?
		""",
		(question_id,),
	)
	if not q:
		return jsonify({"success": False, "msg": "题目不存在"}), 404

	a = fetch_one("SELECT correct_answer FROM answers WHERE question_id=?", (question_id,))
	correct = _normalize_answer((a or {}).get("correct_answer", ""))

	q_type = "multi" if len(correct) > 1 else "single"
	options = [
		{"option_key": "A", "option_content": q.get("option_a") or ""},
		{"option_key": "B", "option_content": q.get("option_b") or ""},
		{"option_key": "C", "option_content": q.get("option_c") or ""},
		{"option_key": "D", "option_content": q.get("option_d") or ""},
	]

	return jsonify(
		{
			"success": True,
			"data": {
				"id": q["id"],
				"title": q["title"],
				"category": q["category"],
				"difficulty": q.get("difficulty") or "Easy",
				"type": q_type,
				"options": options,
			},
		}
	)


@bp.post("/api/submit_answer")
def api_submit_answer():
	init_schema()
	payload = request.get_json(silent=True) or {}
	try:
		question_id = int(payload.get("question_id"))
	except Exception:
		return jsonify({"success": False, "msg": "question_id 无效"}), 400

	user_answer = _normalize_answer(payload.get("user_answer", ""))

	q = fetch_one(
		"SELECT id, category, difficulty FROM questions WHERE id=?",
		(question_id,),
	)
	if not q:
		return jsonify({"success": False, "msg": "题目不存在"}), 404

	a = fetch_one("SELECT correct_answer FROM answers WHERE question_id=?", (question_id,))
	correct = _normalize_answer((a or {}).get("correct_answer", ""))

	is_correct = 1 if (user_answer and correct and user_answer == correct) else 0

	with get_conn() as conn:
		conn.execute(
			"""
			INSERT INTO attempts(user_id, question_id, user_answer, is_correct, category, difficulty)
			VALUES(1,?,?,?,?,?)
			""",
			(question_id, user_answer, is_correct, q.get("category"), q.get("difficulty")),
		)

	return jsonify(
		{
			"success": True,
			"data": {
				"question_id": question_id,
				"user_answer": user_answer,
				"correct_answer": correct,
				"is_correct": bool(is_correct),
			},
		}
	)


@bp.get("/api/explanation/<int:question_id>")
def api_explanation(question_id: int):
	init_schema()
	user_answer = _normalize_answer(request.args.get("user_answer", ""))

	q = fetch_one(
		"""
		SELECT id, title FROM questions WHERE id=?
		""",
		(question_id,),
	)
	if not q:
		return jsonify({"success": False, "msg": "题目不存在"}), 404

	a = fetch_one(
		"""
		SELECT correct_answer, analysis, knowledge_point
		FROM answers
		WHERE question_id=?
		""",
		(question_id,),
	) or {}

	correct = _normalize_answer(a.get("correct_answer", ""))
	is_correct = bool(user_answer and correct and user_answer == correct)

	return jsonify(
		{
			"success": True,
			"data": {
				"id": q["id"],
				"title": q["title"],
				"user_answer": user_answer or "未作答",
				"correct_answer": correct or "--",
				"is_correct": is_correct,
				"analysis": a.get("analysis") or "",
				"knowledge_point": a.get("knowledge_point") or "",
			},
		}
	)
