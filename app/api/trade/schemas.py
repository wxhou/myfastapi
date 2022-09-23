from typing import Optional, List
from pydantic import BaseModel, Field



class ShoppingChartInsert(BaseModel):
    goods_id: int = Field(title='商品ID', ge=1)
    goods_num: int = Field(title='商品数量', ge=0)


class ShoppingChartDelete(BaseModel):
    goods_id: int = Field(title='商品ID', ge=1)


class ShoppingOrderInsert(BaseModel):
    address_id: int = Field(title='地址ID', ge=1)
    goods: List[ShoppingChartInsert] = Field(title='商品')
    order_post: str = Field(title='商品数量', max_length=128)


class ShoppingOrderDelete(BaseModel):
    order_id: int = Field(title='地址ID', ge=1)