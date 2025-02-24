#!/bin/bash

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$SCRIPT_DIR/.."
cd "$BASE_DIR"

echo "パッケージングを開始します..."

# 作業ディレクトリの作成とクリーンアップ
PACKAGE_DIR="$BASE_DIR/package"
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR/python"

# 既存の仮想環境を使用
echo "仮想環境をアクティベートしています..."
source venv/bin/activate

# 必要なパッケージのインストール
echo "依存パッケージをインストールしています..."
pip install -r requirements.txt --target "$PACKAGE_DIR/python"

# パッケージの不要なファイルを削除（先に削除）
echo "パッケージの不要なファイルを削除しています..."
find "$PACKAGE_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type f -name "*.pyc" -delete
find "$PACKAGE_DIR" -type f -name "*.pyo" -delete
find "$PACKAGE_DIR" -type f -name "*.pyd" -delete
find "$PACKAGE_DIR" -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type d -name "test" -exec rm -rf {} + 2>/dev/null || true

# ソースコードのコピー
echo "ソースコードをコピーしています..."
cp -r devices/* "$PACKAGE_DIR/python/"
cp -r ../../backend/config.py "$PACKAGE_DIR/python/"

# ソースコードの不要なファイルを削除
echo "ソースコードの不要なファイルを削除しています..."
find "$PACKAGE_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type f -name "*.pyc" -delete
find "$PACKAGE_DIR" -type f -name "*.pyo" -delete
find "$PACKAGE_DIR" -type f -name "*.pyd" -delete

# 一時ディレクトリを作成してファイルをコピー（パス区切り文字を修正するため）
echo "ファイル構造を正規化しています..."
TMP_DIR="$PACKAGE_DIR/tmp"
mkdir -p "$TMP_DIR"
cd "$PACKAGE_DIR/python"
find . -type f -print0 | while IFS= read -r -d '' file; do
    # パス区切り文字をスラッシュに変換
    normalized_path=$(echo "$file" | sed 's|\\|/|g')
    dir=$(dirname "$normalized_path")
    mkdir -p "$TMP_DIR/$dir"
    cp "$file" "$TMP_DIR/$normalized_path"
done

# 再度不要なファイルを削除（念のため）
echo "最終クリーンアップを実行しています..."
find "$TMP_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$TMP_DIR" -type f -name "*.pyc" -delete
find "$TMP_DIR" -type f -name "*.pyo" -delete
find "$TMP_DIR" -type f -name "*.pyd" -delete
find "$TMP_DIR" -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find "$TMP_DIR" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# ZIPファイルの作成（Unixスタイルのパス区切り文字を使用）
echo "ZIPファイルを作成しています..."
cd "$TMP_DIR"
find . -type f -print0 | LC_ALL=C sort -z | xargs -0 zip -X "$BASE_DIR/function.zip"

# クリーンアップ
cd "$BASE_DIR"
rm -rf "$PACKAGE_DIR"

echo "パッケージングが完了しました。"
echo "作成されたファイル: function.zip" 