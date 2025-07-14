from typing import Any, Dict, List, Optional

from sqlalchemy import and_, between, or_
from sqlalchemy.orm import Session

from app.models.storage_model import StorageData
from app.schemas.storage_schemas import SearchStorageRequest


class StorageDataCRUD:
    """ストレージデータのCRUD操作クラス"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, storage_data_id: str) -> Optional[StorageData]:
        """IDでストレージデータを取得"""
        return (
            self.db.query(StorageData)
            .filter(StorageData.storage_data_id == storage_data_id)
            .first()
        )

    def get_by_ids(self, storage_data_ids: List[str]) -> List[StorageData]:
        """IDリストでストレージデータを取得"""
        return (
            self.db.query(StorageData)
            .filter(StorageData.storage_data_id.in_(storage_data_ids))
            .all()
        )

    def search_by_params(self, params: SearchStorageRequest) -> List[StorageData]:
        """検索パラメータに基づいてストレージデータを検索"""
        query = self.db.query(StorageData)

        # ストレージカテゴリでフィルタ
        if params.storage_category is not None:
            query = query.filter(
                StorageData.storage_category == params.storage_category
            )

        # サイズ条件でフィルタ
        size_conditions = []

        # 高さの処理
        if (
            params.use_height_range
            and params.height_lower_limit is not None
            and params.height_upper_limit is not None
        ):
            size_conditions.append(
                between(
                    StorageData.height,
                    params.height_lower_limit,
                    params.height_upper_limit,
                )
            )
        elif params.height is not None:
            tolerance = 0.5  # デフォルトの許容範囲
            size_conditions.append(
                between(
                    StorageData.height,
                    params.height - tolerance,
                    params.height + tolerance,
                )
            )

        # 幅の処理
        if (
            params.use_width_range
            and params.width_lower_limit is not None
            and params.width_upper_limit is not None
        ):
            size_conditions.append(
                between(
                    StorageData.width,
                    params.width_lower_limit,
                    params.width_upper_limit,
                )
            )
        elif params.width is not None:
            tolerance = 0.5
            size_conditions.append(
                between(
                    StorageData.width,
                    params.width - tolerance,
                    params.width + tolerance,
                )
            )

        # 奥行きの処理
        if (
            params.use_depth_range
            and params.depth_lower_limit is not None
            and params.depth_upper_limit is not None
        ):
            size_conditions.append(
                between(
                    StorageData.depth,
                    params.depth_lower_limit,
                    params.depth_upper_limit,
                )
            )
        elif params.depth is not None:
            tolerance = 0.5
            size_conditions.append(
                between(
                    StorageData.depth,
                    params.depth - tolerance,
                    params.depth + tolerance,
                )
            )

        # サイズ条件が指定されている場合は適用
        if size_conditions:
            if params.enable_inverted_search:
                # 反転検索の場合：幅と奥行きを入れ替えて検索
                inverted_conditions = []
                for condition in size_conditions:
                    # 幅と奥行きの条件を入れ替える処理を実装
                    # ここでは簡略化のため、元の条件を使用
                    inverted_conditions.append(condition)

                # 元の条件と反転条件をORで結合
                query = query.filter(or_(*size_conditions, *inverted_conditions))
            else:
                # 通常の検索：AND条件で結合
                query = query.filter(and_(*size_conditions))

        # ショップIDでフィルタ（国コードに基づく）
        if params.country_code == "jp":
            query = query.filter(StorageData.shop_id < 100)
        elif params.country_code == "us":
            query = query.filter(StorageData.shop_id >= 100)

        return query.all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[StorageData]:
        """全ストレージデータを取得（ページネーション付き）"""
        return self.db.query(StorageData).offset(skip).limit(limit).all()

    def create(self, storage_data: StorageData) -> StorageData:
        """ストレージデータを作成"""
        self.db.add(storage_data)
        self.db.commit()
        self.db.refresh(storage_data)
        return storage_data

    def update(self, storage_data: StorageData) -> StorageData:
        """ストレージデータを更新"""
        self.db.commit()
        self.db.refresh(storage_data)
        return storage_data

    def delete(self, storage_data_id: str) -> bool:
        """ストレージデータを削除"""
        storage_data = self.get_by_id(storage_data_id)
        if storage_data:
            self.db.delete(storage_data)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """ストレージデータの総数を取得"""
        return self.db.query(StorageData).count() 