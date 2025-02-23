# POST/GET/PUT/DELETE /devices/{id} API仕様書

# POST /devices エンドポイントテスト記録

## 1. 正常系テスト

### リクエスト
- エンドポイント: POST /api/v1/devices/
- Content-Type: application/json
- リクエストボディ:
```json
{
  "name": "テスト機器",
  "manufacturer": "テストメーカー"
}
```

### レスポンス
- ステータスコード: 201 Created
- レスポンスボディ:
```json
{
  "name": "テスト機器",
  "manufacturer": "テストメーカー",
  "id": "d62547cc-21fd-4c8e-9f47-c8b0a0615c8a",
  "created_at": "2025-02-22T16:32:01",
  "updated_at": "2025-02-22T16:32:01"
}
```

## 2. エラーケーステスト

### ケース1: デバイス名が空の場合
- リクエストボディ:
```json
{
  "name": "",
  "manufacturer": "テストメーカー"
}
```

### レスポンス
- ステータスコード: 400 Bad Request
- エラーコード: VALIDATION_ERROR
- レスポンスボディ:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "デバイス名は必須です",
    "details": {
      "field": "name"
    }
  }
}
```

### ケース2: メーカー名が空の場合
- リクエストボディ:
```json
{
  "name": "テスト機器",
  "manufacturer": ""
}
```

### レスポンス
- ステータスコード: 400 Bad Request
- エラーコード: VALIDATION_ERROR
- レスポンスボディ:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "メーカー名は必須です",
    "details": {
      "field": "manufacturer"
    }
  }
}
```

### ケース3: 必須フィールドが欠落している場合
- リクエストボディ:
```json
{
  "name": "テスト機器"
}
```

### レスポンス
- ステータスコード: 422 Unprocessable Content
- エラーコード: None (FastAPI標準バリデーションエラー)
- レスポンスボディ:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "manufacturer"
      ],
      "msg": "Field required",
      "input": {
        "name": "テスト機器"
      }
    }
  ]
}
```

## テスト実行ログ
```
INFO:     127.0.0.1:50603 - "POST /api/v1/devices/ HTTP/1.1" 201 Created
INFO:     127.0.0.1:50605 - "POST /api/v1/devices/ HTTP/1.1" 422 Unprocessable Content
INFO:     127.0.0.1:50798 - "POST /api/v1/devices/ HTTP/1.1" 201 Created
エラーが発生しました - コード: VALIDATION_ERROR, メッセージ: デバイス名は必須です, 詳細: {'field': 'name'}
INFO:     127.0.0.1:50818 - "POST /api/v1/devices/ HTTP/1.1" 400 Bad Request
エラーが発生しました - コード: VALIDATION_ERROR, メッセージ: メーカー名は必須です, 詳細: {'field': 'manufacturer'}
INFO:     127.0.0.1:50840 - "POST /api/v1/devices/ HTTP/1.1" 400 Bad Request
```

## 確認項目チェックリスト
- [x] 正常系：新規デバイス作成成功
- [x] 空のデバイス名でのバリデーションエラー
- [x] 空のメーカー名でのバリデーションエラー
- [x] 必須フィールド欠落時のバリデーションエラー
- [x] 各レスポンスのステータスコードが適切
- [x] エラーメッセージが日本語で分かりやすい
- [x] レスポンスボディのフォーマットが一貫している
- [x] タイムスタンプが正しいフォーマットで生成
- [x] UUIDが正しく生成

## テスト環境
- サーバー: uvicorn (FastAPI)
- エンドポイント: http://localhost:8000/api/v1/devices/
- テストツール: Swagger UI (http://localhost:8000/docs)
- データベース: DynamoDB

これで、POST /devicesエンドポイントの動作が要件通りに実装されていることが確認できました。


# GET /devices APIテスト実施記録

## 📝 テスト概要
- テスト日時: 2024-02-22
- テスト環境: ローカル開発環境
- エンドポイント: `http://localhost:8000/api/v1/devices`
- テストツール: Swagger UI (`http://localhost:8000/docs`)

