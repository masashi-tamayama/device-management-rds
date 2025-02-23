import json
from common.db_interface import get_db_interface
import logging

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """デバイスを取得するLambda関数"""
    try:
        # パスパラメータからデバイスIDを取得
        device_id = event.get('pathParameters', {}).get('id')
        
        # データベース操作
        db = get_db_interface()
        
        if device_id:
            # 特定のデバイスを取得
            device = db.get_device(device_id)
            
            if device:
                return {
                    'statusCode': 200,
                    'body': json.dumps(device, default=str)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        'error': 'デバイスが見つかりません'
                    })
                }
        else:
            # 全デバイスを取得
            devices = db.list_devices()
            
            return {
                'statusCode': 200,
                'body': json.dumps(devices, default=str)
            }
            
    except Exception as e:
        logger.error(f"エラー: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error'
            })
        } 