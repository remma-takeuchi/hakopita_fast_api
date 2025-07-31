import json
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.types import Text as _Text
from sqlalchemy.types import TypeDecorator

from app.db.session import Base


class JSONEncodedDict(TypeDecorator):
    """JSONエンコードされた辞書を扱うためのカスタム型"""

    impl = _Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class StorageData(Base):
    """ストレージデータのSQLAlchemyモデル"""

    __tablename__ = "storage_table"

    # プライマリキー
    storage_data_id = Column(String(255), primary_key=True, index=True)

    # 基本情報
    storage_category = Column(Integer, nullable=False, index=True)
    shop_id = Column(Integer, nullable=False, index=True)
    item_id = Column(String(255), nullable=False, index=True)
    item_title = Column(Text, nullable=False)
    item_url = Column(Text, nullable=False)
    primary_image_url = Column(Text, nullable=False)
    image_url_list = Column(JSONEncodedDict, nullable=False)
    price = Column(Float, nullable=False)
    ean = Column(String(256), nullable=True)
    country_code = Column(String(256), nullable=False)
    active = Column(Boolean, nullable=False)

    # サイズ情報
    height = Column(Float, nullable=False, index=True)
    width = Column(Float, nullable=False, index=True)
    depth = Column(Float, nullable=False, index=True)

    # 属性情報
    colors = Column(JSONEncodedDict, nullable=False)
    materials = Column(JSONEncodedDict, nullable=False)

    # メタデータ
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    seller_name = Column(String(256), nullable=True)

    # AI分析結果
    box_likelihood = Column(Float, nullable=True)
    box_features = Column(JSONEncodedDict, nullable=True)
    shelf_likelihood = Column(Float, nullable=True)
    shelf_features = Column(JSONEncodedDict, nullable=True)
    shelf_genres = Column(JSONEncodedDict, nullable=True)

    def __repr__(self):
        return f"<StorageData(storage_data_id='{self.storage_data_id}', item_title='{self.item_title}')>"

    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            "storage_data_id": self.storage_data_id,
            "storage_category": self.storage_category,
            "shop_id": self.shop_id,
            "item_id": self.item_id,
            "item_title": self.item_title,
            "item_url": self.item_url,
            "primary_image_url": self.primary_image_url,
            "image_url_list": self.image_url_list,
            "price": self.price,
            "ean": self.ean,
            "height": self.height,
            "width": self.width,
            "depth": self.depth,
            "colors": self.colors,
            "materials": self.materials,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "seller_name": self.seller_name,
            "box_likelihood": self.box_likelihood,
            "box_features": self.box_features,
            "shelf_likelihood": self.shelf_likelihood,
            "shelf_features": self.shelf_features,
            "shelf_genres": self.shelf_genres,
            "country_code": self.country_code,
            "active": self.active,
        }
