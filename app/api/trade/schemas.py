from typing import Optional, List
from pydantic import BaseModel, Field



class ShoppingChartInsert(BaseModel):
    goods_id: int = Field(description='商品ID', ge=1)
    goods_num: int = Field(description='商品数量', ge=0)


class ShoppingOrderInsert(BaseModel):
    address_id: int = Field(description='地址ID', ge=1)
    goods: List[ShoppingChartInsert] = Field(description='商品')
    order_post: str = Field(description='商品数量', max_length=128)