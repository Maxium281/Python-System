# -*- coding: utf-8 -*-
import os
from app.utils.local_resource_loader import LocalResourceLoader
from app.utils.logger import Logger

logger = Logger()

class Config:
    """
    Configuration manager for local paths and resource checks.
    All strings are UTF-8.
    """
    def __init__(self):
        # project root (two levels up from app/core)
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # default template folder (app/templates). pages/ is added to Jinja loader in app factory.
        self.TEMPLATE_PATH = os.path.join(self.BASE_DIR, 'app', 'templates')
        # static folder at project root/static
        self.STATIC_PATH = os.path.join(self.BASE_DIR, 'static')
        # database path
        self.DB_PATH = os.path.join(self.BASE_DIR, 'database', 'interview.db')
        # debug flag
        self.DEBUG = False
        # local resource loader expects static path
        self.resource_loader = LocalResourceLoader(self.STATIC_PATH)

    def check_local_resources(self):
        """
        Ensure required local directories exist and required static files are present.
        """
        required_dirs = [
            self.TEMPLATE_PATH,
            self.STATIC_PATH,
            os.path.join(self.STATIC_PATH, 'css'),
            os.path.join(self.STATIC_PATH, 'js'),
            os.path.dirname(self.DB_PATH)
        ]
        for d in required_dirs:
            if not os.path.exists(d):
                try:
                    os.makedirs(d, exist_ok=True)
                    logger.warning(f"Created missing directory: {d}")
                except Exception as e:
                    logger.error(f"Failed to create directory {d}: {e}")
        # validate required static resources (will raise FileNotFoundError if missing)
        try:
            self.resource_loader.check_resource_exists()
        except FileNotFoundError as e:
            logger.error(f"Static resource check failed: {e}")
            raise
        logger.info("Local resource check completed successfully")

    def get_config(self) -> dict:
        return {
            'BASE_DIR': self.BASE_DIR,
            'TEMPLATE_PATH': self.TEMPLATE_PATH,
            'STATIC_PATH': self.STATIC_PATH,
            'DB_PATH': self.DB_PATH,
            'DEBUG': self.DEBUG
        }
