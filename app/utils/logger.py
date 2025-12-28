# -*- coding: utf-8 -*-
"""
日志管理模块
提供完整的日志记录功能，支持文件日志、控制台日志、日志轮转等
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, 'interview_system.log')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'interview_system_error.log')
ACCESS_LOG_FILE = os.path.join(LOG_DIR, 'interview_system_access.log')


class Logger:
    """
    日志管理器类
    提供统一的日志记录接口，支持多级别日志、文件轮转、错误分离等功能
    
    功能特性：
    - 多级别日志记录
    - 文件和控制台双重输出
    - 日志文件轮转
    - 错误日志分离
    - 访问日志记录
    - 性能日志记录
    """
    
    _instances = {}
    
    def __init__(self, name: str = 'interview_system', level: str = 'INFO',
                 log_to_file: bool = True, log_to_console: bool = True,
                 max_bytes: int = 10 * 1024 * 1024, backup_count: int = 5):
        """
        初始化日志管理器
        
        Args:
            name: 日志器名称
            level: 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
            log_to_file: 是否记录到文件
            log_to_console: 是否输出到控制台
            max_bytes: 单个日志文件最大字节数
            backup_count: 保留的备份文件数量
        """
        self.name = name
        self.logger = logging.getLogger(name)
        
        # 设置日志级别
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # 避免重复添加处理器
        if self.logger.handlers:
            return
        
        # 日志格式
        detailed_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        simple_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 文件日志处理器（轮转）
        if log_to_file:
            # 主日志文件
            fh = RotatingFileHandler(
                LOG_FILE,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(detailed_format)
            self.logger.addHandler(fh)
            
            # 错误日志文件（只记录ERROR及以上级别）
            error_fh = RotatingFileHandler(
                ERROR_LOG_FILE,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            error_fh.setLevel(logging.ERROR)
            error_fh.setFormatter(detailed_format)
            self.logger.addHandler(error_fh)
        
        # 控制台日志处理器
        if log_to_console:
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(log_level)
            ch.setFormatter(simple_format)
            self.logger.addHandler(ch)
    
    def debug(self, msg: str, *args, **kwargs):
        """记录DEBUG级别日志"""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """记录INFO级别日志"""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """记录WARNING级别日志"""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """记录ERROR级别日志"""
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """记录CRITICAL级别日志"""
        self.logger.critical(msg, *args, **kwargs)
    
    def exception(self, msg: str, *args, exc_info=True, **kwargs):
        """记录异常信息"""
        self.logger.error(msg, *args, exc_info=exc_info, **kwargs)
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """
        记录性能日志
        
        Args:
            operation: 操作名称
            duration: 耗时（秒）
            **kwargs: 其他信息
        """
        extra_info = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
        msg = f"性能: {operation} 耗时 {duration:.4f}秒"
        if extra_info:
            msg += f", {extra_info}"
        self.info(msg)
    
    def log_access(self, method: str, path: str, status_code: int, 
                   duration: float, user_id: Optional[int] = None):
        """
        记录访问日志
        
        Args:
            method: HTTP方法
            path: 请求路径
            status_code: 状态码
            duration: 处理耗时（秒）
            user_id: 用户ID（可选）
        """
        user_info = f"用户ID={user_id}" if user_id else "匿名用户"
        self.info(f"访问: {method} {path} - {status_code} - {duration:.4f}秒 - {user_info}")
    
    @classmethod
    def get_logger(cls, name: str = 'interview_system', **kwargs):
        """
        获取日志器实例（单例模式）
        
        Args:
            name: 日志器名称
            **kwargs: 其他初始化参数
            
        Returns:
            Logger: 日志器实例
        """
        if name not in cls._instances:
            cls._instances[name] = cls(name, **kwargs)
        return cls._instances[name]
