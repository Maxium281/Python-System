from __future__ import annotations

import random
import time
from typing import Any, Dict, List, Optional, Tuple

from flask import Blueprint, jsonify, render_template, request, session

from app.database.db import fetch_all, fetch_one, get_conn, init_schema

bp = Blueprint("interview", __name__)


def _normalize_answer(ans: str) -> str:
	if not ans:
		return ""
	ans = ans.upper()
	ans = "".join([c for c in ans if c in "ABCD"])
	return "".join(sorted(ans))


def _visible_where(category_key: str) -> Tuple[str, Tuple[Any, ...]]:
	# 与题库分类页口径一致（basic/framework/project）
	key = (category_key or "").lower().strip()
	if key == "basic":
		return "(category LIKE '%Basics%' OR category LIKE '%基础%')", ()
	if key == "framework":
		return "(category LIKE '%Flask%' OR category LIKE '%框架%')", ()
	if key == "project":
		return "(category LIKE '%Project%' OR category LIKE '%项目%')", ()
	# all：三类合并（避免抽到“题库页看不到”的题导致用户困惑）
	return (
		"(category LIKE '%Basics%' OR category LIKE '%基础%' OR category LIKE '%Flask%' OR category LIKE '%框架%' OR category LIKE '%Project%' OR category LIKE '%项目%')",
		(),
	)


def _pick_question_ids(count: int, category: str = "all") -> List[int]:
	where, params = _visible_where(category)
	rows = fetch_all(f"SELECT id FROM questions WHERE {where} ORDER BY id ASC", params)
	ids = [int(r["id"]) for r in rows]
	if not ids:
		return []
	count = max(1, min(int(count), 50, len(ids)))  # 上限保护
	return random.sample(ids, count)


def _get_question_payload(question_id: int) -> Optional[Dict[str, Any]]:
	q = fetch_one(
		"""
		SELECT id, category, title, option_a, option_b, option_c, option_d, difficulty
		FROM questions
		WHERE id=?
		""",
		(question_id,),
	)
	if not q:
		return None

	a = fetch_one("SELECT correct_answer FROM answers WHERE question_id=?", (question_id,))
	correct = _normalize_answer((a or {}).get("correct_answer", ""))
	q_type = "multi" if len(correct) > 1 else "single"

	return {
		"id": q["id"],
		"title": q["title"],
		"category": q.get("category") or "",
		"difficulty": q.get("difficulty") or "Easy",
		"type": q_type,
		"options": [
			{"option_key": "A", "option_content": q.get("option_a") or ""},
			{"option_key": "B", "option_content": q.get("option_b") or ""},
			{"option_key": "C", "option_content": q.get("option_c") or ""},
			{"option_key": "D", "option_content": q.get("option_d") or ""},
		],
	}


@bp.get("/interview/mock")
@bp.get("/exam/mock")
def mock_interview():
	init_schema()
	return render_template("mock_interview.html")


@bp.post("/exam/api/start")
def api_start():
	init_schema()
	payload = request.get_json(silent=True) or {}
	count = int(payload.get("count") or 10)
	category = str(payload.get("category") or "all")
	time_limit = int(payload.get("time_limit_seconds") or 10 * 60)  # 默认 10 分钟
	time_limit = max(60, min(time_limit, 60 * 60))  # 1min~60min

	ids = _pick_question_ids(count=count, category=category)
	if not ids:
		return jsonify({"success": False, "msg": "题库为空或该分类下无题目"}), 400

	now = int(time.time())
	session["mock"] = {
		"ids": ids,
		"idx": 0,
		"start_ts": now,
		"time_limit": time_limit,
		"category": category,
		"answers": {},  # qid -> {user_answer,is_correct}
	}

	first = _get_question_payload(ids[0])
	return jsonify(
		{
			"success": True,
			"data": {
				"total": len(ids),
				"index": 1,
				"time_limit_seconds": time_limit,
				"start_ts": now,
				"question": first,
			},
		}
	)


