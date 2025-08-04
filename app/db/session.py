import os
import sys
from typing import Optional

import pymysql
from pydantic import ConfigDict, computed_field
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
        env_file=f".env.{os.getenv('ENV', 'dev')}", 
        env_file_encoding="utf-8",
        extra="ignore"  # 追加の環境変数を無視
    )

    @computed_field
    @property
    def database_url(self) -> str:
        """データベースURLを動的に生成"""
        return f"mysql+pymysql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


# テスト環境かどうかを判定
def is_testing() -> bool:
    """テスト環境かどうかを判定"""
    return (
        'pytest' in sys.modules or
        os.getenv('PYTEST_CURRENT_TEST') is not None or
        'test' in sys.argv[0] if sys.argv else False
    )


# 設定インスタンスを作成
settings = Settings()

# テスト環境でない場合のみDB情報を出力
if not is_testing():
    print(settings.database_url)

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

