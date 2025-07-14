import logging
import sys
from typing import Optional

from app.db.session import settings


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """ログ設定をセットアップする"""

    # ログレベルを設定
    level = log_level or settings.log_level
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # ロガーを作成
    logger = logging.getLogger("hakopita_fast_api")
    logger.setLevel(numeric_level)

    # 既存のハンドラーをクリア
    logger.handlers.clear()

    # コンソールハンドラーを作成
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)

    # フォーマッターを作成
    # フォーマッターにライン番号も含めるように修正
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # ハンドラーをロガーに追加
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "hakopita_fast_api") -> logging.Logger:
    """ロガーを取得する"""
    return logging.getLogger(name)
