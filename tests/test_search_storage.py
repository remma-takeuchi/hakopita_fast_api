import logging
from app.core.logging import setup_logging

# ログ設定をセットアップ
setup_logging("DEBUG")
logger = logging.getLogger(__name__)


def test_search_storage_with_width(setup_database, test_client):
    """幅パラメータでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with width parameter")

    response = test_client.get("/search_storage?width=20&storage_category=0&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    assert "page" in data
    assert "page_size" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Width parameter response: {data}")


def test_search_storage_with_height(setup_database, test_client):
    """高さパラメータでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with height parameter")

    response = test_client.get("/search_storage?height=30&storage_category=0&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Height parameter response: {data}")


def test_search_storage_with_depth(setup_database, test_client):
    """奥行きパラメータでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with depth parameter")

    response = test_client.get("/search_storage?depth=25&storage_category=0&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Depth parameter response: {data}")


def test_search_storage_with_multiple_params(setup_database, test_client):
    """複数パラメータでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with multiple parameters")

    response = test_client.get(
        "/search_storage?width=20&height=30&depth=25&storage_category=0&country_code=jp"
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Multiple parameters response: {data}")


def test_search_storage_with_range_params(setup_database, test_client):
    """範囲パラメータでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with range parameters")

    response = test_client.get(
        "/search_storage?width_lower_limit=15&width_upper_limit=25&use_width_range=true&storage_category=0&country_code=jp"
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Range parameters response: {data}")


def test_search_storage_with_pagination(setup_database, test_client):
    """ページネーション付きでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with pagination")

    response = test_client.get("/search_storage?width=20&page=0&page_size=10&storage_category=0&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    assert "page" in data
    assert data["page"] == 0
    assert "page_size" in data
    assert data["page_size"] == 10
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Pagination response: {data}")


def test_search_storage_no_params(setup_database, test_client):
    """パラメータなしでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with no parameters")

    response = test_client.get("/search_storage")

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    logger.info(f"No parameters error response: {data}")


def test_search_storage_invalid_params(setup_database, test_client):
    """無効なパラメータでのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with invalid parameters")

    response = test_client.get("/search_storage?width=-10&storage_category=0&country_code=jp")

    # 負の値は検証エラーではなく、検索結果が空になる
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    # 負の値での検索は結果が空になることを期待
    assert data["total_items"] == 0
    
    # search_storageではimage_url_listが含まれないことを確認（空の結果でも）
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Invalid parameters response: {data}")


def test_search_storage_with_country_code(setup_database, test_client):
    """国コード指定でのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with country code")

    response = test_client.get("/search_storage?width=20&country_code=us&storage_category=0")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Country code response: {data}")


def test_search_storage_with_storage_category(setup_database, test_client):
    """ストレージカテゴリ指定でのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with storage category")

    response = test_client.get("/search_storage?width=20&storage_category=1&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Storage category response: {data}")


def test_search_storage_with_inverted_search(setup_database, test_client):
    """反転検索でのsearch_storage APIのテスト"""
    logger.info("Starting search_storage API test with inverted search")

    response = test_client.get("/search_storage?width=20&enable_inverted_search=true&storage_category=0&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # search_storageではimage_url_listが含まれないことを確認
    if data["data"]:
        for item in data["data"]:
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info(f"Inverted search response: {data}")


def test_search_storage_schema_validation(setup_database, test_client):
    """search_storageのスキーマ検証テスト"""
    logger.info("Starting search_storage schema validation test")

    response = test_client.get("/search_storage?width=20&storage_category=0&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    
    # レスポンス構造の検証
    assert "total_items" in data
    assert "total_pages" in data
    assert "page" in data
    assert "page_size" in data
    assert "has_more" in data
    assert "data" in data
    
    # データアイテムの構造検証（image_url_listが含まれないことを確認）
    if data["data"]:
        for item in data["data"]:
            # 必須フィールドの存在確認
            assert "storage_data_id" in item
            assert "storage_category" in item
            assert "shop_id" in item
            assert "item_id" in item
            assert "item_title" in item
            assert "item_url" in item
            assert "primary_image_url" in item
            assert "price" in item
            assert "height" in item
            assert "width" in item
            assert "depth" in item
            assert "colors" in item
            assert "materials" in item
            assert "updated_at" in item
            
            # image_url_listが含まれないことを確認
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
    
    logger.info("Search_storage schema validation test completed")
