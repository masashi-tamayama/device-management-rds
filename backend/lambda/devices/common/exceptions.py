from typing import Any, Dict, Optional

class DeviceManagementError(Exception):
    """基本となるカスタム例外クラス"""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

class DeviceNotFoundError(DeviceManagementError):
    """デバイスが見つからない場合の例外"""
    def __init__(self, device_id: str):
        super().__init__(
            message=f"デバイスが見つかりません: {device_id}",
            status_code=404,
            error_code="DEVICE_NOT_FOUND",
            details={"device_id": device_id}
        )

class ValidationError(DeviceManagementError):
    """入力バリデーションエラーの例外"""
    def __init__(self, message: str, details: Dict[str, Any]):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=details
        )

class DatabaseError(DeviceManagementError):
    """データベース操作エラーの例外"""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        details = {"original_error": str(original_error)} if original_error else {}
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
            details=details
        ) 