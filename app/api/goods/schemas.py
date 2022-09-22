
from typing import Optional
from pydantic import BaseModel, Field



class GoodsInsert(BaseModel):
    """新建商品"""
    category_id: int = Field(title='分类ID', ge=1)
    goods_name: str = Field(title='商品名称', min_length=1, max_length=64)
    market_price: int = Field(default=0, title='市场价格')
    shop_price: int = Field(default=0, title='本店价格')
    goods_brief: Optional[str] = Field(default=None, title='商品描述', min_length=1, max_length=512)
    goods_image: int = Field(default=True, title='商品图片', ge=1)
    goods_cover: int = Field(default=True, title='商品缩略图', ge=1)


class GoodsUpdate(BaseModel):
    """更新商品"""
    id: int = Field(ge=1, title='商品ID')
    category_id: int = Field(default=None, title='分类ID', ge=1)
    goods_name: str = Field(default=None, title='商品名称', min_length=1, max_length=64)
    market_price: int = Field(default=None, title='市场价格')
    shop_price: int = Field(default=None, title='本店价格')
    goods_brief: Optional[str] = Field(default=None, title='商品描述', min_length=1, max_length=512)
    goods_image: int = Field(default=None, title='商品图片', ge=1)
    goods_cover: int = Field(default=None, title='商品缩略图', ge=1)


class GoodsDelete(BaseModel):
    """更新商品"""
    id: int = Field(ge=1, title='商品ID')