## 🔍 テストケース1: デバイス一覧取得
### 手順
1. Swagger UIで`GET /api/v1/devices/`を選択
2. 「Try it out」ボタンをクリック
3. パラメータ入力なしで「Execute」ボタンをクリック

### 結果
- **ステータスコード**: 200 OK
- **レスポンスボディ**:
```json
[
  {
    "name": "洗濯機",
    "manufacturer": "シャープ",
    "id": "1b73c6e4-a500-4163-91f7-ac8a4081cbbf",
    "created_at": "2025-02-22T02:31:18",
    "updated_at": "2025-02-22T02:31:18"
  },
  // ... 他10件のデバイス情報
]
```
- **確認項目**:
  - 全11件のデバイスが取得できた
  - 各デバイスの必須フィールド（name, manufacturer, id, created_at, updated_at）が存在
  - 日本語が正しく表示されている

## 🔍 テストケース2: 個別デバイス取得（正常系）
### 手順
1. テストケース1で取得したデバイスIDをコピー  
   使用ID: `d22c26a4-ac22-4be0-b589-238d009b9d74`
2. `GET /api/v1/devices/{device_id}`を選択
3. 「Try it out」ボタンをクリック
4. device_idパラメータに上記IDを入力
5. 「Execute」ボタンをクリック

### 結果
- **ステータスコード**: 200 OK
- **レスポンスボディ**:
```json
{
  "name": "掃除機",
  "manufacturer": "ダイソン",
  "id": "d22c26a4-ac22-4be0-b589-238d009b9d74",
  "created_at": "2025-02-22T02:31:18",
  "updated_at": "2025-02-22T02:31:18"
}
```
- **確認項目**:
  - 指定したIDのデバイス情報が正しく取得できた
  - すべてのフィールドが期待通りの形式で返却された

## 🔍 テストケース3: 存在しないIDでの取得
### 手順
1. `GET /api/v1/devices/{device_id}`を選択
2. 「Try it out」ボタンをクリック
3. device_idパラメータに存在しないUUID形式の値を入力  
   入力値: `00000000-0000-0000-0000-000000000000`
4. 「Execute」ボタンをクリック

### 結果
- **ステータスコード**: 404 Not Found
- **エラーコード**: `DEVICE_NOT_FOUND`
- **レスポンスボディ**:
```json
{
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "デバイスが見つかりません: 00000000-0000-0000-0000-000000000000",
    "details": {
      "device_id": "00000000-0000-0000-0000-000000000000"
    }
  }
}
```
- **確認項目**:
  - 適切なエラーステータスコードが返却された
  - エラーメッセージが日本語で正しく表示されている
  - エラー詳細にデバイスIDが含まれている

## 🔍 テストケース4: 不正なUUID形式での取得
### 手順
1. `GET /api/v1/devices/{device_id}`を選択
2. 「Try it out」ボタンをクリック
3. device_idパラメータに不正な形式の値を入力  
   入力値: `invalid-id`
4. 「Execute」ボタンをクリック

