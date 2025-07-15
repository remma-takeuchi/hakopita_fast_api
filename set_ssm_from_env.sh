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
  [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
  # 末尾の改行やクォートを除去
  value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//')
  echo "Setting $PREFIX/${key} ..."
  aws ssm put-parameter \
    --name "$PREFIX/${key}" \
    --value "$value" \
    --type "SecureString" \
    --overwrite
done < "$ENV_FILE"