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
        query = query.filter(
            StorageData.storage_category == params.storage_category
        )

        # 国コードでフィルタ
        query = query.filter(StorageData.country_code == params.country_code)
        
        # アクティブフラグでフィルタ
        query = query.filter(StorageData.active == True)
        
        # 幅・奥行きの条件を生成する
        wd_conditions = []
        is_width_specified = False
        is_depth_specified = False

        # 幅の処理
        if (
            params.use_width_range
            and params.width_lower_limit is not None
            and params.width_upper_limit is not None
        ):
            wd_conditions.append(
                between(
                    StorageData.width,
                    params.width_lower_limit,
                    params.width_upper_limit,
                )
            )
            is_width_specified = True
        elif params.width is not None:
            tolerance = 0.5
            wd_conditions.append(
                between(
                    StorageData.width,
                    params.width - tolerance,
                    params.width + tolerance,
                )
            )
            is_width_specified = True

        # 奥行きの処理
        if (
            params.use_depth_range
            and params.depth_lower_limit is not None
            and params.depth_upper_limit is not None
        ):
            wd_conditions.append(
                between(
                    StorageData.depth,
                    params.depth_lower_limit,
                    params.depth_upper_limit,
                )
            )
            is_depth_specified = True
        elif params.depth is not None:
            tolerance = 0.5
            wd_conditions.append(
                between(
                    StorageData.depth,
                    params.depth - tolerance,
                    params.depth + tolerance,
                )
            )
            is_depth_specified = True
        
        # 反転検索が有効かつ、幅と奥行きのいずれかが指定されている場合は、反転検索の条件を作成
        if all([
            params.enable_inverted_search,
            (is_width_specified or is_depth_specified)
        ]):
            # 反転検索の場合：幅と奥行きを入れ替えて検索
            inverted_wd_conditions = self._get_inverted_conditions(params)
            
            # 元の幅・奥行きと、反転の幅・奥行きをORで結合
            query = query.filter(or_(and_(True, *wd_conditions), and_(True, *inverted_wd_conditions)))
        
        # 反転検索が無効の場合は、幅・奥行きの条件をANDで結合
        else:
            query = query.filter(and_(True, *wd_conditions))

        # 高さの処理
        height_conditions = []
        if (
            params.use_height_range
            and params.height_lower_limit is not None
            and params.height_upper_limit is not None
        ):
            height_conditions.append(
                between(
                    StorageData.height,
                    params.height_lower_limit,
                    params.height_upper_limit,
                )
            )
        elif params.height is not None:
            tolerance = 0.5  # デフォルトの許容範囲
            height_conditions.append(
                between(
                    StorageData.height,
                    params.height - tolerance,
                    params.height + tolerance,
                )
            )
        
        if height_conditions:
            query = query.filter(and_(True, *height_conditions))
        
        print(query.statement)
        return query.all()

    def _get_inverted_conditions(self, params: SearchStorageRequest) -> List[Any]:
        """反転検索の条件を生成"""
 
        inverted_conditions = []
        
        # 幅と奥行きの条件を入れ替えて新しい条件を生成
        for dim in ['width', 'depth']:
            inverted_dim = 'depth' if dim == 'width' else 'width'
            
            # 範囲指定の場合
            use_range_key = f'use_{dim}_range'
            if getattr(params, use_range_key, False):
                lower_limit_key = f'{dim}_lower_limit'
                upper_limit_key = f'{dim}_upper_limit'
                lower_limit = getattr(params, lower_limit_key)
                upper_limit = getattr(params, upper_limit_key)
                
                if lower_limit is not None and upper_limit is not None:
                    if inverted_dim == 'width':
                        inverted_conditions.append(
                            between(StorageData.width, lower_limit, upper_limit)
                        )
                    else:
                        inverted_conditions.append(
                            between(StorageData.depth, lower_limit, upper_limit)
                        )
            
            # 単一値指定の場合
            elif getattr(params, dim, None) is not None:
                tolerance = 0.5  # デフォルトの許容範囲
                value = getattr(params, dim)
                
                if inverted_dim == 'width':
                    inverted_conditions.append(
                        between(StorageData.width, value - tolerance, value + tolerance)
                    )
                else:
                    inverted_conditions.append(
                        between(StorageData.depth, value - tolerance, value + tolerance)
                    )
        return inverted_conditions

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