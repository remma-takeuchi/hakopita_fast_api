import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.storage_model import Base, StorageData
import logging
from app.core.logging import setup_logging
from fastapi.testclient import TestClient
from app.db.session import get_db
from app.main import app

# ログ設定をセットアップ
setup_logging("DEBUG")
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def test_engine():
    """テスト用SQLiteエンジンを作成"""
    # テスト用データベースファイルのパス
    test_db_path = "./test.db"
    
    # SQLite用のエンジンを作成
    engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False}
    )
    
    # テストデータベースを作成
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    engine.dispose() 
       
    # SQLiteファイル自体を削除
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """テスト用セッションファクトリを作成"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def test_client(test_engine):
    """テスト用クライアントを作成"""

    # テスト用セッションファクトリを作成
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    def override_get_db():
        """テスト用のデータベースセッションを取得"""
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # データベースの依存関係をオーバーライド
    app.dependency_overrides[get_db] = override_get_db
    
    # テストクライアントを作成
    client = TestClient(app)
    
    yield client
    
    # クリーンアップ
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def setup_database(test_engine):
    """テスト用データベースをセットアップ"""
    # 既存のテーブルを削除してから再作成
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # テストデータを準備
    add_test_data(test_engine, num_items=10)
        
    yield
    
    # テスト終了後にテーブルを削除
    Base.metadata.drop_all(bind=test_engine)


def add_test_data(test_engine, num_items=10):
    """テストデータを追加"""
    # テスト用セッションファクトリを作成
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    db = TestingSessionLocal()
    try:
        for i in range(1, num_items):
            db.add(StorageData(
                storage_data_id=f"test_{i}",
                storage_category=i % 2,
                shop_id=i % 5,
                item_id=f"item_{i}",
                item_title=f"item_{i}_title",
                item_url=f"https://example.com/item_{i}",
                primary_image_url=f"https://example.com/item_{i}.jpg",
                image_url_list=[f"https://example.com/item_{i}.jpg"],
                materials=[0,1,2],
                colors=[0,1,2],
                price=i * 100,
                ean=f"ean_{i}",
                height=i * 10,
                width=i * 10,
                depth=i * 10,
            ))
        db.commit()
    finally:
        db.close()