### 結果
- **ステータスコード**: 400 Bad Request
- **エラーコード**: `VALIDATION_ERROR`
- **レスポンスボディ**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "無効なデバイスID: invalid-id",
    "details": {
      "device_id": "invalid-id"
    }
  }
}
```
- **確認項目**:
  - バリデーションエラーが適切に検出された
  - エラーメッセージが具体的で分かりやすい
  - 入力値がエラー詳細に含まれている

## 📋 総合評価
- すべてのテストケースで期待通りの動作を確認
- エラーハンドリングが適切に実装されている
- レスポンスのフォーマットが一貫している
- 日本語対応が正しく機能している

## 📌 注意点
- テスト実施前にDynamoDBのテーブルが正しく設定されていることを確認
- 環境変数`DB_TYPE=dynamodb`が設定されていることを確認
- テストデータが事前に投入されていることを確認


# PUT /devices/{id} APIテスト実施記録

## 🔧 1. 事前準備

### 1.1 データベース設定確認
```bash
# .envファイルでDynamoDBを使用するように設定
DB_TYPE=dynamodb
DYNAMODB_TABLE_NAME=devices
```

### 1.2 サーバー起動
```bash
cd backend/lambda
python -m uvicorn devices.main:app --reload
```

### 1.3 テストデータ作成
```bash
# テストデータ投入スクリプトを実行
python devices/scripts/insert_test_data.py
```

## 📝 2. テストケース実行

### 2.1 正常系テスト（200 OK）
**リクエスト**:
- メソッド: PUT
- エンドポイント: `/api/v1/devices/d22c26a4-ac22-4be0-b589-238d009b9d74`
- リクエストボディ:
```json
{
    "name": "更新後のテスト機器",
    "manufacturer": "更新後のメーカー"
}
```

**レスポンス**:
- ステータスコード: 200 OK
- レスポンスボディ:
```json
{
    "name": "更新後のテスト機器",
    "manufacturer": "更新後のメーカー",
    "id": "d22c26a4-ac22-4be0-b589-238d009b9d74",
    "created_at": "2024-02-20T05:30:00.000Z",
    "updated_at": "2024-02-20T05:35:00.000Z"
}
```

### 2.2 存在しないデバイスID（404 Not Found）
**リクエスト**:
- メソッド: PUT
- エンドポイント: `/api/v1/devices/00000000-0000-0000-0000-000000000000`
- リクエストボディ:
```json
{
    "name": "テスト機器",
    "manufacturer": "テストメーカー"
}
```

**レスポンス**:
- ステータスコード: 404 Not Found
- エラーコード: `DEVICE_NOT_FOUND`
- レスポンスボディ:
```json
{
    "error": {
        "code": "DEVICE_NOT_FOUND",
        "message": "デバイスが見つかりません: 00000000-0000-0000-0000-000000000000",
        "details": {
            "device_id": "00000000-0000-0000-0000-000000000000"
        }
    }
}
```

### 2.3 不正なUUID形式（400 Bad Request）
**リクエスト**:
- メソッド: PUT
- エンドポイント: `/api/v1/devices/invalid-id`
- リクエストボディ:
```json
{
    "name": "テスト機器",
    "manufacturer": "テストメーカー"
}
```

**レスポンス**:
- ステータスコード: 400 Bad Request
- エラーコード: `VALIDATION_ERROR`
- レスポンスボディ:
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "無効なデバイスID: invalid-id",
        "details": {
            "device_id": "invalid-id"
        }
    }
}
```

### 2.4 必須フィールド欠落（422 Unprocessable Content）
**リクエスト**:
- メソッド: PUT
- エンドポイント: `/api/v1/devices/d22c26a4-ac22-4be0-b589-238d009b9d74`
- リクエストボディ:
```json
{
    "name": "テスト機器"
}
```

**レスポンス**:
- ステータスコード: 422 Unprocessable Content
- エラーコード: なし（FastAPIのデフォルトバリデーション）
- レスポンスボディ:
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "manufacturer"],
            "msg": "Field required",
            "input": {
                "name": "テスト機器"
            }
        }
    ]
}
```

## 📊 3. テスト結果まとめ

| テストケース | ステータスコード | エラーコード | 結果 |
|------------|----------------|-------------|------|
| 正常系 | 200 | - | ✅ 成功 |
| 存在しないID | 404 | DEVICE_NOT_FOUND | ✅ 成功 |
| 不正なUUID | 400 | VALIDATION_ERROR | ✅ 成功 |
| 必須フィールド欠落 | 422 | - | ✅ 成功 |

## 📝 4. 補足事項
- すべてのエラーレスポンスは適切な形式で返却
- 日本語のエラーメッセージを実装（422エラー以外）
- タイムスタンプはUTC形式で返却
- DynamoDBとの連携が正常に機能

## 🔍 5. 改善提案
1. 422エラーの日本語対応
2. エラーメッセージの統一フォーマット化
3. バリデーションルールのドキュメント化

## 概要
指定されたIDのデバイスを削除するAPI

## エンドポイント
`DELETE /api/v1/devices/{device_id}`

## リクエスト
### パスパラメータ
| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| device_id | string | ○ | デバイスの一意識別子（UUID形式） |

### リクエストボディ
なし

## レスポンス

### 正常系（200 OK）
デバイスの削除が成功した場合

```json
{
  "message": "デバイスを削除しました",
  "device_id": "d22c26a4-ac22-4be0-b589-238d009b9d74"
}
```

### エラーレスポンス

#### 400 Bad Request
不正なUUID形式の場合

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "無効なデバイスID: invalid-id",
    "details": {
      "device_id": "invalid-id"
    }
  }
}
```

