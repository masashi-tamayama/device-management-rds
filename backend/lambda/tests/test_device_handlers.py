import pytest
from fastapi.testclient import TestClient
from datetime import datetime, UTC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from devices.main import app
from devices.models import Device
from devices.database import Base, get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_database(test_db):
    """各テストの前にデータベースをクリーンアップ"""
    Base.metadata.drop_all(bind=test_db)
    Base.metadata.create_all(bind=test_db)
    yield

def test_list_devices_empty(test_db):
    """デバイスが存在しない場合のテスト"""
    response = client.get("/api/v1/devices/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_devices_with_data(test_db):
    """デバイスが存在する場合のテスト"""
    # テストデータの作成
    test_devices = [
        Device(
            id="test-device-1",
            name="テストデバイス1",
            manufacturer="テストメーカー1"
        ),
        Device(
            id="test-device-2",
            name="テストデバイス2",
            manufacturer="テストメーカー2"
        )
    ]
    
    # テストデータの保存
    with test_db.connect() as connection:
        for device in test_devices:
            connection.execute(Device.__table__.insert().values(
                id=device.id,
                name=device.name,
                manufacturer=device.manufacturer,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            ))
        connection.commit()
    
    # APIリクエスト
    response = client.get("/api/v1/devices/")
    assert response.status_code == 200
    
    # レスポンスの検証
    devices = response.json()
    assert len(devices) == 2
    assert devices[0]["name"] == "テストデバイス1"
    assert devices[0]["manufacturer"] == "テストメーカー1"
    assert devices[1]["name"] == "テストデバイス2"
    assert devices[1]["manufacturer"] == "テストメーカー2"

def test_list_devices_error_handling(test_db):
    """エラーハンドリングのテスト"""
    # 無効なデータベースエンジンを作成
    invalid_engine = create_engine("mysql+mysqlconnector://invalid:invalid@invalid_host:3306/invalid_db")
    invalid_session = sessionmaker(autocommit=False, autoflush=False, bind=invalid_engine)
    
    # 無効なセッションを使用するようにアプリケーションを設定
    def override_get_db():
        db = invalid_session()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.get("/api/v1/devices/")
        assert response.status_code == 500
        assert "error" in response.json()
    finally:
        # 依存関係の上書きをクリア
        app.dependency_overrides.clear()

def test_create_device_success(test_db):
    """新しい機器の登録が成功するケースのテスト"""
    device_data = {
        "name": "新規テスト機器",
        "manufacturer": "新規テストメーカー"
    }
    
    response = client.post("/api/v1/devices/", json=device_data)
    assert response.status_code == 201
    
    created_device = response.json()
    assert created_device["name"] == device_data["name"]
    assert created_device["manufacturer"] == device_data["manufacturer"]
    assert "id" in created_device
    assert "created_at" in created_device
    assert "updated_at" in created_device

def test_create_device_validation_error(test_db):
    """バリデーションエラーのテスト"""
    # 名前が空の場合
    response = client.post("/api/v1/devices/", json={
        "name": "",
        "manufacturer": "テストメーカー"
    })
    assert response.status_code == 400
    assert "デバイス名は必須です" in response.json()["error"]["message"]
    
    # メーカー名が空の場合
    response = client.post("/api/v1/devices/", json={
        "name": "テストデバイス",
        "manufacturer": ""
    })
    assert response.status_code == 400
    assert "メーカー名は必須です" in response.json()["error"]["message"]
    
    # 必須フィールドが欠けている場合
    response = client.post("/api/v1/devices/", json={
        "name": "テストデバイス"
    })
    assert response.status_code == 422  # FastAPIのバリデーションエラー

def test_create_device_database_error(test_db):
    """データベースエラーのテスト"""
    # 無効なデータベースエンジンを作成
    invalid_engine = create_engine("mysql+mysqlconnector://invalid:invalid@invalid_host:3306/invalid_db")
    invalid_session = sessionmaker(autocommit=False, autoflush=False, bind=invalid_engine)
    
    def override_get_db():
        db = invalid_session()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        response = client.post("/api/v1/devices/", json={
            "name": "テストデバイス",
            "manufacturer": "テストメーカー"
        })
        assert response.status_code == 500
        assert "error" in response.json()
    finally:
        app.dependency_overrides.clear()

def test_get_device_success(test_db):
    """特定の機器の取得が成功するケースのテスト"""
    # テスト用デバイスの作成
    test_device = Device(
        id="test-device-123",
        name="テスト機器",
        manufacturer="テストメーカー"
    )
    
    # テストデータの保存
    with test_db.connect() as connection:
        connection.execute(Device.__table__.insert().values(
            id=test_device.id,
            name=test_device.name,
            manufacturer=test_device.manufacturer,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        ))
        connection.commit()
    
    # APIリクエスト
    response = client.get(f"/api/v1/devices/{test_device.id}")
    assert response.status_code == 200
    
    # レスポンスの検証
    device = response.json()
    assert device["id"] == test_device.id
    assert device["name"] == test_device.name
    assert device["manufacturer"] == test_device.manufacturer
    assert "created_at" in device
    assert "updated_at" in device

def test_get_device_not_found(test_db):
    """存在しない機器のIDでリクエストした場合のテスト"""
    non_existent_id = "non-existent-id"
    response = client.get(f"/api/v1/devices/{non_existent_id}")
    assert response.status_code == 404
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "DEVICE_NOT_FOUND"
    assert non_existent_id in error_response["error"]["message"]

def test_get_device_invalid_id(test_db):
    """不正なIDフォーマットでリクエストした場合のテスト"""
    # 不正なUUID形式
    invalid_id = "invalid-123"
    response = client.get(f"/api/v1/devices/{invalid_id}")
    assert response.status_code == 400
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "VALIDATION_ERROR"
    assert "無効なデバイスID" in error_response["error"]["message"]
    assert error_response["error"]["details"]["device_id"] == invalid_id

def test_get_device_valid_uuid_not_found(test_db):
    """有効なUUID形式だが存在しないIDでリクエストした場合のテスト"""
    # 有効なUUID形式
    valid_but_non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/devices/{valid_but_non_existent_id}")
    assert response.status_code == 404
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "DEVICE_NOT_FOUND"
    assert valid_but_non_existent_id in error_response["error"]["message"]
    assert error_response["error"]["details"]["device_id"] == valid_but_non_existent_id

def test_get_device_database_error(test_db):
    """データベースエラーが発生した場合のテスト"""
    # データベースエラーをトリガーするUUID
    error_trigger_id = "11111111-1111-1111-1111-111111111111"
    response = client.get(f"/api/v1/devices/{error_trigger_id}")
    assert response.status_code == 500
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "DATABASE_ERROR"
    assert "テスト用のデータベースエラー" in error_response["error"]["message"]

def test_update_device_success(test_db):
    """デバイス更新の正常系テスト"""
    # テスト用デバイスの作成
    test_device = Device(
        id="12345678-1234-5678-1234-567812345678",
        name="テスト機器",
        manufacturer="テストメーカー"
    )
    
    # テストデータの保存
    with test_db.connect() as connection:
        connection.execute(Device.__table__.insert().values(
            id=test_device.id,
            name=test_device.name,
            manufacturer=test_device.manufacturer,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        ))
        connection.commit()
    
    # 更新データ
    update_data = {
        "name": "更新後の機器名",
        "manufacturer": "更新後のメーカー"
    }
    
    # 更新リクエスト
    response = client.put(f"/api/v1/devices/{test_device.id}", json=update_data)
    assert response.status_code == 200
    
    # レスポンスの検証
    updated_device = response.json()
    assert updated_device["name"] == update_data["name"]
    assert updated_device["manufacturer"] == update_data["manufacturer"]
    assert updated_device["id"] == test_device.id
    assert "created_at" in updated_device
    assert "updated_at" in updated_device

def test_update_device_invalid_id(test_db):
    """不正なIDフォーマットでの更新テスト"""
    invalid_id = "invalid-123"
    update_data = {
        "name": "更新後の機器名",
        "manufacturer": "更新後のメーカー"
    }
    
    response = client.put(f"/api/v1/devices/{invalid_id}", json=update_data)
    assert response.status_code == 400
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "VALIDATION_ERROR"
    assert "無効なデバイスID" in error_response["error"]["message"]
    assert error_response["error"]["details"]["device_id"] == invalid_id

def test_update_device_not_found(test_db):
    """存在しないデバイスの更新テスト"""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    update_data = {
        "name": "更新後の機器名",
        "manufacturer": "更新後のメーカー"
    }
    
    response = client.put(f"/api/v1/devices/{non_existent_id}", json=update_data)
    assert response.status_code == 404
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "DEVICE_NOT_FOUND"
    assert non_existent_id in error_response["error"]["message"]

def test_update_device_validation_error(test_db):
    """バリデーションエラーのテスト"""
    test_device_id = "12345678-1234-5678-1234-567812345678"
    
    # 名前が空の場合
    response = client.put(f"/api/v1/devices/{test_device_id}", json={
        "name": "",
        "manufacturer": "テストメーカー"
    })
    assert response.status_code == 400
    assert "デバイス名は必須です" in response.json()["error"]["message"]
    
    # メーカー名が空の場合
    response = client.put(f"/api/v1/devices/{test_device_id}", json={
        "name": "テストデバイス",
        "manufacturer": ""
    })
    assert response.status_code == 400
    assert "メーカー名は必須です" in response.json()["error"]["message"]

def test_update_device_database_error(test_db):
    """データベースエラーのテスト"""
    error_trigger_id = "11111111-1111-1111-1111-111111111111"
    update_data = {
        "name": "更新後の機器名",
        "manufacturer": "更新後のメーカー"
    }
    
    response = client.put(f"/api/v1/devices/{error_trigger_id}", json=update_data)
    assert response.status_code == 500
    
    error_response = response.json()
    assert "error" in error_response
    assert error_response["error"]["code"] == "DATABASE_ERROR"
    assert "テスト用のデータベースエラー" in error_response["error"]["message"]

def test_update_device_422_validation_error(test_db):
    """FastAPIのバリデーションエラー（422）のテスト"""
    test_device_id = "a51844dd-f16e-41c3-862c-0b13ce8455a5"
    
    # ケース1: リクエストボディが空の場合
    response = client.put(
        f"/api/v1/devices/{test_device_id}",
        json=None
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert error_detail[0]["loc"] == ["body"]
    assert "field required" in error_detail[0]["msg"]
    
    # ケース2: 必須フィールドが欠けている場合
    response = client.put(
        f"/api/v1/devices/{test_device_id}",
        json={"name": "テストデバイス"}  # manufacturerが欠けている
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert error_detail[0]["loc"] == ["body", "manufacturer"]
    assert "field required" in error_detail[0]["msg"]
    
    # ケース3: 不正な型の値が含まれる場合
    response = client.put(
        f"/api/v1/devices/{test_device_id}",
        json={
            "name": 123,  # 文字列ではなく数値
            "manufacturer": "テストメーカー"
        }
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert error_detail[0]["loc"] == ["body", "name"]
    assert "str type expected" in error_detail[0]["msg"]
    
    # ケース4: 不正なJSON形式
    response = client.put(
        f"/api/v1/devices/{test_device_id}",
        headers={"Content-Type": "application/json"},
        content="invalid json data"
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert "JSON decode error" in error_detail[0]["msg"] 