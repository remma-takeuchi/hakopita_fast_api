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


@pytest.fixture(scope="function")
def setup_database_with_active_data(test_engine):
    """active=True/Falseを含むテスト用データベースをセットアップ"""
    # 既存のテーブルを削除してから再作成
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # active=True/Falseを含むテストデータを準備
    add_test_data_with_active_status(test_engine)
        
    yield
    
    # テスト終了後にテーブルを削除
    Base.metadata.drop_all(bind=test_engine)


def add_test_data(test_engine, num_items=10):
    """テストデータを追加（既存の関数）"""
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
                country_code="jp",
                active=True,
            ))
        db.commit()
    finally:
        db.close()


def add_test_data_with_active_status(test_engine):
    """active=Trueとactive=Falseを含むテストデータを追加"""
    # テスト用セッションファクトリを作成
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    db = TestingSessionLocal()
    try:
        # active=Trueのデータ（5件）
        for i in range(1, 6):
            db.add(StorageData(
                storage_data_id=f"active_true_{i}",
                storage_category=i % 2,
                shop_id=i % 5,
                item_id=f"item_active_{i}",
                item_title=f"Active Item {i}",
                item_url=f"https://example.com/item_active_{i}",
                primary_image_url=f"https://example.com/item_active_{i}.jpg",
                image_url_list=[f"https://example.com/item_active_{i}.jpg"],
                materials=[0,1,2],
                colors=[0,1,2],
                price=i * 100,
                ean=f"ean_active_{i}",
                height=i * 10,
                width=i * 10,
                depth=i * 10,
                country_code="jp",
                active=True,
            ))
        
        # active=Falseのデータ（5件）
        for i in range(1, 6):
            db.add(StorageData(
                storage_data_id=f"active_false_{i}",
                storage_category=i % 2,
                shop_id=i % 5,
                item_id=f"item_inactive_{i}",
                item_title=f"Inactive Item {i}",
                item_url=f"https://example.com/item_inactive_{i}",
                primary_image_url=f"https://example.com/item_inactive_{i}.jpg",
                image_url_list=[f"https://example.com/item_inactive_{i}.jpg"],
                materials=[0,1,2],
                colors=[0,1,2],
                price=i * 100,
                ean=f"ean_inactive_{i}",
                height=i * 10,
                width=i * 10,
                depth=i * 10,
                country_code="jp",
                active=False,
            ))
        
        db.commit()
        logger.info("Test data added: 5 active=True items, 5 active=False items")
    finally:
        db.close()


@pytest.fixture(scope="function")
def setup_inverted_search_database(test_engine):
    """反転検索テスト用データベースをセットアップ"""
    # 既存のテーブルを削除してから再作成
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # 反転検索専用のテストデータを準備
    add_inverted_search_test_data(test_engine)
        
    yield
    
    # テスト終了後にテーブルを削除
    Base.metadata.drop_all(bind=test_engine)


def add_inverted_search_test_data(test_engine):
    """反転検索テスト用のテストデータを追加"""
    # テスト用セッションファクトリを作成
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    db = TestingSessionLocal()
    try:
        # 1. 幅20cm、奥行き30cm、高さ25cm
        db.add(StorageData(
            storage_data_id="width_20_depth_30_height_25",
            storage_category=0,
            shop_id=1,
            item_id="item_1",
            item_title="width_20_depth_30_height_25_title",
            item_url="https://example.com/item_1",
            primary_image_url="https://example.com/item_1.jpg",
            image_url_list=["https://example.com/item_1.jpg"],
            materials=[],
            colors=[],
            price=1000,
            ean="ean_1",
            height=25,
            width=20,
            depth=30,
            country_code="jp",
            active=True,
        ))
        
        # 2. 幅30cm、奥行き20cm、高さ25cm
        db.add(StorageData(
            storage_data_id="width_30_depth_20_height_25",
            storage_category=0,
            shop_id=2,
            item_id="item_2",
            item_title="width_30_depth_20_height_25_title",
            item_url="https://example.com/item_2",
            primary_image_url="https://example.com/item_2.jpg",
            image_url_list=["https://example.com/item_2.jpg"],
            materials=[],
            colors=[],
            price=2000,
            ean="ean_2",
            height=25,
            width=30,
            depth=20,
            country_code="jp",
            active=True,
        ))
        
        # 3. 幅25cm、奥行き35cm、高さ25cm（範囲検索用）
        db.add(StorageData(
            storage_data_id="width_25_depth_35_height_25",
            storage_category=0,
            shop_id=3,
            item_id="item_3",
            item_title="width_25_depth_35_height_25_title",
            item_url="https://example.com/item_3",
            primary_image_url="https://example.com/item_3.jpg",
            image_url_list=["https://example.com/item_3.jpg"],
            materials=[],
            colors=[],
            price=3000,
            ean="ean_3",
            height=25,
            width=25,
            depth=35,
            country_code="jp",
            active=True,
        ))
        
        # 4. 幅35cm、奥行き25cm、高さ25cm（範囲検索用）
        db.add(StorageData(
            storage_data_id="width_35_depth_25_height_25",
            storage_category=0,
            shop_id=4,
            item_id="item_4",
            item_title="width_35_depth_25_height_25_title",
            item_url="https://example.com/item_4",
            primary_image_url="https://example.com/item_4.jpg",
            image_url_list=["https://example.com/item_4.jpg"],
            materials=[],
            colors=[],
            price=4000,
            ean="ean_4",
            height=25,
            width=35,
            depth=25,
            country_code="jp",
            active=True,
        ))
        
        # 5. 幅20cm、奥行き30cm、高さ30cm（高さテスト用）
        db.add(StorageData(
            storage_data_id="width_20_depth_30_height_30",
            storage_category=0,
            shop_id=5,
            item_id="item_5",
            item_title="width_20_depth_30_height_30_title",
            item_url="https://example.com/item_5",
            primary_image_url="https://example.com/item_5.jpg",
            image_url_list=["https://example.com/item_5.jpg"],
            materials=[],
            colors=[],
            price=5000,
            ean="ean_5",
            height=30,
            width=20,
            depth=30,
            country_code="jp",
            active=True,
        ))
        
        db.commit()
    finally:
        db.close()
