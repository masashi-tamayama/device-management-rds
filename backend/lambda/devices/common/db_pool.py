import os
from typing import Optional
import mysql.connector
from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from dotenv import load_dotenv
from .logger import setup_logger

# ロガーの設定
logger = setup_logger(__name__)

# 環境変数の読み込み
load_dotenv()

class DatabaseConnectionPool:
    """データベース接続プールを管理するクラス"""
    
    _instance: Optional['DatabaseConnectionPool'] = None
    _pool: Optional[MySQLConnectionPool] = None
    
    def __new__(cls):
        """シングルトンパターンの実装"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnectionPool, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """接続プールの設定を初期化"""
        if self._pool is None:
            self._initialize_pool()
    
    def _initialize_pool(self) -> None:
        """接続プールを初期化"""
        try:
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', '3306')),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', ''),
                'database': os.getenv('DB_NAME', 'lambdadb'),
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_unicode_ci',
                'pool_name': 'device_management_pool',
                'pool_size': int(os.getenv('DB_POOL_SIZE', '5')),
                'pool_reset_session': True,
                'auth_plugin': 'mysql_native_password',
                'connect_timeout': 10,
                'connection_timeout': 10
            }
            
            self._pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)
            logger.info("データベース接続プールを初期化しました")
        except mysql.connector.Error as err:
            logger.error(f"接続プールの初期化エラー: {err}")
            raise
    
    def get_connection(self) -> PooledMySQLConnection:
        """プールから接続を取得"""
        try:
            if self._pool is None:
                self._initialize_pool()
            connection = self._pool.get_connection()
            logger.debug("データベース接続を取得しました")
            return connection
        except mysql.connector.Error as err:
            logger.error(f"データベース接続エラー: {err}")
            raise
        except Exception as err:
            logger.error(f"予期せぬエラー: {err}")
            raise
    
    def close_all_connections(self) -> None:
        """全ての接続を閉じる"""
        try:
            if self._pool:
                self._pool._remove_connections()
                logger.info("全てのデータベース接続を閉じました")
        except Exception as err:
            logger.error(f"接続クローズエラー: {err}")
            raise
        finally:
            self._pool = None

# グローバルなインスタンスを作成
db_pool = DatabaseConnectionPool() 