# HakoPita FastAPI

HakoPitaのストレージデータ管理用FastAPIアプリケーション

## 概要

このプロジェクトは、HakoPitaのストレージデータを管理するためのFastAPIアプリケーションです。
元のLambda関数ベースのAPIをFastAPI + SQLAlchemy + MySQL + Poetryを使ったモダンな構成に移行しました。

## 機能

- **fetch_storage**: クエリパラメータでitem_idのリストを受取り、該当するデータを返す
- **search_storage**: クエリパラメータでstorage_dataのサイズ情報を受け取り、該当するデータを検索して返す

## 技術スタック

- **FastAPI**: APIフレームワーク
- **SQLAlchemy**: ORM
- **MySQL**: データベース
- **Poetry**: 依存関係管理
- **Pydantic**: データバリデーション
- **Pytest**: テストフレームワーク


## プロジェクト構造

```
hakopita_fast_api/
├── app/
│   ├── main.py              # FastAPIアプリケーションのエントリーポイント
│   ├── core/
│   │   └── logging.py       # ログ設定
│   ├── db/
│   │   ├── session.py       # データベースセッション管理
│   │   └── __init__.py
│   ├── models/
│   │   ├── storage_model.py # SQLAlchemyモデル
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── storage_schemas.py # Pydanticスキーマ
│   │   └── __init__.py
│   ├── crud/
│   │   ├── storage_crud.py  # CRUD操作
│   │   └── __init__.py
│   ├── routers/
│   │   ├── storage_router.py # APIルーター
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── conftest.py          # Pytest設定
│   ├── test_fetch_storage.py
│   └── test_search_storage.py
├── lambda_handler.py         # AWS Lambda用ハンドラー
├── serverless.yml.example   # Serverless Framework設定例
├── pyproject.toml           # Poetry設定
├── poetry.lock              # Poetry依存関係ロック
├── Makefile                 # ビルド・実行コマンド
├── .env.template            # 環境変数テンプレート
├── .gitignore               # Git除外設定
├── LICENSE                  # ライセンスファイル
└── README.md
```

## API エンドポイント

### GET /{prefix}/fetch_storage
指定されたIDリストに基づいてストレージデータを取得します。

**クエリパラメータ:**
- `id_list`: カンマ区切りのストレージデータIDリスト

**例:**
```
GET /fetch_storage?id_list=0_4549131159912,100_10008758
```

**curlコマンド例:**
```bash
curl "http://localhost:8000/fetch_storage?id_list=0_4549131159912,100_10008758"
```

### GET /{prefix}/search_storage
サイズ条件に基づいてストレージデータを検索します。

**クエリパラメータ:**
- `width`: 幅
- `depth`: 奥行き
- `height`: 高さ
- `storage_category`: ストレージカテゴリ（0: Box, 1: Shelf）
- `country_code`: 国コード（jp/us）
- `page`: ページ番号
- `page_size`: ページサイズ

**例:**
```
GET /search_storage?width=20&depth=30&height=25&storage_category=0&country_code=jp&page=0&page_size=10
```

**curlコマンド例:**
```bash
curl "http://localhost:8000/search_storage?country_code=jp&page=0&page_size=2000&storage_category=0&use_width_range=true&width_lower_limit=10&width_upper_limit=20"
```

## デプロイオプション

このプロジェクトは以下の方法でデプロイできます：

### 1. オンプレミス
- **使用技術**: uvicorn + FastAPI

### 2. AWS Lambda + API Gateway
- **使用技術**: mangum + FastAPI

## 使用方法

### 前提条件

- Python 3.11以上
- Poetry
- MySQL

### 依存パッケージのインストール

```bash
# 依存関係をインストール
make install

# 各環境変数ファイルを編集して、実際のデータベース接続情報を設定
```

### 環境変数の設定