#### 404 Not Found
指定されたIDのデバイスが存在しない場合

```json
{
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "デバイスが見つかりません: 00000000-0000-0000-0000-000000000000",
    "details": {
      "device_id": "00000000-0000-0000-0000-000000000000"
    }
  }
}
```

#### 500 Internal Server Error
サーバー内部でエラーが発生した場合

```json
{
  "error": {
    "code": "DATABASE_ERROR",
    "message": "テスト用のデータベースエラー",
    "details": {}
  }
}
```

## テスト手順

### 1. 事前準備
1. データベースの設定確認
   ```bash
   # .envファイルでDynamoDBを使用するように設定
   DB_TYPE=dynamodb
   DYNAMODB_TABLE_NAME=devices
   ```

2. サーバーの起動
   ```bash
   cd backend/lambda
   python -m uvicorn devices.main:app --reload
   ```

### 2. テストケース実行

#### 2.1 正常系テスト
1. リクエスト
   - メソッド: DELETE
   - URL: `http://localhost:8000/api/v1/devices/d22c26a4-ac22-4be0-b589-238d009b9d74`

2. レスポンス
   - ステータスコード: 200 OK
   - レスポンスボディ:
     ```json
     {
       "message": "デバイスを削除しました",
       "device_id": "d22c26a4-ac22-4be0-b589-238d009b9d74"
     }
     ```

#### 2.2 存在しないデバイスIDテスト
1. リクエスト
   - メソッド: DELETE
   - URL: `http://localhost:8000/api/v1/devices/00000000-0000-0000-0000-000000000000`

2. レスポンス
   - ステータスコード: 404 Not Found
   - エラーコード: `DEVICE_NOT_FOUND`
   - レスポンスボディ:
     ```json
     {
       "error": {
         "code": "DEVICE_NOT_FOUND",
         "message": "デバイスが見つかりません: 00000000-0000-0000-0000-000000000000",
         "details": {
           "device_id": "00000000-0000-0000-0000-000000000000"
         }
       }
     }
     ```

#### 2.3 不正なUUID形式テスト
1. リクエスト
   - メソッド: DELETE
   - URL: `http://localhost:8000/api/v1/devices/invalid-id`

2. レスポンス
   - ステータスコード: 400 Bad Request
   - エラーコード: `VALIDATION_ERROR`
   - レスポンスボディ:
     ```json
     {
       "error": {
         "code": "VALIDATION_ERROR",
         "message": "無効なデバイスID: invalid-id",
         "details": {
           "device_id": "invalid-id"
         }
       }
     }
     ```

#### 2.4 データベースエラーテスト
1. リクエスト
   - メソッド: DELETE
   - URL: `http://localhost:8000/api/v1/devices/11111111-1111-1111-1111-111111111111`

2. レスポンス
   - ステータスコード: 500 Internal Server Error
   - エラーコード: `DATABASE_ERROR`
   - レスポンスボディ:
     ```json
     {
       "error": {
         "code": "DATABASE_ERROR",
         "message": "テスト用のデータベースエラー",
         "details": {}
       }
     }
     ```

## 実装の補足事項
1. エラーメッセージは一貫して日本語で提供
2. エラーレスポンスの形式が統一されている
3. デバイスIDのバリデーションが適切に機能
4. データベースの内部エラーメッセージは外部に漏れないよう制御 