# -*- coding: utf-8 -*-
import os
import logging

# Initialize logger at module level before class definition
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LocalResourceLoader:
    """
    Simple local static resource checker/loader.
    Do not import app.core.config here to avoid circular imports.
    """
    def __init__(self, static_path: str = None):
        # Default to project static directory if not provided
        if static_path:
            self.static_path = os.path.abspath(static_path)
        else:
            self.static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static'))
        self.required_resources = [
            os.path.join(self.static_path, 'css', 'bootstrap.css'),
            os.path.join(self.static_path, 'css', 'custom.css'),
            os.path.join(self.static_path, 'js', 'bootstrap.bundle.min.js'),
            os.path.join(self.static_path, 'js', 'jquery-3.6.0.min.js')
        ]

    def check_resource_exists(self):
        """
        Verify required static resources exist. Raises FileNotFoundError if any missing.
        """
        missing = []
        for resource in self.required_resources:
            if not os.path.exists(resource):
                missing.append(resource)
        if missing:
            msg = f"Missing static resources: {missing}"
            logger.error(msg)
            raise FileNotFoundError(msg)
        logger.info("All required static resources present")

    def load_css(self, css_name: str) -> str:
        """
        Return URL path for a css file under static/css if exists, else empty string.
        """
        css_path = os.path.join(self.static_path, 'css', css_name)
        if not os.path.exists(css_path):
            logger.warning(f"CSS not found: {css_path}")
            return ''
        return f"/static/css/{css_name}"

    def load_js(self, js_name: str) -> str:
        """
        Return URL path for a js file under static/js if exists, else empty string.
        """
        js_path = os.path.join(self.static_path, 'js', js_name)
        if not os.path.exists(js_path):
            logger.warning(f"JS not found: {js_path}")
            return ''
        return f"/static/js/{js_name}"
