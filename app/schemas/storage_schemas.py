from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class StorageDataBase(BaseModel):
    """ストレージデータの基本スキーマ"""

    storage_data_id: str = Field(..., description="ストレージデータID")
    storage_category: int = Field(..., description="ストレージカテゴリ（0: Box, 1: Shelf）")
    shop_id: int = Field(..., description="ショップID")
    item_id: str = Field(..., description="アイテムID")
    item_title: str = Field(..., description="アイテムタイトル")
    item_url: str = Field(..., description="アイテムURL")
    primary_image_url: str = Field(..., description="メイン画像URL")
    image_url_list: List[str] = Field(..., description="画像URLリスト")
    price: float = Field(..., description="価格")
    ean: Optional[str] = Field(None, description="EANコード")
    height: float = Field(..., description="高さ")
    width: float = Field(..., description="幅")
    depth: float = Field(..., description="奥行き")
    colors: List[int] = Field(..., description="色のリスト")
    materials: List[int] = Field(..., description="素材のリスト")
    updated_at: datetime = Field(..., description="更新日時")
    seller_name: Optional[str] = Field(None, description="販売者名")
    box_likelihood: Optional[float] = Field(None, description="ボックス確率")
    box_features: Optional[List[int]] = Field(None, description="ボックス特徴")
    shelf_likelihood: Optional[float] = Field(None, description="棚確率")
    shelf_features: Optional[List[int]] = Field(None, description="棚特徴")
    shelf_genres: Optional[List[int]] = Field(None, description="棚ジャンル")


class StorageDataResponse(StorageDataBase):
    """ストレージデータレスポンススキーマ"""

    model_config = ConfigDict(from_attributes=True)


class StorageDataListResponse(BaseModel):
    """ストレージデータリストレスポンススキーマ"""

    data: List[StorageDataResponse] = Field(..., description="ストレージデータリスト")


class SearchStorageRequest(BaseModel):
    """ストレージ検索リクエストスキーマ"""

    # サイズパラメータ
    width: Optional[float] = Field(None, description="幅")
    width_lower_limit: Optional[float] = Field(None, description="幅の下限")
    width_upper_limit: Optional[float] = Field(None, description="幅の上限")
    use_width_range: Optional[bool] = Field(False, description="幅の範囲指定を使用")

    depth: Optional[float] = Field(None, description="奥行き")
    depth_lower_limit: Optional[float] = Field(None, description="奥行きの下限")
    depth_upper_limit: Optional[float] = Field(None, description="奥行きの上限")
    use_depth_range: Optional[bool] = Field(False, description="奥行きの範囲指定を使用")

    height: Optional[float] = Field(None, description="高さ")
    height_lower_limit: Optional[float] = Field(None, description="高さの下限")
    height_upper_limit: Optional[float] = Field(None, description="高さの上限")
    use_height_range: Optional[bool] = Field(False, description="高さの範囲指定を使用")

    # その他のパラメータ
    storage_category: Optional[int] = Field(
        0, description="ストレージカテゴリ（0: Box, 1: Shelf）"
    )
    country_code: Optional[str] = Field("jp", description="国コード（jp/us）")
    enable_inverted_search: Optional[bool] = Field(False, description="反転検索を有効にする")

    # ページネーション
    page: Optional[int] = Field(0, description="ページ番号")
    page_size: Optional[int] = Field(2000, description="ページサイズ")


class SearchStorageResponse(BaseModel):
    """ストレージ検索レスポンススキーマ"""

    total_items: int = Field(..., description="総アイテム数")
    total_pages: int = Field(..., description="総ページ数")
    page: int = Field(..., description="現在のページ番号")
    page_size: int = Field(..., description="ページサイズ")
    has_more: bool = Field(..., description="次のページがあるか")
    next_page_url: Optional[str] = Field(None, description="次のページのURL")
    data: List[StorageDataResponse] = Field(..., description="ストレージデータリスト")


class FetchStorageRequest(BaseModel):
    """ストレージ取得リクエストスキーマ"""

    id_list: str = Field(..., description="カンマ区切りのストレージデータIDリスト")


class ErrorResponse(BaseModel):
    """エラーレスポンススキーマ"""

    error: str = Field(..., description="エラーメッセージ")
    detail: Optional[str] = Field(None, description="詳細エラー情報") 