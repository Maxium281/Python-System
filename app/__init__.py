# -*- coding: utf-8 -*-
from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader
from app.routes import register_routes
from app.utils.logger import Logger
import os

logger = Logger()

def create_app(config):
    # 创建 Flask 应用，支持同时从 app/templates 与 项目根 pages 加载模板
    app = Flask(
        __name__,
        template_folder=config.TEMPLATE_PATH,
        static_folder=config.STATIC_PATH
    )
    pages_path = os.path.abspath(os.path.join(config.BASE_DIR, 'pages'))
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(config.TEMPLATE_PATH),
        FileSystemLoader(pages_path)
    ])
    # 注册路由蓝图
    register_routes(app)
    app.config['STATIC_FOLDER'] = config.STATIC_PATH
    app.config['TEMPLATE_FOLDER'] = config.TEMPLATE_PATH
    logger.info("Flask app initialized successfully")
    return app
