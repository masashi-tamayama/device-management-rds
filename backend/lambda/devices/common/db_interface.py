import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DatabaseInterface(ABC):
    """データベース操作の抽象クラス"""
    
    @abstractmethod
    def create_device(self, device_data: Dict) -> Dict:
        """デバイスを作成する"""
        pass
    
    @abstractmethod
    def get_device(self, device_id: str) -> Optional[Dict]:
        """デバイスを取得する"""
        pass
    
    @abstractmethod
    def update_device(self, device_id: str, device_data: Dict) -> Optional[Dict]:
        """デバイスを更新する"""
        pass
    
    @abstractmethod
    def delete_device(self, device_id: str) -> bool:
        """デバイスを削除する"""
        pass
    
    @abstractmethod
    def list_devices(self) -> List[Dict]:
        """全デバイスを取得する"""
        pass

def get_db_interface() -> DatabaseInterface:
    """
    環境変数に基づいて適切なデータベースインターフェースを返す
    DB_TYPE環境変数が 'dynamodb' の場合はDynamoDB、それ以外の場合はRDSを使用
    """
    db_type = os.getenv('DB_TYPE', 'rds').lower()
    
    if db_type == 'dynamodb':
        from .dynamodb import DynamoDBInterface
        logger.info("Using DynamoDB interface")
        return DynamoDBInterface()
    else:
        from .rds import RDSInterface
        logger.info("Using RDS interface")
        return RDSInterface() 