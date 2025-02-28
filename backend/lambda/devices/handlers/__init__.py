import os
import sys
import logging

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# カレントディレクトリとdevicesディレクトリのパスを取得
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
DEVICES_DIR = os.path.join(PROJECT_ROOT, "devices")

# Lambda実行環境のルートパスを設定
LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', PROJECT_ROOT)

# 必要なパスをsys.pathに追加（優先順位順）
paths = [
    CURRENT_DIR,                    # handlersディレクトリ
    os.path.dirname(CURRENT_DIR),   # devicesディレクトリ
    PROJECT_ROOT,                   # プロジェクトルート
    LAMBDA_TASK_ROOT,              # Lambda実行環境のルート
]

# パスを追加（存在チェック付き）
for path in paths:
    if path and path not in sys.path:
        sys.path.insert(0, path)
        logger.debug(f"Added to sys.path: {path}")

# デバッグ情報の出力
logger.debug("=== Handlers Package Configuration ===")
logger.debug(f"Current File: {__file__}")
logger.debug(f"Current Directory: {CURRENT_DIR}")
logger.debug(f"Project Root: {PROJECT_ROOT}")
logger.debug(f"Devices Directory: {DEVICES_DIR}")
logger.debug(f"Lambda Task Root: {LAMBDA_TASK_ROOT}")
logger.debug(f"Python Path: {sys.path}")

# 親モジュールのインポートを確認
try:
    from devices import models
    from devices import schemas
    from devices import database
    logger.debug("✓ Parent modules imported successfully")
except ImportError as e:
    logger.error(f"Failed to import parent modules: {str(e)}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise
