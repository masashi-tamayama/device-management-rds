import os
import uuid
import logging
from typing import Dict, List, Optional
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
from .db_interface import DatabaseInterface

# 環境変数の読み込み
load_dotenv()

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class RDSInterface(DatabaseInterface):
    """RDS（MySQL）インターフェースの実装クラス"""
    
    def __init__(self):
        """データベース接続の初期化"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('RDS_HOST'),
                user=os.getenv('RDS_USER'),
                password=os.getenv('RDS_PASSWORD'),
                database=os.getenv('RDS_DATABASE'),
                port=int(os.getenv('RDS_PORT', '3306'))
            )
            self.connection.autocommit = True
            logger.info(f"RDSデータベース {os.getenv('RDS_DATABASE')} に接続しました")
        except mysql.connector.Error as e:
            logger.error(f"データベース接続エラー: {str(e)}")
            raise

    def _get_cursor(self):
        """カーソルを取得し、必要に応じて再接続する"""
        try:
            self.connection.ping(reconnect=True, attempts=3, delay=5)
            return self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            logger.error(f"データベース接続エラー: {str(e)}")
            raise

    def create_device(self, device_data: Dict) -> Dict:
        """デバイスを作成する"""
        cursor = self._get_cursor()
        try:
            device_id = str(uuid.uuid4())
            now = datetime.utcnow()
            
            query = """
                INSERT INTO devices (id, name, manufacturer, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                device_id,
                device_data['name'],
                device_data['manufacturer'],
                now,
                now
            ))
            self.connection.commit()
            
            # 作成したデバイスを取得して返す
            return self.get_device(device_id)
        except mysql.connector.Error as e:
            logger.error(f"デバイス作成エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def get_device(self, device_id: str) -> Optional[Dict]:
        """デバイスを取得する"""
        cursor = self._get_cursor()
        try:
            query = "SELECT * FROM devices WHERE id = %s"
            cursor.execute(query, (device_id,))
            device = cursor.fetchone()
            if device:
                logger.info(f"デバイスを取得しました: {device_id}")
            else:
                logger.info(f"デバイスが見つかりません: {device_id}")
            return device
        except mysql.connector.Error as e:
            logger.error(f"デバイス取得エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def update_device(self, device_id: str, update_data: Dict) -> Optional[Dict]:
        """デバイスを更新する"""
        cursor = self._get_cursor()
        try:
            # 更新可能なフィールドを指定
            allowed_fields = ['name', 'manufacturer']
            update_fields = {k: v for k, v in update_data.items() if k in allowed_fields}
            
            if not update_fields:
                logger.warning(f"更新可能なフィールドがありません: {device_id}")
                return None
            
            # UPDATE文の構築
            set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
            query = f"UPDATE devices SET {set_clause}, updated_at = %s WHERE id = %s"
            
            # パラメータの準備
            params = list(update_fields.values()) + [datetime.utcnow(), device_id]
            
            # 更新の実行
            cursor.execute(query, params)
            self.connection.commit()
            
            # 更新後のデータを取得して返す
            return self.get_device(device_id)
        except mysql.connector.Error as e:
            logger.error(f"デバイス更新エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def delete_device(self, device_id: str) -> bool:
        """デバイスを削除する"""
        cursor = self._get_cursor()
        try:
            query = "DELETE FROM devices WHERE id = %s"
            cursor.execute(query, (device_id,))
            self.connection.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"デバイスを削除しました: {device_id}")
            else:
                logger.info(f"削除対象のデバイスが見つかりません: {device_id}")
            return deleted
        except mysql.connector.Error as e:
            logger.error(f"デバイス削除エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def list_devices(self) -> List[Dict]:
        """全デバイスを取得する"""
        cursor = self._get_cursor()
        try:
            query = "SELECT * FROM devices"
            cursor.execute(query)
            devices = cursor.fetchall()
            logger.info(f"デバイス一覧を取得しました: {len(devices)}件")
            return devices
        except mysql.connector.Error as e:
            logger.error(f"デバイス一覧取得エラー: {str(e)}")
            raise
        finally:
            cursor.close()

    def __del__(self):
        """デストラクタ：接続のクリーンアップ"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            logger.info("データベース接続を閉じました") 