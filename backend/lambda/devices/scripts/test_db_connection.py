import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List
import logging

# プロジェクトルートへのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from devices.common.db import get_db_connection, initialize_connection_pool, close_all_connections
from devices.common.logger import setup_logger

# ロガーの設定
logger = setup_logger(__name__)

def test_single_connection():
    """単一の接続テスト"""
    try:
        # 接続の取得
        connection = get_db_connection()
        logger.info("接続の取得に成功しました")

        # テストクエリの実行
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        logger.info(f"テストクエリの結果: {result}")

        # 接続のクリーンアップ
        cursor.close()
        connection.close()
        logger.info("接続を正常にクローズしました")
        return True
    except Exception as e:
        logger.error(f"接続テストエラー: {e}")
        return False

def test_multiple_connections(num_connections: int = 3) -> List[bool]:
    """複数の同時接続テスト

    Args:
        num_connections: テストする同時接続数

    Returns:
        List[bool]: 各接続のテスト結果
    """
    with ThreadPoolExecutor(max_workers=num_connections) as executor:
        results = list(executor.map(lambda _: test_single_connection(), range(num_connections)))
    return results

def main():
    """メイン実行関数"""
    try:
        logger.info("データベース接続テストを開始します")

        # 接続プールの初期化
        initialize_connection_pool()
        logger.info("接続プールの初期化が完了しました")

        # 単一接続のテスト
        logger.info("単一接続テストを実行します")
        if test_single_connection():
            logger.info("単一接続テストが成功しました")
        else:
            logger.error("単一接続テストが失敗しました")

        # 複数同時接続のテスト
        logger.info("複数同時接続テストを実行します")
        results = test_multiple_connections()
        success_count = sum(results)
        logger.info(f"同時接続テスト結果: 成功 {success_count}/{len(results)}")

        # 全ての接続をクローズ
        close_all_connections()
        logger.info("全ての接続をクローズしました")

    except Exception as e:
        logger.error(f"テスト実行中にエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 