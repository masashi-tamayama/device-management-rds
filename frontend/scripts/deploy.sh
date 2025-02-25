#!/bin/bash

# 設定の読み込み
CONFIG_FILE="deploy-config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: deploy-config.json not found"
    exit 1
fi

# 設定値の取得
BUCKET_NAME=$(jq -r '.s3.bucket' "$CONFIG_FILE")
REGION=$(jq -r '.s3.region' "$CONFIG_FILE")
DISTRIBUTION_ID=$(jq -r '.cloudfront.distributionId' "$CONFIG_FILE")

echo "デプロイを開始します..."

# ビルド
echo "ビルドを実行中..."
npm run build

if [ $? -ne 0 ]; then
    echo "Error: ビルドに失敗しました"
    exit 1
fi

# S3へのアップロード
echo "S3バケットにファイルをアップロード中..."
aws s3 sync dist "s3://$BUCKET_NAME" --delete --region "$REGION"

if [ $? -ne 0 ]; then
    echo "Error: S3へのアップロードに失敗しました"
    exit 1
fi

# CloudFrontのキャッシュ削除
if [ ! -z "$DISTRIBUTION_ID" ]; then
    echo "CloudFrontのキャッシュを削除中..."
    aws cloudfront create-invalidation \
        --distribution-id "$DISTRIBUTION_ID" \
        --paths "/*"
    
    if [ $? -ne 0 ]; then
        echo "Warning: CloudFrontのキャッシュ削除に失敗しました"
    fi
fi

echo "デプロイが完了しました！" 