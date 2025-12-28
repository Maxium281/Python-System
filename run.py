# -*- coding: utf-8 -*-
import os
from app import create_app
from app.core.config import Config

config = Config()
config.check_local_resources()
app = create_app(config)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
