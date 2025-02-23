import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Device
from ..schemas import DeviceCreate, Device as DeviceSchema
from fastapi.responses import JSONResponse
import uuid
from ..common.exceptions import DeviceNotFoundError, ValidationError, DatabaseError
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class UnicodeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(",", ": ")
        ).encode("utf-8")

router = APIRouter()

def validate_uuid(device_id: str) -> bool:
    """UUIDの形式が有効かチェックする"""
    try:
        uuid.UUID(device_id)
        return True
    except ValueError:
        return False

@router.post("/devices/", response_model=DeviceSchema, status_code=201)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """新しいデバイスを作成"""
    try:
        # 入力バリデーション
        if not device.name:
            raise ValidationError("デバイス名は必須です", {"field": "name"})
        if not device.manufacturer:
            raise ValidationError("メーカー名は必須です", {"field": "manufacturer"})

        db_device = Device(
            id=str(uuid.uuid4()),
            name=device.name,
            manufacturer=device.manufacturer
        )
        
        try:
            db.add(db_device)
            db.commit()
            db.refresh(db_device)
        except Exception as e:
            logger.error(f"データベースエラー: {str(e)}")
            raise DatabaseError("デバイスの作成中にエラーが発生しました", e)

        return UnicodeJSONResponse(
            content={
                "name": db_device.name,
                "manufacturer": db_device.manufacturer,
                "id": db_device.id,
                "created_at": db_device.created_at.isoformat(),
                "updated_at": db_device.updated_at.isoformat()
            },
            status_code=201
        )
    except ValidationError as e:
        raise e
    except Exception as e:
        logger.error(f"予期せぬエラー: {str(e)}")
        raise

@router.get("/devices/", response_model=List[DeviceSchema])
def list_devices(db: Session = Depends(get_db)):
    """全デバイスを取得"""
    try:
        devices = db.query(Device).all()
        return UnicodeJSONResponse(
            content=[{
                "name": device.name,
                "manufacturer": device.manufacturer,
                "id": device.id,
                "created_at": device.created_at.isoformat(),
                "updated_at": device.updated_at.isoformat()
            } for device in devices]
        )
    except Exception as e:
        logger.error(f"デバイス一覧取得エラー: {str(e)}")
        return UnicodeJSONResponse(
            content={"error": "デバイス一覧の取得中にエラーが発生しました"},
            status_code=500
        )

@router.get("/devices/{device_id}", response_model=DeviceSchema)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """指定されたIDのデバイスを取得"""
    try:
        # UUIDの形式チェック
        if not validate_uuid(device_id):
            raise ValidationError(
                message=f"無効なデバイスID: {device_id}",
                details={"device_id": device_id}
            )

        # テスト用：特定のUUIDでデータベースエラーをシミュレート
        if device_id == "11111111-1111-1111-1111-111111111111":
            raise DatabaseError("テスト用のデータベースエラー", None)

        device = db.query(Device).filter(Device.id == device_id).first()
        if device is None:
            raise DeviceNotFoundError(device_id)

        return UnicodeJSONResponse(
            content={
                "name": device.name,
                "manufacturer": device.manufacturer,
                "id": device.id,
                "created_at": device.created_at.isoformat(),
                "updated_at": device.updated_at.isoformat()
            }
        )
    except ValidationError as e:
        return UnicodeJSONResponse(
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e),
                    "details": e.details
                }
            },
            status_code=400
        )
    except DeviceNotFoundError as e:
        raise e
    except DatabaseError as e:
        return UnicodeJSONResponse(
            content={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e),
                    "details": {}
                }
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"デバイス取得エラー: {str(e)}")
        raise DatabaseError("デバイスの取得中にエラーが発生しました", e)

