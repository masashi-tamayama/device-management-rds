#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from devices.database import engine, Base
from devices.models import Device

def create_tables():
    """データベーステーブルを作成"""
    print("テーブルを作成しています...")
    try:
        Base.metadata.create_all(bind=engine)
        print("テーブルの作成が完了しました")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    create_tables() 