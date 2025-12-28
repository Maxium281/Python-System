# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify
from app.core.question_bank import QuestionBank
from app.core.interview_simulator import InterviewSimulator
from app.database.db_manager import DBManager

# blueprint 名称修改为 interview，以匹配模板中的 url_for('interview.mock_interview')
exam_bp = Blueprint('interview', __name__)
db_manager = DBManager()
question_bank = QuestionBank(db_manager)
interview_simulator = InterviewSimulator(question_bank, db_manager)

@exam_bp.route('/generate')
def generate_exam():
    category = request.args.get('category', None)
    questions = interview_simulator.generate_exam(category)
    interview_simulator.start_exam()
    return render_template('exam.html', questions=questions, exam_id=interview_simulator.exam_id)

@exam_bp.route('/end', methods=['POST'])
def end_exam():
    data = request.get_json()
    user_answers = data.get('user_answers', [])
    interview_simulator.end_exam()
    interview_simulator.save_exam_record(user_answers)
    return jsonify({'success': True, 'msg': 'Exam record saved'})

@exam_bp.route('/mock')
def mock_interview():
    """Render the mock interview page (mock_interview.html)."""
    return render_template('mock_interview.html')
