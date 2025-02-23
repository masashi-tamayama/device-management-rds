import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import logging
from typing import Dict, List, Optional
from .db_interface import DatabaseInterface

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数の読み込み
load_dotenv()

class DynamoDBInterface(DatabaseInterface):
    """DynamoDBを使用したデバイス管理クラス"""
    
    def __init__(self):
        """DynamoDBテーブルのリソースを初期化"""
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
            self.table = self.dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))
            logger.info(f"DynamoDBテーブル {os.getenv('DYNAMODB_TABLE_NAME')} に接続しました")
        except ClientError as e:
            logger.error(f"DynamoDB接続エラー: {e.response['Error']['Message']}")
            raise

    def create_device(self, device_data: Dict) -> Dict:
        """デバイスを作成する"""
        try:
            self.table.put_item(Item=device_data)
            logger.info(f"デバイスを作成しました: {device_data['id']}")
            return device_data
        except ClientError as e:
            logger.error(f"デバイス作成エラー: {e.response['Error']['Message']}")
            raise

    def get_device(self, device_id: str) -> Optional[Dict]:
        """デバイスを取得する"""
        try:
            response = self.table.get_item(Key={'id': device_id})
            device = response.get('Item')
            if device:
                logger.info(f"デバイスを取得しました: {device_id}")
            else:
                logger.info(f"デバイスが見つかりません: {device_id}")
            return device
        except ClientError as e:
            logger.error(f"デバイス取得エラー: {e.response['Error']['Message']}")
            raise

    def update_device(self, device_id: str, update_data: Dict) -> Optional[Dict]:
        """デバイスを更新する"""
        update_expression = "SET "
        expression_attribute_values = {}
        
        for key, value in update_data.items():
            if key != 'id':  # idは更新しない
                update_expression += f"#{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
        
        # 末尾のカンマとスペースを削除
        update_expression = update_expression[:-2]
        
        try:
            response = self.table.update_item(
                Key={'id': device_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames={f"#{k}": k for k in update_data.keys() if k != 'id'},
                ReturnValues="ALL_NEW"
            )
            updated_device = response.get('Attributes')
            logger.info(f"デバイスを更新しました: {device_id}")
            return updated_device
        except ClientError as e:
            logger.error(f"デバイス更新エラー: {e.response['Error']['Message']}")
            raise

    def delete_device(self, device_id: str) -> bool:
        """デバイスを削除する"""
        try:
            self.table.delete_item(Key={'id': device_id})
            logger.info(f"デバイスを削除しました: {device_id}")
            return True
        except ClientError as e:
            logger.error(f"デバイス削除エラー: {e.response['Error']['Message']}")
            raise

    def list_devices(self) -> List[Dict]:
        """全デバイスを取得する"""
        try:
            response = self.table.scan()
            devices = response.get('Items', [])
            logger.info(f"デバイス一覧を取得しました: {len(devices)}件")
            return devices
        except ClientError as e:
            logger.error(f"デバイス一覧取得エラー: {e.response['Error']['Message']}")
            raise
