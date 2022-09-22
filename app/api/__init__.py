# 把模型在此引入才能被alembic检测到
from .base.model import BaseUser, BaseRole, BasePermission, UploadModel, UserAddress, UserCollect, UserComment
from .blog.model import Category, Post, Comment
from .device.model import DeviceInfo
from .goods.model import Goods, GoodsCategory, GoodsCategoryBrand, HotSearchWord
from .trade.model import ShoppingCart, ShoppingOrder, ShoppingOrderGoods