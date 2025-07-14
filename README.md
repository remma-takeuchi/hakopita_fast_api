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

# 各環境変数ファイルを編集して、実際のデータベース接続情報を設定
```

### 環境変数の設定

`.env.template`から各環境用(dev/prod)の`.env.{環境名}`ファイルを作成し、以下の項目を設定してください：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASS=your_password
DB_NAME=hakopita_database_dev
```

## 使用方法

### 開発環境での起動

```bash
make run ENV=dev
```

### 本番環境での起動

```bash
make run ENV=prod
```

### テスト実行

```bash
# ローカル環境でのテスト
make test

# カバレッジ付きテスト
make test-cov
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

**curlコマンド例:**
```bash
curl "http://localhost:8000/api/fetch_storage?id_list=0_4549131159912,100_10008758"
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

**curlコマンド例:**
```bash
curl "http://localhost:8000/api/search_storage?country_code=jp&page=0&page_size=2000&storage_category=0&use_width_range=true&width_lower_limit=10&width_upper_limit=20"
```

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
├── pyproject.toml           # Poetry設定
├── poetry.lock              # Poetry依存関係ロック
├── Makefile                 # ビルド・実行コマンド
├── .env.template            # 環境変数テンプレート
├── .gitignore               # Git除外設定
├── LICENSE                  # ライセンスファイル
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