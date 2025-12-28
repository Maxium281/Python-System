# -*- coding: utf-8 -*-
"""
本地资源加载器模块
提供静态资源检查、加载、验证等功能
"""
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LocalResourceLoader:
    """本地资源加载器类"""
    
    def __init__(self, static_path: str = None):
        """初始化资源加载器"""
        if static_path:
            self.static_path = os.path.abspath(static_path)
        else:
            self.static_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..', 'static')
            )
        
        self.required_resources = [
            os.path.join(self.static_path, 'css', 'bootstrap.css'),
            os.path.join(self.static_path, 'css', 'custom.css'),
            os.path.join(self.static_path, 'js', 'bootstrap.bundle.min.js'),
            os.path.join(self.static_path, 'js', 'jquery-3.6.0.min.js')
        ]
    
    def check_resource_exists(self) -> bool:
        """检查必需的静态资源是否存在"""
        missing = []
        for resource in self.required_resources:
            if not os.path.exists(resource):
                missing.append(resource)
        
        if missing:
            msg = f"缺失的静态资源: {missing}"
            logger.error(msg)
            raise FileNotFoundError(msg)
        
        logger.info("所有必需的静态资源都存在")
        return True
    
    def check_all_resources(self) -> dict:
        """检查所有静态资源"""
        result = {'exists': [], 'missing': []}
        
        for resource in self.required_resources:
            if os.path.exists(resource):
                result['exists'].append(resource)
            else:
                result['missing'].append(resource)
        
        return result
    
    def load_css(self, css_name: str) -> str:
        """加载CSS文件并返回URL路径"""
        css_path = os.path.join(self.static_path, 'css', css_name)
        if not os.path.exists(css_path):
            logger.warning(f"CSS文件不存在: {css_path}")
            return ''
        
        return f"/static/css/{css_name}"
    
    def load_js(self, js_name: str) -> str:
        """加载JavaScript文件并返回URL路径"""
        js_path = os.path.join(self.static_path, 'js', js_name)
        if not os.path.exists(js_path):
            logger.warning(f"JS文件不存在: {js_path}")
            return ''
        
        return f"/static/js/{js_name}"
    
    def load_image(self, image_name: str, subfolder: str = 'images') -> str:
        """加载图片文件并返回URL路径"""
        image_path = os.path.join(self.static_path, subfolder, image_name)
        if not os.path.exists(image_path):
            logger.warning(f"图片文件不存在: {image_path}")
            return ''
        
        return f"/static/{subfolder}/{image_name}"
