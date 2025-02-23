import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# 既存の環境変数をクリア
os.environ.clear()

# テスト用の環境変数を設定
os.environ["DB_TYPE"] = "rds"
os.environ["DB_HOST"] = "127.0.0.1"
os.environ["DB_PORT"] = "3306"
os.environ["DB_USER"] = "root"
os.environ["DB_PASSWORD"] = "okitasouji"
os.environ["DB_NAME"] = "test_lambdadb"

from devices.database import Base
from devices.main import app
from fastapi.testclient import TestClient
from devices.common.db_pool import db_pool

# テスト用のデータベースURL
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@127.0.0.1:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

@pytest.fixture(scope="session")
def test_db():
    """テスト用データベースのセットアップとクリーンアップ"""
    # テスト用データベースの作成
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        connect_args={
            "charset": "utf8mb4",
            "use_unicode": True,
            "collation": "utf8mb4_unicode_ci",
            "auth_plugin": "mysql_native_password"
        }
    )
    
    # テーブルの作成
    Base.metadata.create_all(bind=engine)
    
    # テスト用セッションの作成
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield engine
    
    # テスト後のクリーンアップ
    Base.metadata.drop_all(bind=engine)
    db_pool.close_all_connections()

@pytest.fixture
def test_client():
    """テストクライアントを提供"""
    return TestClient(app)