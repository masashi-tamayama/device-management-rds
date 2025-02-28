import os
import sys
import logging
import platform
import traceback

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# システム情報の出力
logger.debug("=== System Information ===")
logger.debug(f"Python Version: {platform.python_version()}")
logger.debug(f"Platform: {platform.platform()}")
logger.debug(f"Working Directory: {os.getcwd()}")

# プロジェクトルートの絶対パスを取得
LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', '')
if not LAMBDA_TASK_ROOT:
    LAMBDA_TASK_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# パッケージのルートディレクトリを特定
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 必要なパスをsys.pathに追加（優先順位順）
paths = [
    os.path.dirname(os.path.abspath(__file__)),  # devicesディレクトリ
    LAMBDA_TASK_ROOT,  # プロジェクトルート
    os.path.join(LAMBDA_TASK_ROOT, "devices"),  # devicesパッケージ
    os.getcwd(),  # カレントディレクトリ
]

for path in paths:
    if path and path not in sys.path:
        sys.path.insert(0, path)
        logger.debug(f"Added to sys.path: {path}")

# デバッグ情報の出力
logger.debug("=== Directory Structure ===")
logger.debug(f"Current File: {__file__}")
logger.debug(f"sys.path: {sys.path}")
logger.debug(f"Current Directory Contents: {os.listdir(os.getcwd())}")
if os.path.exists(LAMBDA_TASK_ROOT):
    logger.debug(f"LAMBDA_TASK_ROOT Contents: {os.listdir(LAMBDA_TASK_ROOT)}")

# モジュールの可用性チェック
logger.debug("=== Module Availability Check ===")
try:
    from devices.handlers import device_handlers
    logger.debug("✓ Successfully imported device_handlers")
except ImportError as e:
    logger.error(f"Failed to import device_handlers: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")

try:
    import fastapi
    logger.debug(f"✓ FastAPI Version: {fastapi.__version__}")
except ImportError as e:
    logger.error(f"FastAPI import error: {e}")

try:
    import mangum
    logger.debug("✓ Mangum imported successfully")
except ImportError as e:
    logger.error(f"Mangum import error: {e}")

try:
    import sqlalchemy
    logger.debug(f"✓ SQLAlchemy Version: {sqlalchemy.__version__}")
except ImportError as e:
    logger.error(f"SQLAlchemy import error: {e}")
