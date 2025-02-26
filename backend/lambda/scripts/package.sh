#!/bin/bash

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$SCRIPT_DIR/.."
cd "$BASE_DIR"

echo "パッケージングを開始します..."

# 作業ディレクトリの作成とクリーンアップ
PACKAGE_DIR="$BASE_DIR/package"
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR/devices/handlers"
cd "$PACKAGE_DIR"

# 必要な6つのファイルのみをコピー
echo "必要なファイルをコピーしています..."
# 1. メインハンドラー
cp "$BASE_DIR/devices/handlers/device_handlers.py" devices/handlers/
# 2. データベースモデル
cp "$BASE_DIR/devices/models.py" devices/
# 3. スキーマ定義
cp "$BASE_DIR/devices/schemas.py" devices/
# 4. データベース設定
cp "$BASE_DIR/devices/database.py" devices/
# 5. パッケージ化用の__init__.py
touch devices/__init__.py
# 6. 環境設定
cp "$BASE_DIR/../../backend/config.py" .

# 必要なライブラリをインストール
echo "必要なライブラリをインストールしています..."
pip install \
    fastapi==0.109.2 \
    mangum==0.19.0 \
    sqlalchemy==2.0.27 \
    mysql-connector-python==8.3.0 \
    pydantic==2.6.1 \
    typing_extensions \
    starlette \
    -t .

# 明示的に指定したファイルのみをZIP化
echo "ZIPファイルを作成しています..."
cd "$PACKAGE_DIR"
zip -r ../function.zip \
    devices/handlers/device_handlers.py \
    devices/models.py \
    devices/schemas.py \
    devices/database.py \
    devices/__init__.py \
    config.py \
    fastapi \
    mangum \
    sqlalchemy \
    mysql \
    pydantic \
    typing_extensions.py \
    starlette

# ZIPファイルの内容を確認
echo "ZIPファイルの内容を確認しています..."
cd "$BASE_DIR"
echo "ZIPファイルの内容:"
unzip -l function.zip

echo "パッケージングが完了しました。"
echo "作成されたファイル: function.zip" 