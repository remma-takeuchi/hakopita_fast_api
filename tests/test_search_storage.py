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


def test_search_storage_active_behavior(setup_database_with_active_data, test_client):
    """search_storageでのactiveフィールドの挙動テスト"""
    logger.info("=== Starting search_storage active field behavior test ===")

    # search_storageではactive=Trueのデータのみが返されることを確認
    response = test_client.get("/search_storage?width=20&storage_category=0&country_code=jp")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    
    # search_storageではactive=Trueのデータのみが返されることを確認
    if data["data"]:
        data_count = len(data["data"])
        logger.info(f"Returned {data_count} active items only")
        for item in data["data"]:
            # image_url_listが含まれないことを確認
            assert "image_url_list" not in item, "search_storage should not include image_url_list"
            # active=Trueのデータのみが返されることを確認（storage_data_idで判定）
            assert item["storage_data_id"].startswith("active_true_"), f"Expected active=True item, got: {item['storage_data_id']}"
    
    logger.info(f"Active behavior response: {data}")
    logger.info("=== Search_storage active field behavior test completed ===")


# 反転検索専用テストパターン

def test_inverted_search_width_20cm(setup_inverted_search_database, test_client):
    """幅20cm検索での反転検索テスト - 通常2件、反転3件"""
    logger.info("幅20cm検索での反転検索テストを開始")

    # 通常検索（デフォルトでstorage_category=0）
    response_normal = test_client.get("/search_storage?width=20&storage_category=0&country_code=jp")
    assert response_normal.status_code == 200
    data_normal = response_normal.json()
    logger.info(f"幅20cm通常検索結果: {data_normal['total_items']}件")
    
    # 通常検索で返されたアイテムのIDを確認
    normal_ids = [item['storage_data_id'] for item in data_normal['data']]
    logger.info(f"通常検索でマッチしたID: {normal_ids}")

    # 反転検索（デフォルトでstorage_category=0）
    response_inverted = test_client.get("/search_storage?width=20&enable_inverted_search=true&storage_category=0&country_code=jp")
    assert response_inverted.status_code == 200
    data_inverted = response_inverted.json()
    logger.info(f"幅20cm反転検索結果: {data_inverted['total_items']}件")
    
    # 反転検索で返されたアイテムのIDを確認  
    inverted_ids = [item['storage_data_id'] for item in data_inverted['data']]
    logger.info(f"反転検索でマッチしたID: {inverted_ids}")

    # 期待される結果：
    # 通常検索: width=20でマッチ → width_20_depth_30_height_25, width_20_depth_30_height_30 (2件)
    # 反転検索: width=20 OR depth=20でマッチ → 上記2件 + width_30_depth_20_height_25 (3件)
    assert data_normal["total_items"] == 2
    assert data_inverted["total_items"] == 3

    # 反転検索で結果が増えることを確認
    assert data_inverted["total_items"] > data_normal["total_items"]


def test_inverted_search_depth_20cm(setup_inverted_search_database, test_client):
    """奥行き20cm検索での反転検索テスト - 通常1件、反転3件"""
    logger.info("奥行き20cm検索での反転検索テストを開始")

    # 通常検索（デフォルトでstorage_category=0）
    response_normal = test_client.get("/search_storage?depth=20&storage_category=0&country_code=jp")
    assert response_normal.status_code == 200
    data_normal = response_normal.json()
    logger.info(f"奥行き20cm通常検索結果: {data_normal['total_items']}件")
    
    normal_ids = [item['storage_data_id'] for item in data_normal['data']]
    print(f"通常検索でマッチしたID: {normal_ids}")

    # 反転検索（デフォルトでstorage_category=0）
    response_inverted = test_client.get("/search_storage?depth=20&enable_inverted_search=true&storage_category=0&country_code=jp")
    assert response_inverted.status_code == 200
    data_inverted = response_inverted.json()
    logger.info(f"奥行き20cm反転検索結果: {data_inverted['total_items']}件")
    
    inverted_ids = [item['storage_data_id'] for item in data_inverted['data']]
    print(f"反転検索でマッチしたID: {inverted_ids}")

    print(f"通常検索件数: {data_normal['total_items']}, 反転検索件数: {data_inverted['total_items']}")
    
    # 期待される結果：
    # 通常検索: depth=20でマッチ → width_30_depth_20_height_25 (1件)
    # 反転検索: depth=20 OR width=20でマッチ → width_30_depth_20_height_25 + width_20_depth_30_height_25 + width_20_depth_30_height_30 (3件)
    assert data_normal["total_items"] == 1
    assert data_inverted["total_items"] == 3

    # 反転検索で結果が増えることを確認
    assert data_inverted["total_items"] > data_normal["total_items"]


