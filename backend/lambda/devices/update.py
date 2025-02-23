import json
from common.db_interface import get_db_interface
import logging

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """デバイスを更新するLambda関数"""
    try:
        # パスパラメータからデバイスIDを取得
        device_id = event['pathParameters']['id']
        
        # リクエストボディの取得
        body = json.loads(event['body'])
        
        # 更新可能なフィールド
        allowed_fields = ['name', 'manufacturer']
        update_data = {k: v for k, v in body.items() if k in allowed_fields}
        
        if not update_data:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': '更新可能なフィールドがありません'
                })
            }
        
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
        
        # デバイスの更新
        updated_device = db.update_device(device_id, update_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'デバイスを更新しました',
                'device': updated_device
            }, default=str)
        }
            
    except Exception as e:
        logger.error(f"エラー: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error'
            })
        } 