import json
from common.db_interface import get_db_interface
import logging

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """デバイスを削除するLambda関数"""
    try:
        # パスパラメータからデバイスIDを取得
        device_id = event['pathParameters']['id']
        
        # データベース操作
        db = get_db_interface()
        
        # デバイスの存在確認
        existing_device = db.get_device(device_id)
        if not existing_device:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'デバイスが見つかりません'
                })
            }
        
        # デバイスの削除
        db.delete_device(device_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'デバイスを削除しました',
                'device_id': device_id
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