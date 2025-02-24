from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from .handlers import device_handlers
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from .common.exceptions import DeviceManagementError
from .common.error_handlers import device_management_exception_handler, general_exception_handler
from sqlalchemy import text
from .database import get_db

class UnicodeJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(",", ": ")
        ).encode("utf-8")

    def init_headers(self, headers: dict = None) -> dict:
        headers = super().init_headers(headers)
        headers["Content-Type"] = "application/json; charset=utf-8"
        return headers

app = FastAPI(
    title="Device Management API",
    description="機器管理システムのバックエンドAPI",
    version="1.0.0",
    default_response_class=UnicodeJSONResponse
)

# エラーハンドラーの登録
app.add_exception_handler(DeviceManagementError, device_management_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(device_handlers.router, prefix="/api/v1")

# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "Device Management API"}

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    try:
        # データベース接続テスト
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

# AWS Lambda用ハンドラー
handler = Mangum(app) 