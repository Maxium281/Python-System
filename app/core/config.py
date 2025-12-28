# -*- coding: utf-8 -*-
"""
配置管理模块
提供系统配置、路径管理、资源验证等功能
"""
import os
from typing import Dict, Any
from app.utils.local_resource_loader import LocalResourceLoader
from app.utils.logger import Logger

logger = Logger()


class Config:
    """配置管理器类"""
    
    DEFAULT_QUESTION_COUNT = 20
    DEFAULT_TIME_LIMIT = 30 * 60
    DEFAULT_PAGE_SIZE = 20
    MAX_QUESTION_COUNT = 100
    MIN_QUESTION_COUNT = 5
    
    def __init__(self, config_file: str = None):
        """初始化配置管理器"""
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        # 路径配置
        self.TEMPLATE_PATH = os.path.join(self.BASE_DIR, 'app', 'templates')
        self.STATIC_PATH = os.path.join(self.BASE_DIR, 'static')
        self.DB_PATH = os.path.join(self.BASE_DIR, 'database', 'interview.db')
        self.LOG_DIR = os.path.join(self.BASE_DIR, 'logs')
        
        # 应用配置
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.HOST = os.getenv('HOST', '127.0.0.1')
        self.PORT = int(os.getenv('PORT', '5000'))
        
        # 数据库配置
        self.DB_TIMEOUT = int(os.getenv('DB_TIMEOUT', '20'))
        self.DB_CHECK_SAME_THREAD = os.getenv('DB_CHECK_SAME_THREAD', 'False').lower() == 'true'
        
        # 考试配置
        self.DEFAULT_QUESTION_COUNT = int(os.getenv('DEFAULT_QUESTION_COUNT', str(self.DEFAULT_QUESTION_COUNT)))
        self.DEFAULT_TIME_LIMIT = int(os.getenv('DEFAULT_TIME_LIMIT', str(self.DEFAULT_TIME_LIMIT)))
        
        # 分页配置
        self.DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', str(self.DEFAULT_PAGE_SIZE)))
        
        # 日志配置
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # 资源加载器
        self.resource_loader = LocalResourceLoader(self.STATIC_PATH)
        
        self._validate_config()
    
    def _validate_config(self):
        """验证配置的有效性"""
        errors = []
        
        if not (self.MIN_QUESTION_COUNT <= self.DEFAULT_QUESTION_COUNT <= self.MAX_QUESTION_COUNT):
            errors.append(f"默认题目数量必须在{self.MIN_QUESTION_COUNT}和{self.MAX_QUESTION_COUNT}之间")
        
        if not (1 <= self.PORT <= 65535):
            errors.append(f"端口号必须在1-65535之间")
        
        if errors:
            error_msg = "配置验证失败:\n" + "\n".join(f"  - {e}" for e in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def check_local_resources(self) -> bool:
        """检查并创建必需的本地目录和静态资源"""
        required_dirs = [
            self.TEMPLATE_PATH,
            self.STATIC_PATH,
            os.path.join(self.STATIC_PATH, 'css'),
            os.path.join(self.STATIC_PATH, 'js'),
            os.path.join(self.STATIC_PATH, 'icons'),
            os.path.dirname(self.DB_PATH),
            self.LOG_DIR
        ]
        
        success = True
        for d in required_dirs:
            if not os.path.exists(d):
                try:
                    os.makedirs(d, exist_ok=True)
                    logger.info(f"创建目录: {d}")
                except Exception as e:
                    logger.error(f"创建目录失败 {d}: {e}")
                    success = False
        
        try:
            self.resource_loader.check_resource_exists()
            logger.info("静态资源检查通过")
        except FileNotFoundError as e:
            logger.error(f"静态资源检查失败: {e}")
            success = False
        
        if success:
            logger.info("本地资源检查完成")
        else:
            logger.warning("本地资源检查完成，但存在一些问题")
        
        return success
    
    def get_config(self) -> Dict[str, Any]:
        """获取所有配置项"""
        return {
            'BASE_DIR': self.BASE_DIR,
            'TEMPLATE_PATH': self.TEMPLATE_PATH,
            'STATIC_PATH': self.STATIC_PATH,
            'DB_PATH': self.DB_PATH,
            'LOG_DIR': self.LOG_DIR,
            'DEBUG': self.DEBUG,
            'HOST': self.HOST,
            'PORT': self.PORT,
            'DEFAULT_QUESTION_COUNT': self.DEFAULT_QUESTION_COUNT,
            'DEFAULT_TIME_LIMIT': self.DEFAULT_TIME_LIMIT,
            'DEFAULT_PAGE_SIZE': self.DEFAULT_PAGE_SIZE,
            'LOG_LEVEL': self.LOG_LEVEL
        }
    
    def get_paths(self) -> Dict[str, str]:
        """获取所有路径配置"""
        return {
            'base': self.BASE_DIR,
            'templates': self.TEMPLATE_PATH,
            'static': self.STATIC_PATH,
            'database': self.DB_PATH,
            'logs': self.LOG_DIR
        }
    
    def get_db_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return {
            'path': self.DB_PATH,
            'timeout': self.DB_TIMEOUT,
            'check_same_thread': self.DB_CHECK_SAME_THREAD
        }
    
    def is_debug_mode(self) -> bool:
        """检查是否处于调试模式"""
        return self.DEBUG
