#!/bin/bash

# 環境変数の読み込み
if [ -f .env ]; then
    source .env
else
    echo ".envファイルが見つかりません"
    exit 1
fi

# 設定の読み込み
FUNCTION_NAME=$(jq -r '.FunctionName' deploy-config.json)
RUNTIME=$(jq -r '.Runtime' deploy-config.json)
HANDLER=$(jq -r '.Handler' deploy-config.json)
MEMORY_SIZE=$(jq -r '.MemorySize' deploy-config.json)
TIMEOUT=$(jq -r '.Timeout' deploy-config.json)

echo "Lambda関数のデプロイを開始します..."

# Lambda関数の存在確認
if aws lambda get-function --function-name $FUNCTION_NAME 2>/dev/null; then
    # 関数が存在する場合は更新
    echo "既存の関数を更新します: $FUNCTION_NAME"
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://function.zip

    # 設定の更新
    aws lambda update-function-configuration \
        --function-name $FUNCTION_NAME \
        --runtime $RUNTIME \
        --handler $HANDLER \
        --memory-size $MEMORY_SIZE \
        --timeout $TIMEOUT \
        --environment "Variables={STAGE=production,LOG_LEVEL=INFO}"
else
    # 関数が存在しない場合は新規作成
    echo "新しい関数を作成します: $FUNCTION_NAME"
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime $RUNTIME \
        --handler $HANDLER \
        --memory-size $MEMORY_SIZE \
        --timeout $TIMEOUT \
        --role $LAMBDA_ROLE_ARN \
        --environment "Variables={STAGE=production,LOG_LEVEL=INFO}" \
        --zip-file fileb://function.zip
fi

echo "デプロイが完了しました。" 