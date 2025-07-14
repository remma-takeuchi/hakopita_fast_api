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

## セットアップ

### 前提条件

- Python 3.11以上
- Poetry
- MySQL

### インストール

```bash
# 依存関係をインストール
make install

# 環境変数ファイルを設定
cp env.dev .env.dev
cp env.prod .env.prod
cp env.test .env.test
cp env.remote.dev .env.remote.dev

# 各環境変数ファイルを編集して、実際のデータベース接続情報を設定
```

### 環境変数の設定

各環境用の`.env.{環境名}`ファイルを作成し、以下の項目を設定してください：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASS=your_password
DB_NAME=hakopita_database_dev
```

### データベース構成

- **開発環境**: `hakopita_database_dev`
- **テスト環境**: `hakopita_database_test`
- **本番環境**: `hakopita_database_v4.0`
- **リモート開発環境**: `hakopita_database_dev` (リモートDB)

## 使用方法

### 開発環境での起動

```bash
make run ENV=dev
```

### リモート開発環境での起動

```bash
make run ENV=remote.dev
```

### 本番環境での起動

```bash
make run ENV=prod
```

### テスト実行

```bash
# ローカル環境でのテスト
make test

# リモート開発環境でのテスト
make test-remote

# カバレッジ付きテスト（ローカル）
make test-cov

# カバレッジ付きテスト（リモート）
make test-cov-remote
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

## API エンドポイント

### GET /api/fetch_storage
指定されたIDリストに基づいてストレージデータを取得します。

**クエリパラメータ:**
- `id_list`: カンマ区切りのストレージデータIDリスト

**例:**
```
GET /api/fetch_storage?id_list=0_4549131159912,100_10008758
```

### GET /api/search_storage
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
GET /api/search_storage?width=20&depth=30&height=25&storage_category=0&country_code=jp&page=0&page_size=10
```

## プロジェクト構造

```
hakopita_fast_api/
├── app/
│   ├── main.py              # FastAPIアプリケーションのエントリーポイント
│   ├── db/
│   │   ├── session.py       # データベースセッション管理
│   │   └── __init__.py
│   ├── models/
│   │   ├── storage_data.py  # SQLAlchemyモデル
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── storage_data.py  # Pydanticスキーマ
│   │   └── __init__.py
│   ├── crud/
│   │   ├── storage_data.py  # CRUD操作
│   │   └── __init__.py
│   ├── routers/
│   │   ├── storage.py       # APIルーター
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── test_fetch_storage.py
│   └── test_search_storage.py
├── pyproject.toml           # Poetry設定
├── Makefile                 # ビルド・実行コマンド
├── env.dev                  # 開発環境設定
├── env.prod                 # 本番環境設定
├── env.test                 # テスト環境設定
├── env.remote.dev           # リモート開発環境設定
└── README.md
```

## 開発ガイドライン

### コードフォーマット

```bash
make format
```

### テスト

```bash
make test
```

### リント

```bash
make lint
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 