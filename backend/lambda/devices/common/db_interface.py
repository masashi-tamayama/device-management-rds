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
    RDSインターフェースを返す
    """
    from .rds import RDSInterface
    logger.info("Using RDS interface")
    return RDSInterface() 