import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from dotenv import load_dotenv
import logging
import traceback

# ロガーの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 環境変数の読み込み
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
env_file = f".env.{ENVIRONMENT}"
load_dotenv(env_file)
logger.debug(f"Loading environment from: {env_file}")

# データベース接続情報
if ENVIRONMENT == "production":
    DB_HOST = os.getenv("RDS_HOST")
    DB_PORT = os.getenv("RDS_PORT", "3306")
    DB_USER = os.getenv("RDS_USER")
    DB_PASSWORD = os.getenv("RDS_PASSWORD")
    DB_NAME = os.getenv("RDS_DATABASE")
else:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "lambdadb")

# 接続情報をログ出力（パスワードは除く）
logger.debug(f"Environment: {ENVIRONMENT}")
logger.debug(f"Database connection info - Host: {DB_HOST}, Port: {DB_PORT}, User: {DB_USER}, Database: {DB_NAME}")

# SQLAlchemy用のデータベースURL
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4&collation=utf8mb4_unicode_ci"

try:
    # エンジンの作成
    logger.debug("Creating database engine...")
    engine = create_engine(
        DATABASE_URL,
        pool_recycle=3600,
        pool_pre_ping=True,
        echo=True,
        connect_args={
            "charset": "utf8mb4",
            "use_unicode": True,
            "collation": "utf8mb4_unicode_ci"
        }
    )
    logger.debug("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        # 接続テスト
        logger.debug("Testing database connection...")
        db.execute(text("SELECT 1"))
        logger.debug("Database connection successful")
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        db.close()
        raise HTTPException(
            status_code=500,
            detail={
                "message": "データベース接続エラーが発生しました",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        db.close()
        raise HTTPException(
            status_code=500,
            detail={
                "message": "予期せぬエラーが発生しました",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )
    finally:
        logger.debug("Closing database connection")
        db.close()