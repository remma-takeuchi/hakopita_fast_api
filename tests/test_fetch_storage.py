import logging
from app.core.logging import setup_logging

# ログ設定をセットアップ（DEBUGレベルで）
setup_logging("DEBUG")
logger = logging.getLogger(__name__)

def test_fetch_storage_success(setup_database, test_client):
    """正常なfetch_storage APIのテスト"""
    logger.info("=== 正常なfetch_storage APIのテストを開始 ===")

    # テストデータを準備
    test_ids = ["test_1", "test_2", "test_3"]
    logger.info(f"テストID: {test_ids}")

    # APIを呼び出し
    response = test_client.get(f"/dev/fetch_storage?id_list={','.join(test_ids)}")

    # レスポンスを検証
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == len(test_ids)
    logger.info(f"レスポンス: {data}")
    logger.info("=== 正常なfetch_storage APIのテスト完了 ===")


def test_fetch_storage_empty_id_list(setup_database, test_client):
    """空のIDリストでのfetch_storage APIのテスト"""
    logger.info("=== 空のIDリストでのfetch_storage APIのテストを開始 ===")

    response = test_client.get("/dev/fetch_storage?id_list=")

    # 空のIDリストの場合は200で空のデータが返される
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 0
    logger.info(f"空リストレスポンス: {data}")
    logger.info("=== 空のIDリストでのfetch_storage APIのテスト完了 ===")


def test_fetch_storage_missing_id_list(setup_database, test_client):
    """IDリストパラメータが不足している場合のテスト"""
    logger.info("=== IDリストパラメータ不足のテストを開始 ===")

    response = test_client.get("/dev/fetch_storage")

    assert response.status_code == 422  # Validation error
    logger.info(f"バリデーションエラーレスポンス: {response.json()}")
    logger.info("=== IDリストパラメータ不足のテスト完了 ===")


def test_fetch_storage_invalid_ids(setup_database, test_client):
    """無効なIDでのfetch_storage APIのテスト"""
    logger.info("=== 無効なIDでのfetch_storage APIのテストを開始 ===")

    response = test_client.get("/dev/fetch_storage?id_list=invalid_id_1,invalid_id_2")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 0  # 無効なIDなので空のリストが返される
    logger.info(f"無効IDレスポンス: {data}")
    logger.info("=== 無効なIDでのfetch_storage APIのテスト完了 ===")


def test_fetch_storage_single_id(setup_database, test_client):
    """単一IDでのfetch_storage APIのテスト"""
    logger.info("=== 単一IDでのfetch_storage APIのテストを開始 ===")

    response = test_client.get("/dev/fetch_storage?id_list=single_test_id")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    logger.info(f"単一IDレスポンス: {data}")
    logger.info("=== 単一IDでのfetch_storage APIのテスト完了 ===")


def test_fetch_storage_with_spaces(setup_database, test_client):
    """スペースを含むIDリストでのfetch_storage APIのテスト"""
    logger.info("=== スペースを含むIDリストでのfetch_storage APIのテストを開始 ===")

    response = test_client.get("/dev/fetch_storage?id_list= id1 , id2 , id3 ")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    logger.info(f"スペース含みレスポンス: {data}")
    logger.info("=== スペースを含むIDリストでのfetch_storage APIのテスト完了 ===")
