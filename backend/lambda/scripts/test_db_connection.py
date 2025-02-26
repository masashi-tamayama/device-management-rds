#!/usr/bin/env python3
import os
import mysql.connector
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# データベース接続情報
config = {
    'host': os.getenv('RDS_HOST'),
    'user': os.getenv('RDS_USER'),
    'password': os.getenv('RDS_PASSWORD'),
    'database': os.getenv('RDS_DATABASE'),
    'port': os.getenv('RDS_PORT')
}

print("接続情報:")
print(f"Host: {config['host']}")
print(f"Port: {config['port']}")
print(f"Database: {config['database']}")
print(f"User: {config['user']}")

try:
    print("\nデータベースに接続しています...")
    conn = mysql.connector.connect(**config)
    print("接続成功!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"テストクエリ結果: {result}")
    
    cursor.close()
    conn.close()
    print("接続を閉じました")
except Exception as e:
    print(f"エラーが発生しました: {str(e)}") 