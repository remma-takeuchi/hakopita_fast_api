import os
from typing import Optional

import pymysql
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


class Settings(BaseSettings):
    """アプリケーション設定クラス"""

    # データベース設定（デフォルト値）
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_pass: str = "root"
    db_name: str = "hakopita_database_dev"

    # アプリケーション設定
    app_name: str = "HakoPita FastAPI"
    debug: bool = True
    log_level: str = "DEBUG"
    
    # 環境変数ファイル(.env.*)から読み込む（デフォルトは.env.dev）
    model_config = ConfigDict(
        env_file=f".env.{os.getenv('ENV', 'dev')}", env_file_encoding="utf-8"
    )

    # データベースURLを作成
    database_url: str = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


# 設定インスタンスを作成
settings = Settings()
print(settings.database_url)
print(os.environ)

# SQLAlchemy設定
engine = create_engine(
    settings.database_url, pool_pre_ping=True, pool_recycle=300, echo=settings.debug
)

# セッションを作成
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

