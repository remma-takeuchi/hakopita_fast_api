import logging
import os
from typing import Optional

import pymysql
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# ロガーを取得
logger = logging.getLogger("hakopita_fast_api.db")


class Settings(BaseSettings):
    """アプリケーション設定クラス"""

    # データベース設定（環境変数ファイルから読み込まれる）
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_pass: str = "root"
    db_name: str = "hakopita_database_dev"

    # アプリケーション設定
    app_name: str = "HakoPita FastAPI"
    debug: bool = True
    log_level: str = "DEBUG"
    
    # API設定
    api_prefix: str = "/dev"  # デフォルトは/dev

    model_config = ConfigDict(
        env_file=f".env.{os.getenv('ENV', 'dev')}", env_file_encoding="utf-8"
    )

    database_url: str = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    


# 設定インスタンスを作成
settings = Settings()


def create_database_if_not_exists():
    """データベースが存在しない場合は作成する（オプショナル）"""
    try:
        # データベース名を除いた接続URLを作成（MySQLサーバーに接続）
        server_url = f"mysql+pymysql://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}"
        server_engine = create_engine(server_url)

        with server_engine.connect() as conn:
            # データベースが存在するかチェック
            result = conn.execute(text(f"SHOW DATABASES LIKE '{settings.db_name}'"))
            if not result.fetchone():
                logger.info(f"データベース '{settings.db_name}' が存在しません。作成します...")
                conn.execute(
                    text(
                        f"CREATE DATABASE `{settings.db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                    )
                )
                logger.info(f"データベース '{settings.db_name}' を作成しました。")
            else:
                logger.info(f"データベース '{settings.db_name}' は既に存在します。")

        server_engine.dispose()

    except Exception as e:
        logger.error(f"データベース作成中にエラーが発生しました: {e}")
        logger.warning("データベース作成をスキップします。手動でデータベースを作成してください。")
        # エラーが発生してもアプリケーションは起動する


# データベースが存在しない場合は作成（エラーハンドリング付き）
create_database_if_not_exists()

# SQLAlchemy設定
engine = create_engine(
    settings.database_url, pool_pre_ping=True, pool_recycle=300, echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスを作成
Base = declarative_base()


def get_db():
    """データベースセッションを取得する関数"""
    db = SessionLocal()
    try:
       # 読み取り専用モードでセッションを開始
        db.execute(text("SET TRANSACTION READ ONLY"))        
        yield db
    finally:
        db.close()

