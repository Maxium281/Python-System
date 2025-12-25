# -*- coding: utf-8 -*-
from app.routes.index import index_bp
from app.routes.question import question_bp
from app.routes.exam import exam_bp
from app.routes.progress import progress_bp

def register_routes(app):
    """
    Register blueprints for the Flask application.
    """
    app.register_blueprint(index_bp)
    app.register_blueprint(question_bp, url_prefix='/question')
    app.register_blueprint(exam_bp, url_prefix='/exam')
    app.register_blueprint(progress_bp, url_prefix='/progress')
