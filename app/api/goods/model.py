from datetime import datetime
from sqlalchemy import Column, String, SmallInteger, Integer, BigInteger, Boolean, Text, DATETIME
from app.api.model import Base


class GoodsCategory(Base):
    """商品分类"""
    __tablename__ = 't_goods_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(32)) # 分类名称
    code = Column(String(32)) # 分类编号
    desc = Column(String(128)) # 分类描述
    parent_id = Column(Integer, default=0, index=True) # 父节点ID, 0为顶级节点


class GoodsCategoryBrand(Base):
    """宣传商标"""
    __tablename__ = 't_goods_category_brand'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, index=True) # 分类ID
    name = Column(String(32)) # 品牌名
    desc = Column(String(256)) # 品牌描述
    image_id = Column(Integer, index=True) # 图片ID


class Goods(Base):
    __tablename__ = 't_goods'
    id = Column(BigInteger, primary_key=True)
    category_id = Column(Integer, index=True, nullable=False) # 分类ID
    goods_name = Column(String(64)) # 商品名称
    goods_sn = Column(String(64), unique=True) # 商品唯一货号
    click_num = Column(Integer, default=0) # 商品点击数
    sold_num = Column(Integer, default=0) # 销售量
    comment_num = Column(Integer, default=0) # 评论数
    goods_num = Column(Integer, default=0) # 库存数
    market_price = Column(Integer, default=0) # 市场价格
    shop_price = Column(Integer, default=0) # 本店价格
    goods_brief = Column(String(512)) # 商品描述
    goods_image = Column(Integer, index=True) # 商品图片
    goods_cover = Column(Integer, index=True) # 商品缩略图
    ship_free = Column(Boolean, default=True) # 是否免运费
    is_new = Column(Boolean, default=False) # 是否新品
    is_hot = Column(Boolean, default=False) # 是否热销



class HotSearchWord(Base):
    """热搜词"""
    __tablename__ = 't_goods_hot_search'
    id = Column(BigInteger, primary_key=True)
    keyword = Column(String(128)) # 热搜词
    order_num = Column(Integer, default=0) # 排序