import json
import uuid
from common.db_interface import get_db_interface
import logging

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """デバイスを作成するLambda関数"""
    try:
        # リクエストボディの取得
        body = json.loads(event['body'])
        
        # 必須フィールドの検証
        required_fields = ['name', 'manufacturer']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': f'必須フィールドがありません: {field}'
                    })
                }
        
        # デバイスIDの生成
        device_id = str(uuid.uuid4())
        
        # デバイスデータの準備
        device_data = {
            'id': device_id,
            'name': body['name'],
            'manufacturer': body['manufacturer']
        }
        
        # データベース操作
        db = get_db_interface()
        created_device = db.create_device(device_data)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'デバイスを作成しました',
                'device': created_device
            })
        }
            
    except Exception as e:
        logger.error(f"エラー: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error'
            })
        } 