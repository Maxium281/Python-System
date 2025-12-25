# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from app.core.question_bank import QuestionBank
from app.database.db_manager import DBManager
from app.core.user_progress import UserProgress

index_bp = Blueprint('main', __name__)

db_manager = DBManager()
question_bank = QuestionBank(db_manager)

@index_bp.route('/')
def index():
    # load basic data for template
    try:
        category_list = question_bank.get_category_list()
    except Exception:
        category_list = []
    try:
        user_progress = UserProgress(db_manager).get_progress()
    except Exception:
        user_progress = {'completion_rate': 0, 'practiced_count': 0, 'accuracy_rate': 0, 'mock_interview_count': 0}
    try:
        total_row = db_manager.query("SELECT COUNT(*) as cnt FROM questions").fetchone()
        total_questions = total_row['cnt'] if total_row else 0
    except Exception:
        total_questions = 0
    total_users = 1
    return render_template(
        'index.html',
        category_list=category_list,
        user_progress=user_progress,
        total_questions=total_questions,
        total_users=total_users
    )
