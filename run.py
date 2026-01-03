# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import uuid

from flask import Flask, jsonify

from app.blueprints.interview import bp as interview_bp
from app.blueprints.main import bp as main_bp
from app.blueprints.progress import bp as progress_bp
from app.blueprints.question import bp as question_bp
from app.database.db import init_schema


def create_app() -> Flask:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "pages"),
        static_folder=os.path.join(base_dir, "static"),
    )

    # 关键：即使 debug=False，也尽量让模板变更可生效（开发排查期）
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True

    # 可选：开发期尽量不要缓存静态文件
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    # 单机：启动即确保建库
    init_schema()

    # 实例标识：用来确认你浏览器连到的到底是不是这份 run.py
    app.config["APP_INSTANCE_ID"] = os.environ.get("APP_INSTANCE_ID") or uuid.uuid4().hex

    @app.after_request
    def _add_instance_header(resp):
        resp.headers["X-App-Instance"] = app.config["APP_INSTANCE_ID"]
        return resp

    # 调试：确认“当前运行的是哪份工程/模板目录”
    @app.get("/__debug/info")
    def __debug_info():
        searchpath = []
        try:
            searchpath = list(getattr(app.jinja_loader, "searchpath", []) or [])
        except Exception:
            searchpath = []
        return jsonify(
            {
                "instance_id": app.config["APP_INSTANCE_ID"],
                "base_dir": base_dir,
                "template_folder": app.template_folder,
                "static_folder": app.static_folder,
                "jinja_searchpath": searchpath,
                "cwd": os.getcwd(),
            }
        )

    @app.get("/__debug/ping")
    def __debug_ping():
        return "pong"

    app.register_blueprint(main_bp)
    app.register_blueprint(question_bp, url_prefix="/question")
    app.register_blueprint(progress_bp, url_prefix="/progress")
    app.register_blueprint(interview_bp)

    # 关键：启用 session（模拟面试需要）
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-dev-secret-key")

    return app


app = create_app()

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("DEBUG", "0") == "1"

    print("[run.py] instance_id =", app.config.get("APP_INSTANCE_ID"))
    print("[run.py] base_dir     =", os.path.dirname(os.path.abspath(__file__)))
    print("[run.py] url_map      =")
    print(app.url_map)

    app.run(host=host, port=port, debug=debug, threaded=True)
