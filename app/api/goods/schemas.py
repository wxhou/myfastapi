
from typing import Optional
from pydantic import BaseModel, Field



class GoodsInsert(BaseModel):
    """新建商品"""
    category_id: int = Field(description='分类ID', ge=1)
    goods_name: str = Field(description='商品名称', min_length=1, max_length=64)
    market_price: int = Field(default=0, description='市场价格')
    shop_price: int = Field(default=0, description='本店价格')
    goods_brief: Optional[str] = Field(default=None, description='商品描述', min_length=1, max_length=512)
    goods_image: int = Field(default=True, description='商品图片', ge=1)
    goods_cover: int = Field(default=True, description='商品缩略图', ge=1)


class GoodsUpdate(BaseModel):
    """更新商品"""
    category_id: Optional[int] = Field(default=None, description='分类ID', ge=1)
    goods_name: Optional[str] = Field(default=None, description='商品名称', min_length=1, max_length=64)
    goods_num: Optional[int] = Field(default=None, description='商品库存', ge=0)
    market_price: Optional[int] = Field(default=None, description='市场价格')
    shop_price: Optional[int] = Field(default=None, description='本店价格')
    goods_brief: Optional[str] = Field(default=None, description='商品描述', min_length=1, max_length=512)
    goods_image: Optional[int] = Field(default=None, description='商品图片', ge=1)
    goods_cover: Optional[int] = Field(default=None, description='商品缩略图', ge=1)