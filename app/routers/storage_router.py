from typing import List, Tuple, Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.storage_crud import StorageDataCRUD
from app.db.session import get_db, settings
from app.models.storage_model import StorageData
from app.schemas.storage_schemas import (
    ErrorResponse,
    SearchStorageRequest,
    SearchStorageResponse,
    StorageDataListResponse,
    StorageDataResponse,
)
from app.core.logging import get_logger

# ロガーを取得
logger = get_logger("hakopita_fast_api.storage")

# プレフィックスなしでAPIRouterを作成
router = APIRouter(tags=["storage"])


def convert_storage_data_safely(storage_data_list: List[StorageData]) -> Tuple[List[StorageDataResponse], List[str]]:
    """
    ストレージデータを安全にスキーマに変換する
    
    Returns:
        Tuple[List[StorageDataResponse], List[str]]: (成功したデータリスト, エラーメッセージリスト)
    """
    successful_data = []
    error_messages = []
    
    for i, storage_data in enumerate(storage_data_list):
        try:
            # モデルからスキーマに変換
            converted_data = StorageDataResponse.model_validate(storage_data)
            successful_data.append(converted_data)
        except Exception as e:
            # エラーが発生した場合はログに記録し、スキップ
            error_msg = f"データ変換エラー (index {i}, ID: {getattr(storage_data, 'storage_data_id', 'unknown')}): {str(e)}"
            error_messages.append(error_msg)
            # loggerを使ってwarningで出力
            logger.warning(error_msg)
    
    return successful_data, error_messages


@router.get("/fetch_storage", response_model=StorageDataListResponse)
async def fetch_storage(
    id_list: str = Query(..., description="カンマ区切りのストレージデータIDリスト"),
    db: Session = Depends(get_db),
):
    """
    指定されたIDリストに基づいてストレージデータを取得します。

    - **id_list**: カンマ区切りのストレージデータIDリスト
    """
    try:
        # IDリストをパース
        if not id_list:
            # 空の場合は空リストを返す
            return StorageDataListResponse(data=[])

        storage_data_ids = [id.strip() for id in id_list.split(",") if id.strip()]
        if not storage_data_ids:
            # 有効なIDが1つもない場合も空リストを返す
            return StorageDataListResponse(data=[])

        # CRUD操作を実行
        crud = StorageDataCRUD(db)
        storage_data_list = crud.get_by_ids(storage_data_ids)
        
        # 安全にスキーマに変換
        successful_data, error_messages = convert_storage_data_safely(storage_data_list)
        
        # エラーメッセージがある場合はログに記録
        if error_messages:
            logger.warning(f"{len(error_messages)}件のデータ変換エラーが発生しました")
        
        # 成功したデータのみを返却
        return StorageDataListResponse(data=successful_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/search_storage", response_model=SearchStorageResponse)
async def search_storage(
    # サイズパラメータ
    width: Optional[float] = Query(None, description="幅"),
    width_lower_limit: Optional[float] = Query(None, description="幅の下限"),
    width_upper_limit: Optional[float] = Query(None, description="幅の上限"),
    use_width_range: Optional[bool] = Query(False, description="幅の範囲指定を使用"),
    depth: Optional[float] = Query(None, description="奥行き"),
    depth_lower_limit: Optional[float] = Query(None, description="奥行きの下限"),
    depth_upper_limit: Optional[float] = Query(None, description="奥行きの上限"),
    use_depth_range: Optional[bool] = Query(False, description="奥行きの範囲指定を使用"),
    height: Optional[float] = Query(None, description="高さ"),
    height_lower_limit: Optional[float] = Query(None, description="高さの下限"),
    height_upper_limit: Optional[float] = Query(None, description="高さの上限"),
    use_height_range: Optional[bool] = Query(False, description="高さの範囲指定を使用"),
    # その他のパラメータ
    storage_category: Optional[int] = Query(
        0, description="ストレージカテゴリ（0: Box, 1: Shelf）"
    ),
    country_code: Optional[str] = Query("jp", description="国コード（jp/us）"),
    enable_inverted_search: Optional[bool] = Query(False, description="反転検索を有効にする"),
    # ページネーション
    page: Optional[int] = Query(0, description="ページ番号"),
    page_size: Optional[int] = Query(2000, description="ページサイズ"),
    db: Session = Depends(get_db),
):
    """
    サイズ条件に基づいてストレージデータを検索します。

    - **width**: 幅
    - **depth**: 奥行き
    - **height**: 高さ
    - **storage_category**: ストレージカテゴリ（0: Box, 1: Shelf）
    - **country_code**: 国コード（jp/us）
    - **page**: ページ番号
    - **page_size**: ページサイズ
    """
    try:
        # 検索パラメータを構築
        search_params = SearchStorageRequest(
            width=width,
            width_lower_limit=width_lower_limit,
            width_upper_limit=width_upper_limit,
            use_width_range=use_width_range,
            depth=depth,
            depth_lower_limit=depth_lower_limit,
            depth_upper_limit=depth_upper_limit,
            use_depth_range=use_depth_range,
            height=height,
            height_lower_limit=height_lower_limit,
            height_upper_limit=height_upper_limit,
            use_height_range=use_height_range,
            storage_category=storage_category,
            country_code=country_code,
            enable_inverted_search=enable_inverted_search,
            page=page,
            page_size=page_size,
        )

        # 少なくとも1つのサイズパラメータが必要
        if not any(
            [
                width,
                depth,
                height,
                (use_width_range and width_lower_limit and width_upper_limit),
                (use_depth_range and depth_lower_limit and depth_upper_limit),
                (use_height_range and height_lower_limit and height_upper_limit),
            ]
        ):
            raise HTTPException(
                status_code=400,
                detail="At least one of 'width', 'depth', or 'height' must be specified",
            )

        # CRUD操作を実行
        crud = StorageDataCRUD(db)
        all_results = crud.search_by_params(search_params)
        
        # 安全にスキーマに変換
        successful_data, error_messages = convert_storage_data_safely(all_results)
        
        # エラーメッセージがある場合はログに記録
        if error_messages:
            logger.debug(f"{len(error_messages)}件のデータ変換エラーが発生しました")

        # ページネーション処理（成功したデータに対して）
        total_items = len(successful_data)
        total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 1
        offset = page * page_size
        paginated_results = successful_data[offset : offset + page_size]
        has_more = offset + page_size < total_items

        # 次のページのURLを生成
        next_page_url = None
        if has_more:
            # 現在のURLパラメータを構築
            params = []
            if width is not None:
                params.append(f"width={width}")
            if depth is not None:
                params.append(f"depth={depth}")
            if height is not None:
                params.append(f"height={height}")
            if storage_category is not None:
                params.append(f"storage_category={storage_category}")
            if country_code is not None:
                params.append(f"country_code={country_code}")
            if enable_inverted_search is not None:
                params.append(f"enable_inverted_search={enable_inverted_search}")

            # ページネーションパラメータを追加
            params.append(f"page={page + 1}")
            params.append(f"page_size={page_size}")

            next_page_url = f"search_storage?{'&'.join(params)}"

        # レスポンスを生成
        return SearchStorageResponse(
            total_items=total_items,
            total_pages=total_pages,
            page=page,
            page_size=page_size,
            has_more=has_more,
            next_page_url=next_page_url,
            data=paginated_results,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 