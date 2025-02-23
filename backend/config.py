import os
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

# 環境変数の取得
DATABASE_URL = os.getenv("DATABASE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# 環境変数の確認（デバッグ用）
print(f"Database URL: {DATABASE_URL}")
print(f"AWS Access Key: {AWS_ACCESS_KEY_ID}")
print(f"AWS Secret Key: {AWS_SECRET_ACCESS_KEY}")
print(f"Secret Key: {SECRET_KEY}")
