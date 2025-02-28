#!/usr/bin/env python3
import os
import json
import boto3
import time
from botocore.exceptions import ClientError

def deploy_lambda():
    # 設定ファイルの読み込み
    with open('deploy-config.json', 'r') as f:
        config = json.load(f)

    # AWS クライアントの初期化
    s3 = boto3.client('s3')
    lambda_client = boto3.client('lambda')
    
    # S3バケット名（一時的なアップロード用）
    bucket_name = 'device-management-lambda-deploy'
    zip_file = '../function.zip'
    s3_key = 'function.zip'

    try:
        # S3バケットの存在確認、なければ作成
        try:
            s3.head_bucket(Bucket=bucket_name)
        except ClientError:
            print(f"バケット {bucket_name} を作成します...")
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'}
            )

        # ZIPファイルをS3にアップロード
        print("デプロイパッケージをS3にアップロードしています...")
        s3.upload_file(zip_file, bucket_name, s3_key)

        # Lambda関数の存在確認
        try:
            lambda_client.get_function(FunctionName=config['FunctionName'])
            # 関数が存在する場合は更新
            print(f"Lambda関数 {config['FunctionName']} を更新します...")
            response = lambda_client.update_function_code(
                FunctionName=config['FunctionName'],
                S3Bucket=bucket_name,
                S3Key=s3_key
            )
            
            # コードの更新完了を待機
            print("コードの更新完了を待機しています...")
            waiter = lambda_client.get_waiter('function_updated')
            waiter.wait(
                FunctionName=config['FunctionName'],
                WaiterConfig={'Delay': 5, 'MaxAttempts': 60}
            )
            
            # 設定を更新
            print("Lambda関数の設定を更新します...")
            lambda_client.update_function_configuration(
                FunctionName=config['FunctionName'],
                Runtime=config['Runtime'],
                Handler=config['Handler'],
                Timeout=config['Timeout'],
                MemorySize=config['MemorySize'],
                Environment=config['Environment'],
                VpcConfig=config['VpcConfig']
            )
            
            # 設定の更新完了を待機
            print("設定の更新完了を待機しています...")
            waiter = lambda_client.get_waiter('function_updated')
            waiter.wait(
                FunctionName=config['FunctionName'],
                WaiterConfig={'Delay': 5, 'MaxAttempts': 60}
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                # 関数が存在しない場合は新規作成
                print(f"Lambda関数 {config['FunctionName']} を作成します...")
                with open('.env', 'r') as f:
                    env_vars = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

                response = lambda_client.create_function(
                    FunctionName=config['FunctionName'],
                    Runtime=config['Runtime'],
                    Handler=config['Handler'],
                    Role=env_vars['LAMBDA_ROLE_ARN'],
                    Code={
                        'S3Bucket': bucket_name,
                        'S3Key': s3_key
                    },
                    Timeout=config['Timeout'],
                    MemorySize=config['MemorySize'],
                    Environment={
                        'Variables': config['Environment']['Variables']
                    }
                )
            else:
                raise

        # デプロイ状態の確認
        print("デプロイ状態を確認しています...")
        for _ in range(30):  # 最大30秒待機
            status = lambda_client.get_function(
                FunctionName=config['FunctionName']
            )['Configuration']['State']
            
            if status == 'Active':
                print("デプロイが完了しました！")
                break
            elif status == 'Failed':
                raise Exception("デプロイに失敗しました")
            
            time.sleep(1)

        # S3の一時ファイルを削除
        print("一時ファイルを削除しています...")
        s3.delete_object(Bucket=bucket_name, Key=s3_key)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    deploy_lambda() 