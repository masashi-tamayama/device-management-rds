import os
import logging
from typing import Optional
import mysql.connector
from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from dotenv import load_dotenv
from .logger import setup_logger

# ロギングの設定
logger = setup_logger(__name__)

# 環境変数の読み込み
load_dotenv()

# データベース接続プールの設定
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'device_management'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'pool_name': 'device_management_pool',
    'pool_size': int(os.getenv('DB_POOL_SIZE', '5')),
    'pool_reset_session': True
}

# グローバル変数としてコネクションプールを保持
connection_pool: Optional[MySQLConnectionPool] = None

def initialize_connection_pool() -> None:
    """データベース接続プールを初期化する関数"""
    global connection_pool
    try:
        if connection_pool is None:
            connection_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_CONFIG)
            logger.info("データベース接続プールを初期化しました")
    except mysql.connector.Error as err:
        logger.error(f"接続プールの初期化エラー: {err}")
        raise

def get_db_connection() -> PooledMySQLConnection:
    """接続プールからデータベース接続を取得する関数"""
    global connection_pool
    try:
        if connection_pool is None:
            initialize_connection_pool()
        connection = connection_pool.get_connection()
        logger.debug("データベース接続を取得しました")
        return connection
    except mysql.connector.Error as err:
        logger.error(f"データベース接続エラー: {err}")
        raise
    except Exception as err:
        logger.error(f"予期せぬエラー: {err}")
        raise

def init_db() -> None:
    """データベースとテーブルを初期化する関数"""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # devicesテーブルの作成
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL COMMENT '機器名',
                manufacturer VARCHAR(255) NOT NULL COMMENT 'メーカー名',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_name (name),
                INDEX idx_manufacturer (manufacturer)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        connection.commit()
        logger.info("devicesテーブルを初期化しました")
    except mysql.connector.Error as err:
        logger.error(f"テーブル作成エラー: {err}")
        raise
    finally:
        cursor.close()
        connection.close()

def close_all_connections() -> None:
    """全ての接続を閉じる関数"""
    global connection_pool
    if connection_pool:
        try:
            # プール内の全ての接続を閉じる
            connection_pool._remove_connections()
            logger.info("全てのデータベース接続を閉じました")
        except Exception as err:
            logger.error(f"接続クローズエラー: {err}")
            raise
        finally:
            connection_pool = None