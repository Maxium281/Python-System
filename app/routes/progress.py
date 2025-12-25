# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from app.core.user_progress import UserProgress
from app.database.db_manager import DBManager

progress_bp = Blueprint('progress', __name__)
db_manager = DBManager()
user_progress = UserProgress(db_manager)

@progress_bp.route('/')
def progress():
    progress_data = user_progress.get_progress()
    return render_template('progress.html', progress=progress_data)

@progress_bp.route('/error')
def error_questions():
    errors = user_progress.get_error_questions()
    return render_template('error_questions.html', error_questions=errors)

@progress_bp.route('/favorite')
def favorite_questions():
    favs = user_progress.get_favorite()
    return render_template('favorite_questions.html', favorite_questions=favs)
