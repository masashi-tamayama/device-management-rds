import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from devices.main import app
from devices.common.exceptions import DeviceNotFoundError, ValidationError, DatabaseError

client = TestClient(app)

def test_device_not_found_error():
    """存在しないデバイスへのアクセスで404エラーが返されることを確認"""
    response = client.get("/api/v1/devices/non-existent-id")
    assert response.status_code == 404
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "DEVICE_NOT_FOUND"
    assert "non-existent-id" in error_response["error"]["message"]

def test_validation_error_create_device():
    """デバイス作成時の入力バリデーションエラーを確認"""
    # 名前が空の場合
    response = client.post(
        "/api/v1/devices/",
        json={"name": "", "manufacturer": "テストメーカー"}
    )
    assert response.status_code == 400
    
    error_response = response.json()
    assert error_response["error"]["code"] == "VALIDATION_ERROR"
    assert "デバイス名は必須です" in error_response["error"]["message"]
    
    # メーカー名が空の場合
    response = client.post(
        "/api/v1/devices/",
        json={"name": "テストデバイス", "manufacturer": ""}
    )
    assert response.status_code == 400
    
    error_response = response.json()
    assert error_response["error"]["code"] == "VALIDATION_ERROR"
    assert "メーカー名は必須です" in error_response["error"]["message"]

def test_validation_error_update_device():
    """デバイス更新時の入力バリデーションエラーを確認"""
    response = client.put(
        "/api/v1/devices/test-id",
        json={"name": "", "manufacturer": "テストメーカー"}
    )
    assert response.status_code == 400
    
    error_response = response.json()
    assert error_response["error"]["code"] == "VALIDATION_ERROR"
    assert "デバイス名は必須です" in error_response["error"]["message"]

def test_successful_error_response_format():
    """エラーレスポンスの形式が正しいことを確認"""
    response = client.get("/api/v1/devices/non-existent-id")
    assert response.status_code == 404
    
    error_response = response.json()
    assert "error" in error_response
    assert "code" in error_response["error"]
    assert "message" in error_response["error"]
    assert "details" in error_response["error"] 