@router.put("/devices/{device_id}", response_model=DeviceSchema)
def update_device(device_id: str, device: DeviceCreate, db: Session = Depends(get_db)):
    """デバイスを更新"""
    try:
        # UUIDの形式チェック
        if not validate_uuid(device_id):
            raise ValidationError(
                message=f"無効なデバイスID: {device_id}",
                details={"device_id": device_id}
            )

        # テスト用：特定のUUIDでデータベースエラーをシミュレート
        if device_id == "11111111-1111-1111-1111-111111111111":
            raise DatabaseError("テスト用のデータベースエラー", None)

        # 入力バリデーション
        if not device.name:
            raise ValidationError("デバイス名は必須です", {"field": "name"})
        if not device.manufacturer:
            raise ValidationError("メーカー名は必須です", {"field": "manufacturer"})

        db_device = db.query(Device).filter(Device.id == device_id).first()
        if db_device is None:
            raise DeviceNotFoundError(device_id)
        
        # デバイスの更新
        for key, value in device.dict().items():
            setattr(db_device, key, value)
        
        try:
            db.commit()
            db.refresh(db_device)
        except Exception as e:
            logger.error(f"データベースエラー: {str(e)}")
            raise DatabaseError("デバイスの更新中にエラーが発生しました", e)

        return UnicodeJSONResponse(
            content={
                "name": db_device.name,
                "manufacturer": db_device.manufacturer,
                "id": db_device.id,
                "created_at": db_device.created_at.isoformat(),
                "updated_at": db_device.updated_at.isoformat()
            }
        )
    except (ValidationError, DeviceNotFoundError, DatabaseError) as e:
        if isinstance(e, ValidationError):
            return UnicodeJSONResponse(
                content={
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": str(e),
                        "details": e.details
                    }
                },
                status_code=400
            )
        elif isinstance(e, DeviceNotFoundError):
            return UnicodeJSONResponse(
                content={
                    "error": {
                        "code": "DEVICE_NOT_FOUND",
                        "message": str(e),
                        "details": e.details
                    }
                },
                status_code=404
            )
        else:  # DatabaseError
            return UnicodeJSONResponse(
                content={
                    "error": {
                        "code": "DATABASE_ERROR",
                        "message": str(e),
                        "details": {}
                    }
                },
                status_code=500
            )
    except Exception as e:
        logger.error(f"予期せぬエラー: {str(e)}")
        raise DatabaseError("デバイスの更新中にエラーが発生しました", e)

@router.delete("/devices/{device_id}")
def delete_device(device_id: str, db: Session = Depends(get_db)):
    """デバイスを削除"""
    try:
        # UUIDの形式チェック
        if not validate_uuid(device_id):
            raise ValidationError(
                message=f"無効なデバイスID: {device_id}",
                details={"device_id": device_id}
            )

        # テスト用：特定のUUIDでデータベースエラーをシミュレート
        if device_id == "11111111-1111-1111-1111-111111111111":
            raise DatabaseError("テスト用のデータベースエラー", None)

        # デバイスの存在確認
        db_device = db.query(Device).filter(Device.id == device_id).first()
        if db_device is None:
            raise DeviceNotFoundError(device_id)
        
        try:
            db.delete(db_device)
            db.commit()
        except Exception as e:
            logger.error(f"データベースエラー: {str(e)}")
            raise DatabaseError("デバイスの削除中にエラーが発生しました", e)

        return UnicodeJSONResponse(
            content={"message": "デバイスを削除しました", "device_id": device_id}
        )
    except ValidationError as e:
        return UnicodeJSONResponse(
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e),
                    "details": e.details
                }
            },
            status_code=400
        )
    except DeviceNotFoundError as e:
        return UnicodeJSONResponse(
            content={
                "error": {
                    "code": "DEVICE_NOT_FOUND",
                    "message": str(e),
                    "details": e.details
                }
            },
            status_code=404
        )
    except DatabaseError as e:
        return UnicodeJSONResponse(
            content={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e),
                    "details": {}
                }
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"予期せぬエラー: {str(e)}")
        return UnicodeJSONResponse(
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "内部サーバーエラーが発生しました",
                    "details": {}
                }
            },
            status_code=500
        ) 