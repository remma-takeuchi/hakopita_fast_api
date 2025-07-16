#!/bin/bash

# 使い方: ./set_ssm_from_env.sh .env.v1 v1

ENV_FILE=$1
STAGE=$2
PREFIX="/hakopita-fast-api-${STAGE}"

if [ ! -f "$ENV_FILE" ]; then
  echo "File not found: $ENV_FILE"
  exit 1
fi

while IFS='=' read -r key value
do
  # 空行やコメント行はスキップ
  if [[ "$key" =~ ^#.*$ || -z "$key" ]]; then
    continue
  fi
  # キーがDATABASE_URLの場合は、データベースURLを作成
  if [ "$key" = "DATABASE_URL" ]; then
    value="mysql+pymysql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
  # その他のキーは末尾の改行やクォートを除去して登録
  else
    value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//')
  fi
  echo "Setting SSM Parameter: $PREFIX/${key}: $value"
  aws ssm put-parameter \
    --name "$PREFIX/${key}" \
    --value "$value" \
    --type "SecureString" \
    --overwrite
  export $key=$value
done < "$ENV_FILE"