@bp.get("/exam/api/question")
def api_current_question():
	init_schema()
	state = session.get("mock") or {}
	ids = state.get("ids") or []
	idx = int(state.get("idx") or 0)

	if not ids:
		return jsonify({"success": False, "msg": "未开始模拟面试，请先开始"}), 400
	if idx < 0 or idx >= len(ids):
		return jsonify({"success": False, "msg": "模拟面试已结束"}), 400

	q = _get_question_payload(int(ids[idx]))
	return jsonify(
		{
			"success": True,
			"data": {
				"total": len(ids),
				"index": idx + 1,
				"time_limit_seconds": int(state.get("time_limit") or 0),
				"start_ts": int(state.get("start_ts") or 0),
				"question": q,
			},
		}
	)


@bp.post("/exam/api/submit")
def api_submit():
	init_schema()
	state = session.get("mock") or {}
	ids = state.get("ids") or []
	idx = int(state.get("idx") or 0)

	if not ids:
		return jsonify({"success": False, "msg": "未开始模拟面试"}), 400
	if idx < 0 or idx >= len(ids):
		return jsonify({"success": False, "msg": "模拟面试已结束"}), 400

	payload = request.get_json(silent=True) or {}
	try:
		question_id = int(payload.get("question_id"))
	except Exception:
		return jsonify({"success": False, "msg": "question_id 无效"}), 400

	current_id = int(ids[idx])
	if question_id != current_id:
		return jsonify({"success": False, "msg": "题目状态不同步，请刷新重试"}), 409

	user_answer = _normalize_answer(payload.get("user_answer", ""))
	if not user_answer:
		return jsonify({"success": False, "msg": "请选择答案后提交"}), 400

	a = fetch_one("SELECT correct_answer, analysis, knowledge_point FROM answers WHERE question_id=?", (question_id,))
	correct = _normalize_answer((a or {}).get("correct_answer", ""))

	is_correct = 1 if (correct and user_answer == correct) else 0

	# 写入练习记录（用于进度统计）
	q_meta = fetch_one("SELECT category, difficulty FROM questions WHERE id=?", (question_id,)) or {}
	with get_conn() as conn:
		conn.execute(
			"""
			INSERT INTO attempts(user_id, question_id, user_answer, is_correct, category, difficulty)
			VALUES(1,?,?,?,?,?)
			""",
			(question_id, user_answer, is_correct, q_meta.get("category"), q_meta.get("difficulty")),
		)

	# 更新 session
	answers = state.get("answers") or {}
	answers[str(question_id)] = {"user_answer": user_answer, "is_correct": bool(is_correct)}
	state["answers"] = answers

	# 前进
	next_idx = idx + 1
	state["idx"] = next_idx
	session["mock"] = state

	finished = next_idx >= len(ids)
	next_qid = None if finished else int(ids[next_idx])

	return jsonify(
		{
			"success": True,
			"data": {
				"is_correct": bool(is_correct),
				"correct_answer": correct,
				"analysis": (a or {}).get("analysis") or "",
				"knowledge_point": (a or {}).get("knowledge_point") or "",
				"finished": finished,
				"next_question_id": next_qid,
				"progress": {"total": len(ids), "index": min(next_idx + 1, len(ids))},
			},
		}
	)


@bp.post("/exam/api/finish")
def api_finish():
	init_schema()
	state = session.get("mock") or {}
	answers = state.get("answers") or {}
	total = len(state.get("ids") or [])
	correct = sum(1 for v in answers.values() if v.get("is_correct") is True)
	wrong = max(0, len(answers) - correct)

	# 可选：结束后清理 session
	session.pop("mock", None)

	accuracy = int(round((correct / total) * 100, 0)) if total else 0
	return jsonify(
		{
			"success": True,
			"data": {
				"total": total,
				"answered": len(answers),
				"correct": correct,
				"wrong": wrong,
				"accuracy": accuracy,
			},
		}
	)
