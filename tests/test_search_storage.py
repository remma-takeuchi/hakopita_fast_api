import logging
from app.core.logging import setup_logging

# ログ設定をセットアップ
setup_logging("DEBUG")
logger = logging.getLogger(__name__)


def test_search_storage_with_width(setup_database, test_client):
    """幅パラメータでのsearch_storage APIのテスト"""
    logger.info("幅パラメータでのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?width=20")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    assert "page" in data
    assert "page_size" in data
    logger.info(f"幅パラメータレスポンス: {data}")


def test_search_storage_with_height(setup_database, test_client):
    """高さパラメータでのsearch_storage APIのテスト"""
    logger.info("高さパラメータでのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?height=30")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    logger.info(f"高さパラメータレスポンス: {data}")


def test_search_storage_with_depth(setup_database, test_client):
    """奥行きパラメータでのsearch_storage APIのテスト"""
    logger.info("奥行きパラメータでのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?depth=25")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    logger.info(f"奥行きパラメータレスポンス: {data}")


def test_search_storage_with_multiple_params(setup_database, test_client):
    """複数パラメータでのsearch_storage APIのテスト"""
    logger.info("複数パラメータでのsearch_storage APIのテストを開始")

    response = test_client.get(
        "/dev/search_storage?width=20&height=30&depth=25&storage_category=0&country_code=jp"
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    logger.info(f"複数パラメータレスポンス: {data}")


def test_search_storage_with_range_params(setup_database, test_client):
    """範囲パラメータでのsearch_storage APIのテスト"""
    logger.info("範囲パラメータでのsearch_storage APIのテストを開始")

    response = test_client.get(
        "/dev/search_storage?width_lower_limit=15&width_upper_limit=25&use_width_range=true"
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    logger.info(f"範囲パラメータレスポンス: {data}")


def test_search_storage_with_pagination(setup_database, test_client):
    """ページネーション付きでのsearch_storage APIのテスト"""
    logger.info("ページネーション付きでのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?width=20&page=0&page_size=10")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    assert "page" in data
    assert data["page"] == 0
    assert "page_size" in data
    assert data["page_size"] == 10
    logger.info(f"ページネーション付きレスポンス: {data}")


def test_search_storage_no_params(setup_database, test_client):
    """パラメータなしでのsearch_storage APIのテスト"""
    logger.info("パラメータなしでのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage")

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    logger.info(f"パラメータなしエラーレスポンス: {data}")


def test_search_storage_invalid_params(setup_database, test_client):
    """無効なパラメータでのsearch_storage APIのテスト"""
    logger.info("無効なパラメータでのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?width=-10")

    # 負の値は検証エラーではなく、検索結果が空になる
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_items" in data
    # 負の値での検索は結果が空になることを期待
    assert data["total_items"] == 0
    logger.info(f"無効パラメータレスポンス: {data}")


def test_search_storage_with_country_code(setup_database, test_client):
    """国コード指定でのsearch_storage APIのテスト"""
    logger.info("国コード指定でのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?width=20&country_code=us")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    logger.info(f"国コード指定レスポンス: {data}")


def test_search_storage_with_storage_category(setup_database, test_client):
    """ストレージカテゴリ指定でのsearch_storage APIのテスト"""
    logger.info("ストレージカテゴリ指定でのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?width=20&storage_category=1")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    logger.info(f"ストレージカテゴリ指定レスポンス: {data}")


def test_search_storage_with_inverted_search(setup_database, test_client):
    """反転検索でのsearch_storage APIのテスト"""
    logger.info("反転検索でのsearch_storage APIのテストを開始")

    response = test_client.get("/dev/search_storage?width=20&enable_inverted_search=true")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    logger.info(f"反転検索レスポンス: {data}")
