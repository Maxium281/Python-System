# -*- coding: utf-8 -*-
"""
数据库管理模块
提供数据库连接、查询、事务管理等功能
"""
import os
import sqlite3
import time
import threading
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
from datetime import datetime
from app.utils.logger import Logger

logger = Logger()


class DBManager:
    """数据库管理器类"""
    
    _lock = threading.Lock()
    _instances = {}
    
    def __init__(self, db_path: Optional[str] = None, timeout: int = 20, 
                 check_same_thread: bool = False, enable_wal: bool = True):
        """初始化数据库管理器"""
        if db_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            db_path = os.path.join(base_dir, 'database', 'interview.db')
        
        self.db_path = os.path.abspath(db_path)
        self.timeout = timeout
        self.check_same_thread = check_same_thread
        self.enable_wal = enable_wal
        
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        self._connect()
        self.query_count = 0
    
    def _connect(self):
        """建立数据库连接"""
        try:
            self.conn = sqlite3.connect(
                self.db_path,
                timeout=self.timeout,
                check_same_thread=self.check_same_thread
            )
            self.conn.row_factory = sqlite3.Row
            
            if self.enable_wal:
                try:
                    self.conn.execute('PRAGMA journal_mode=WAL;')
                    logger.info("已启用WAL模式")
                except Exception as e:
                    logger.warning(f"启用WAL模式失败: {e}")
            
            self.conn.execute('PRAGMA foreign_keys=ON;')
            self.conn.execute('PRAGMA synchronous=NORMAL;')
            self.conn.execute('PRAGMA cache_size=10000;')
            
            logger.info(f"数据库连接已建立: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def query(self, sql: str, params: Tuple = ()) -> sqlite3.Cursor:
        """执行查询语句"""
        start_time = time.time()
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params if params else ())
            self.query_count += 1
            elapsed = time.time() - start_time
            
            if elapsed > 1.0:
                logger.warning(f"慢查询检测: {elapsed:.2f}s - {sql[:100]}")
            
            return cur
        except sqlite3.Error as e:
            logger.error(f"查询执行失败: {e}\nSQL: {sql}\nParams: {params}")
            raise
    
    def execute(self, sql: str, params: Tuple = ()) -> sqlite3.Cursor:
        """执行更新语句（INSERT, UPDATE, DELETE）"""
        start_time = time.time()
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params if params else ())
            self.query_count += 1
            elapsed = time.time() - start_time
            
            if elapsed > 1.0:
                logger.warning(f"慢更新检测: {elapsed:.2f}s - {sql[:100]}")
            
            return cur
        except sqlite3.Error as e:
            logger.error(f"执行失败: {e}\nSQL: {sql}\nParams: {params}")
            raise
    
    def executemany(self, sql: str, params_list: List[Tuple]) -> sqlite3.Cursor:
        """批量执行SQL语句"""
        start_time = time.time()
        try:
            cur = self.conn.cursor()
            cur.executemany(sql, params_list)
            self.query_count += 1
            elapsed = time.time() - start_time
            
            logger.info(f"批量执行完成: {len(params_list)}条记录, 耗时{elapsed:.2f}s")
            return cur
        except sqlite3.Error as e:
            logger.error(f"批量执行失败: {e}\nSQL: {sql}")
            raise
    
    def commit(self):
        """提交事务"""
        try:
            self.conn.commit()
            logger.debug("事务已提交")
        except sqlite3.Error as e:
            logger.error(f"提交事务失败: {e}")
            raise
    
    def rollback(self):
        """回滚事务"""
        try:
            self.conn.rollback()
            logger.debug("事务已回滚")
        except sqlite3.Error as e:
            logger.error(f"回滚事务失败: {e}")
            raise
    
    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        try:
            yield self
            self.commit()
            logger.debug("事务成功完成")
        except Exception as e:
            self.rollback()
            logger.error(f"事务失败，已回滚: {e}")
            raise
    
    def fetchone(self, sql: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """执行查询并返回单条记录"""
        cur = self.query(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None
    
    def fetchall(self, sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """执行查询并返回所有记录"""
        cur = self.query(sql, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    
    def fetchmany(self, sql: str, params: Tuple = (), size: int = 100) -> List[Dict[str, Any]]:
        """执行查询并返回指定数量的记录"""
        cur = self.query(sql, params)
        rows = cur.fetchmany(size)
        return [dict(row) for row in rows]
    
    def get_count(self, table: str, where: str = '', params: Tuple = ()) -> int:
        """获取表中记录数量"""
        sql = f"SELECT COUNT(*) as count FROM {table}"
        if where:
            sql += f" WHERE {where}"
        result = self.fetchone(sql, params)
        return result['count'] if result else 0
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetchone(sql, (table_name,))
        return result is not None
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        return self.fetchall(f"PRAGMA table_info({table_name})")
    
    def get_all_tables(self) -> List[str]:
        """获取所有表名"""
        results = self.fetchall("SELECT name FROM sqlite_master WHERE type='table'")
        return [r['name'] for r in results]
    
    def backup(self, backup_path: Optional[str] = None) -> str:
        """备份数据库"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(os.path.dirname(self.db_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f'interview_backup_{timestamp}.db')
        
        try:
            backup_conn = sqlite3.connect(backup_path)
            self.conn.backup(backup_conn)
            backup_conn.close()
            
            logger.info(f"数据库备份完成: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"数据库备份失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
                logger.info("数据库连接已关闭")
        except Exception as e:
            logger.error(f"关闭数据库连接失败: {e}")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
    
    def __del__(self):
        """析构函数"""
        try:
            self.close()
        except Exception:
            pass
