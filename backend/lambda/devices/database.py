import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from dotenv import load_dotenv
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

# 環境変数の読み込み
load_dotenv()

# データベース接続情報
DB_TYPE = os.getenv("DB_TYPE", "rds")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "lambdadb")

# SQLAlchemy用のデータベースURL
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4&collation=utf8mb4_unicode_ci"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
        "collation": "utf8mb4_unicode_ci"
    }
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        # 接続テスト
        db.execute(text("SELECT 1"))
        yield db
    except SQLAlchemyError as e:
        logger.error(f"データベース接続エラー: {str(e)}")
        db.close()
        raise HTTPException(status_code=500, detail="データベース接続エラーが発生しました")
    finally:
        db.close()