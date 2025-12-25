# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify
from app.core.question_bank import QuestionBank
from app.core.user_progress import UserProgress
from app.database.db_manager import DBManager

question_bp = Blueprint('question', __name__)
db_manager = DBManager()
question_bank = QuestionBank(db_manager)
user_progress = UserProgress(db_manager)

@question_bp.route('/category')
def question_category():
    """
    Render the question category page (pages/question_category.html)
    """
    return render_template('question_category.html')

@question_bp.route('/detail/<int:question_id>')
def question_detail(question_id):
    """
    Render the answer page (answer_page.html)
    """
    return render_template('answer_page.html', question_id=question_id)

@question_bp.route('/explanation/<int:question_id>')
def question_explanation(question_id):
    """
    Render the explanation page (explanation.html)
    """
    return render_template('explanation.html', question_id=question_id)

@question_bp.route('/api/questions', methods=['GET'])
def api_get_questions():
    """
    Query list of questions.
    Query param: category (basic|framework|project)
    """
    category_map = {
        "basic": "Python Basics",
        "framework": "Flask Framework",
        "project": "Project Experience"
    }
    req_cat = request.args.get('category', 'basic')
    db_cat = category_map.get(req_cat, req_cat)
    try:
        questions = question_bank.get_questions_by_category(db_cat, page=1, page_size=100)
        data = [{"id": q.get('id'), "category": q.get('category'), "title": q.get('title')} for q in questions]
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

@question_bp.route('/api/question/<int:question_id>', methods=['GET'])
def api_get_question(question_id):
    """
    Return question detail compatible with frontend.
    """
    q = question_bank.get_question_by_id(question_id)
    if not q:
        return jsonify({"success": False, "msg": "question not found"}), 404
    q_type = "single" if len(q.get('correct_answer', '')) <= 1 else "multiple"
    options = [
        {"option_key": "A", "option_content": q.get('option_a', '')},
        {"option_key": "B", "option_content": q.get('option_b', '')},
        {"option_key": "C", "option_content": q.get('option_c', '')},
        {"option_key": "D", "option_content": q.get('option_d', '')},
    ]
    resp = {"id": q.get('id'), "title": q.get('title'), "type": q_type, "difficulty": q.get('difficulty', ''), "options": options}
    return jsonify({"success": True, "data": resp})

@question_bp.route('/api/submit_answer', methods=['POST'])
def api_submit_answer():
    """
    Save submitted answer via UserProgress.save_answer
    Body: { question_id: int, user_answer: "A" }
    """
    try:
        data = request.get_json() or {}
        qid = int(data.get('question_id', 0))
        uans = data.get('user_answer', '')
        if not qid or uans is None:
            return jsonify({"success": False, "msg": "invalid parameters"}), 400
        ok = user_progress.save_answer(qid, uans)
        return jsonify({"success": ok, "msg": "saved" if ok else "save failed"})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500
