import logging
from app.core.logging import setup_logging

# ログ設定をセットアップ（DEBUGレベルで）
setup_logging("DEBUG")
logger = logging.getLogger(__name__)

def test_fetch_storage_success(setup_database, test_client):
    """正常なfetch_storage APIのテスト"""
    logger.info("=== Starting normal fetch_storage API test ===")

    # テストデータを準備
    test_ids = ["test_1", "test_2", "test_3"]
    logger.info(f"Test IDs: {test_ids}")

    # APIを呼び出し
    response = test_client.get(f"/fetch_storage?id_list={','.join(test_ids)}")

    # レスポンスを検証
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == len(test_ids)
    
    # fetch_storageではimage_url_listが含まれることを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" in item, "fetch_storage should include image_url_list"
            assert isinstance(item["image_url_list"], list), "image_url_list should be a list"
    
    logger.info(f"Response: {data}")
    logger.info("=== Normal fetch_storage API test completed ===")


def test_fetch_storage_empty_id_list(setup_database, test_client):
    """空のIDリストでのfetch_storage APIのテスト"""
    logger.info("=== Starting fetch_storage API test with empty ID list ===")

    response = test_client.get("/fetch_storage?id_list=")

    # 空のIDリストの場合は200で空のデータが返される
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 0
    logger.info(f"Empty list response: {data}")
    logger.info("=== Fetch_storage API test with empty ID list completed ===")


def test_fetch_storage_missing_id_list(setup_database, test_client):
    """IDリストパラメータが不足している場合のテスト"""
    logger.info("=== Starting test for missing ID list parameter ===")

    response = test_client.get("/fetch_storage")

    assert response.status_code == 422  # Validation error
    logger.info(f"Validation error response: {response.json()}")
    logger.info("=== Test for missing ID list parameter completed ===")


def test_fetch_storage_invalid_ids(setup_database, test_client):
    """無効なIDでのfetch_storage APIのテスト"""
    logger.info("=== Starting fetch_storage API test with invalid IDs ===")

    response = test_client.get("/fetch_storage?id_list=invalid_id_1,invalid_id_2")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 0  # 無効なIDなので空のリストが返される
    logger.info(f"Invalid ID response: {data}")
    logger.info("=== Fetch_storage API test with invalid IDs completed ===")


def test_fetch_storage_single_id(setup_database, test_client):
    """単一IDでのfetch_storage APIのテスト"""
    logger.info("=== Starting fetch_storage API test with single ID ===")

    response = test_client.get("/fetch_storage?id_list=test_1")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # 単一IDでもimage_url_listが含まれることを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" in item, "fetch_storage should include image_url_list"
    
    logger.info(f"Single ID response: {data}")
    logger.info("=== Fetch_storage API test with single ID completed ===")


def test_fetch_storage_with_spaces(setup_database, test_client):
    """スペースを含むIDリストでのfetch_storage APIのテスト"""
    logger.info("=== Starting fetch_storage API test with spaces in ID list ===")

    response = test_client.get("/fetch_storage?id_list= test_1 , test_2 , test_3 ")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # スペース含みでもimage_url_listが含まれることを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" in item, "fetch_storage should include image_url_list"
    
    logger.info(f"Response with spaces: {data}")
    logger.info("=== Fetch_storage API test with spaces in ID list completed ===")


def test_fetch_storage_active_behavior(setup_database_with_active_data, test_client):
    """fetch_storageでのactiveフィールドの挙動テスト"""
    logger.info("=== Starting fetch_storage active field behavior test ===")

    # active=Trueとactive=Falseの両方のデータを含むIDリストをテスト
    test_ids = ["active_true_1", "active_true_2", "active_false_1", "active_false_2"]
    
    response = test_client.get(f"/fetch_storage?id_list={','.join(test_ids)}")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # fetch_storageではactiveの値に関係なく、リクエストされたIDのデータが返されることを確認
    assert len(data["data"]) == len(test_ids), f"Expected {len(test_ids)} items, got {len(data['data'])}"
    
    if data["data"]:
        data_count = len(data["data"])
        logger.info(f"Returned {data_count} items regardless of active status")
        for item in data["data"]:
            # image_url_listが含まれることを確認
            assert "image_url_list" in item, "fetch_storage should include image_url_list"
            # storage_data_idが期待されるIDのいずれかであることを確認
            assert item["storage_data_id"] in test_ids, f"Unexpected storage_data_id: {item['storage_data_id']}"
    
    logger.info(f"Active behavior response: {data}")
    logger.info("=== Fetch_storage active field behavior test completed ===")


def test_fetch_storage_active_true_only(setup_database_with_active_data, test_client):
    """fetch_storageでactive=Trueのデータのみをリクエストするテスト"""
    logger.info("=== Starting fetch_storage active=True only test ===")

    # active=Trueのデータのみをリクエスト
    test_ids = ["active_true_1", "active_true_2", "active_true_3"]
    
    response = test_client.get(f"/fetch_storage?id_list={','.join(test_ids)}")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # リクエストされたIDのデータが返されることを確認
    assert len(data["data"]) == len(test_ids)
    
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" in item, "fetch_storage should include image_url_list"
            assert item["storage_data_id"] in test_ids
    
    logger.info(f"Active=True only response: {data}")
    logger.info("=== Fetch_storage active=True only test completed ===")


def test_fetch_storage_active_false_only(setup_database_with_active_data, test_client):
    """fetch_storageでactive=Falseのデータのみをリクエストするテスト"""
    logger.info("=== Starting fetch_storage active=False only test ===")

    # active=Falseのデータのみをリクエスト
    test_ids = ["active_false_1", "active_false_2", "active_false_3"]
    
    response = test_client.get(f"/fetch_storage?id_list={','.join(test_ids)}")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # リクエストされたIDのデータが返されることを確認
    assert len(data["data"]) == len(test_ids)
    
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" in item, "fetch_storage should include image_url_list"
            assert item["storage_data_id"] in test_ids
    
    logger.info(f"Active=False only response: {data}")
    logger.info("=== Fetch_storage active=False only test completed ===")