`.env.template`から各環境用(例：dev/prod)の`.env.{環境名}`ファイルを作成し、以下の項目を設定してください：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASS=your_password
DB_NAME=hakopita_database_dev
```

### テスト実行

```bash
# ローカル環境でのテスト
make test

# カバレッジ付きテスト
make test-cov
```

### オンプレミス環境での起動
#### 開発環境

```bash
make run ENV=dev
```

#### 本番環境

```bash
make run ENV=prod
```

### AWS Lambdaへのデプロイ

#### 前提条件

- AWS CLI
- Serverless Framework
- Node.js

#### セットアップ

```bash
# Serverless Frameworkをインストール
npm install -g serverless

# AWS認証情報を設定
aws configure
```

#### セキュリティ設定
AWS Systems Manager Parameter Storeにパラメータを設定します。  
**重要**: セキュリティグループIDやサブネットIDなどの機密情報を公開リポジトリに記載することは避けてください。

```bash
# VPC設定
aws ssm put-parameter --name "/hakopita/security_group_id" --value "sg-xxxxxxxxxxxxxxxxx" --type "SecureString"
aws ssm put-parameter --name "/hakopita/subnet_id" --value "subnet-xxxxxxxxxxxxxxxxx" --type "SecureString"
```

#### デプロイ手順

Serverless Frameworkは自動的にパッケージングを行います：

1. **依存関係の解決**: Poetryの依存関係を自動的に読み取り
2. **コードのバンドル**: アプリケーションコードを自動的に含める
3. **ZIPファイルの作成**: デプロイ用のZIPファイルを自動生成
4. **Lambda関数へのデプロイ**: 作成されたパッケージをLambda関数にデプロイ

```bash
# Serverless Frameworkでデプロイ (devステージ)
make deploy-serverless

# デプロイを削除 （devステージ）
make remove-serverless
```

### その他のコマンド

```bash
# コードフォーマット
make format

# リント実行
make lint

# 依存関係更新
make update

# ヘルプ表示
make help
```

## 注意事項

### 機密情報の管理
- セキュリティグループID、サブネットIDなどの機密情報は公開リポジトリに記載しないでください
- AWS Systems Manager Parameter Storeを使用して機密情報を管理してください

### 補足：SSMパラメータによる接続先DBの登録（AWS Lambda環境）

本プロジェクトはデータベース接続情報等の機密情報は、AWS Systems Manager Parameter Store（SSM）で管理することができます。
`set_ssm_from_env.sh`を利用することで`.env.*`に記載される接続先情報を、SSMパラメータとして一括登録できます。

#### 目的・用途
- 機密情報（DB接続情報など）をGitリポジトリに含めず、AWS SSM Parameter Storeで安全に管理する
- 環境ごと（dev, v1など）に異なるパラメータを簡単に一括登録できる
- Serverless Frameworkの`serverless.yml`からSSMパラメータを参照し、Lambdaの環境変数として利用する

#### 使用方法
1. 事前にAWS CLIで認証情報を設定しておく（`aws configure`など）
2. `.env.dev`や`.env.v1`など、各環境用の.envファイルを用意する
3. スクリプトを実行

```bash
./set_ssm_from_env.sh .env.v1 v1
```
- 第1引数: .envファイルのパス
- 第2引数: ステージ名（例: dev, v1 など）

これにより、.envファイル内の各キー・バリューが`/hakopita-fast-api-<ステージ>/<キー名>`というSSMパラメータとしてSecureString型で登録されます。

> 例: `.env.v1`に`DB_HOST=xxx.rds.amazonaws.com`とあれば、
> `/hakopita-fast-api-v1/DB_HOST` というSSMパラメータが作成されます。

### 注意事項
- スクリプトは**.envファイルの全てのキーをSSMに登録**します。不要な情報は.envから除外してください。
- SSMパラメータの登録・上書きには適切なIAM権限が必要です。
- SSMパラメータはServerless Frameworkの`serverless.yml`で`${ssm:/hakopita-fast-api-${opt:stage}/DB_HOST}`のように参照しています。