def test_inverted_search_height_30cm(setup_inverted_search_database, test_client):
    """高さ30cm検索での反転検索テスト - 通常1件、反転5件"""
    logger.info("高さ30cm検索での反転検索テストを開始")

    # 通常検索（デフォルトでstorage_category=0）
    response_normal = test_client.get("/search_storage?height=30&storage_category=0&country_code=jp")
    assert response_normal.status_code == 200
    data_normal = response_normal.json()
    logger.info(f"高さ30cm通常検索結果: {data_normal['total_items']}件")
    
    normal_ids = [item['storage_data_id'] for item in data_normal['data']]
    print(f"通常検索でマッチしたID: {normal_ids}")

    # 反転検索（デフォルトでstorage_category=0）
    response_inverted = test_client.get("/search_storage?height=30&enable_inverted_search=true&storage_category=0&country_code=jp")
    assert response_inverted.status_code == 200
    data_inverted = response_inverted.json()
    logger.info(f"高さ30cm反転検索結果: {data_inverted['total_items']}件")
    
    inverted_ids = [item['storage_data_id'] for item in data_inverted['data']]
    print(f"反転検索でマッチしたID: {inverted_ids}")

    print(f"通常検索件数: {data_normal['total_items']}, 反転検索件数: {data_inverted['total_items']}")
    
    # 期待される結果：
    # 通常検索: height=30でマッチ → width_20_depth_30_height_30 (1件)
    # 反転検索: 高さは反転対象外なので同じ結果 → width_20_depth_30_height_30 (1件)
    assert data_normal["total_items"] == 1
    assert data_inverted["total_items"] == 1

    # 高さは反転対象外なので結果が変わらないことを確認
    assert data_inverted["total_items"] == data_normal["total_items"]


def test_inverted_search_width_range_20_30cm(setup_inverted_search_database, test_client):
    """幅20-30cm範囲検索での反転検索テスト - 通常4件、反転5件"""
    logger.info("幅20-30cm範囲検索での反転検索テストを開始")

    # 通常検索（デフォルトでstorage_category=0）
    response_normal = test_client.get(
        "/search_storage?width_lower_limit=20&width_upper_limit=30&use_width_range=true&storage_category=0&country_code=jp"
    )
    assert response_normal.status_code == 200
    data_normal = response_normal.json()
    logger.info(f"幅20-30cm範囲通常検索結果: {data_normal['total_items']}件")
    
    normal_ids = [item['storage_data_id'] for item in data_normal['data']]
    print(f"通常検索でマッチしたID: {normal_ids}")

    # 反転検索（デフォルトでstorage_category=0）
    response_inverted = test_client.get(
        "/search_storage?width_lower_limit=20&width_upper_limit=30&use_width_range=true&enable_inverted_search=true&storage_category=0&country_code=jp"
    )
    assert response_inverted.status_code == 200
    data_inverted = response_inverted.json()
    logger.info(f"幅20-30cm範囲反転検索結果: {data_inverted['total_items']}件")
    
    inverted_ids = [item['storage_data_id'] for item in data_inverted['data']]
    print(f"反転検索でマッチしたID: {inverted_ids}")

    print(f"通常検索件数: {data_normal['total_items']}, 反転検索件数: {data_inverted['total_items']}")
    
    # 期待される結果：
    # 通常検索: width=20-30でマッチ → width_20_depth_30_height_25, width_30_depth_20_height_25, width_25_depth_35_height_25, width_20_depth_30_height_30 (4件)
    # 反転検索: width=20-30 OR depth=20-30でマッチ → 上記4件 + width_35_depth_25_height_25 (5件)
    assert data_normal["total_items"] == 4
    assert data_inverted["total_items"] == 5

    # 反転検索で結果が増えることを確認
    assert data_inverted["total_items"] > data_normal["total_items"]
