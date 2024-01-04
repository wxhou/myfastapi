import traceback
from sqlalchemy import update

from celery.utils.log import get_task_logger
from app.core.celery_app import celery
from app.extensions import session
from app.api.goods.model import Goods
from app.api.trade.model import ShoppingCart



logger = get_task_logger(__name__)


@celery.task
def update_inventory_task(args: list):
    """更新库存"""
    with session() as db:
        with db.begin():
            for arg in args:
                db.execute(update(Goods).where(Goods.id==arg['goods_id'], Goods.status==0).values(goods_num=Goods.goods_num+arg['goods_num']))
            db.commit()


@celery.task
def update_cart_task(goods, current_user_id):
    """更新购物车"""
    with session() as db:
        with db.begin():
            for gd in goods:
                db.execute(update(ShoppingCart).where(
                    ShoppingCart.user_id==current_user_id,
                    ShoppingCart.goods_id==gd.goods_id,
                    ShoppingCart.status==0).values(
                        goods_num=ShoppingCart.goods_num-gd.goods_num))
            db.commit()