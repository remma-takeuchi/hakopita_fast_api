import logging
import os
import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.db.session import engine, settings
from app.models.storage_model import Base
from app.routers.storage_router import router as storage_router

# ログ設定をセットアップ
logger = setup_logging()

# バージョン取得（起動時に一度だけ実行）
def get_git_version():
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--always'],
            capture_output=True, text=True, check=True
        )
        version = result.stdout.strip()
        return version
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Git version not found: {e}")
        return "unknown"

# バージョンをメタ情報として保持
VERSION = get_git_version()

# データベーステーブルを作成（エラーハンドリング付き）
try:
    Base.metadata.create_all(bind=engine)
    logger.info("データベーステーブルを作成しました。")
except Exception as e:
    logger.error(f"データベーステーブル作成中にエラーが発生しました: {e}")
    logger.warning("アプリケーションは起動しますが、データベース機能は利用できません。")

# FastAPIアプリケーションを作成
app = FastAPI(
    title=settings.app_name,
    description="HakoPitaのストレージデータ管理用FastAPIアプリケーション",
    version=VERSION,
    debug=settings.debug,
)

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを追加（prefixなし）
app.include_router(storage_router)


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "HakoPita FastAPI",
        "version": VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}


@app.get("/test")
async def test_endpoint():
    """テスト用エンドポイント（データベース接続なし）"""
    return {
        "message": "Test endpoint working",
        "env": os.getenv("ENV", "unknown")
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """グローバル例外ハンドラー"""
    logger.error(f"Unhandled exception: {exc}")
    return {"error": "Internal server error", "detail": str(exc)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)
