import logging
import os
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """ロガーを設定する関数

    Args:
        name: ロガー名（Noneの場合はルートロガーを設定）

    Returns:
        設定されたロガーインスタンス
    """
    # ロガーの取得
    logger = logging.getLogger(name)
    
    # 既に設定済みの場合は既存のロガーを返す
    if logger.handlers:
        return logger
    
    # ログレベルの設定
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logger.setLevel(getattr(logging, log_level))
    
    # ハンドラーの設定
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    
    # フォーマッターの設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # ハンドラーの追加
    logger.addHandler(handler)
    
    return logger 