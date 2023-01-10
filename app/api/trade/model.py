from sqlalchemy import Column, String, SmallInteger, Boolean, Integer, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from app.api.model import Base


class ShoppingCart(Base):
    """购物车"""
    __tablename__ = 't_shopping_chart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)  # 用户ID
    goods_id = Column(Integer, index=True)  # 商品
    goods_num = Column(Integer, default=0)  # 商品数量


class ShoppingOrder(Base):
    """购物订单"""
    __tablename__ = 't_shopping_order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)  # 用户ID
    user_address_id = Column(Integer, index=True)  # 用户地址ID
    order_sn = Column(String(64), nullable=False, unique=True)  # 订单编号
    order_mount = Column(Integer, default=0.0)  # 订单金额
    order_post = Column(String(128))  # 订单留言

    pay_type = Column(SmallInteger)  # 1微信2支付宝
    pay_status = Column(SmallInteger, default=1)  # 1待支付2成功3超时关闭4交易结束5交易成功
    pay_time = Column(DateTime)


class ShoppingOrderGoods(Base):
    """订单内商品"""
    __tablename__ = 't_shopping_order_goods'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, index=True)  # 订单ID
    goods_id = Column(Integer, index=True)  # 商品ID
    goods_num = Column(Integer, default=0)


class RaffleActivity(Base):
    """抽奖活动"""
    __tablename__ = 't_raffle_activity'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))  # 活动名称
    description = Column(String(2048))  # 活动详情
    start_time = Column(DateTime)  # 活动开始时间
    end_time = Column(DateTime)  # 活动开始时间
    image_id = Column(Integer)  # 活动图片
    appendix = Column(ARRAY(Integer))  # 活动附件


class RafflePrize(Base):
    """抽奖"""
    # https://juejin.cn/post/6989208605375332389
    # https://juejin.cn/post/6844903488229638152
    __tablename__ = 't_raffle_prize'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))  # 名称
    weight = Column(Integer)  # 奖品的权重
    stock_count = Column(Integer)  # 库存
    enable_stock = Column(Boolean, default=True)


class RaffleLog(Base):
    """中奖日志"""
    __tablename__ = 't_raffle_log'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, index=True)  # 用户ID
    prize_id = Column(Integer)  # 奖品ID
