from fastapi import Request
from fastapi.responses import JSONResponse
import logging
from .exceptions import DeviceManagementError

# ロガーの設定
logger = logging.getLogger(__name__)

async def device_management_exception_handler(
    request: Request,
    exc: DeviceManagementError
) -> JSONResponse:
    """カスタム例外のハンドラー"""
    logger.error(
        f"エラーが発生しました - コード: {exc.error_code}, "
        f"メッセージ: {exc.message}, "
        f"詳細: {exc.details}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """一般的な例外のハンドラー"""
    logger.error(f"予期せぬエラーが発生しました: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error"
        }
    ) 