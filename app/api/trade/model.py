from sqlalchemy import Column, String, SmallInteger, Integer, DateTime, Boolean, Text
from app.api.model import Base



class ShoppingCart(Base):
    """购物车"""
    __tablename__ = 't_shopping_chart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True) # 用户ID
    goods_id = Column(Integer, index=True) # 商品


class ShoppingOrder(Base):
    """购物订单"""
    __tablename__ = 't_shopping_order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True) # 用户ID
    user_address_id = Column(Integer, index=True) # 用户地址ID
    order_sn = Column(String(64), nullable=False, unique=True) # 订单编号
    order_mount = Column(Integer, default=0.0) # 订单金额
    order_post = Column(String(128)) # 订单留言

    pay_status = Column(SmallInteger, default=1) # 1待支付2成功3超时关闭4交易结束5交易成功
    pay_time = Column(DateTime)


class ShoppingOrderGoods(Base):
    """订单内商品"""
    __tablename__ = 't_shopping_order_goods'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, index=True) # 订单ID
    goods_id = Column(Integer, index=True) # 商品ID
    goods_num = Column(Integer, default=0)