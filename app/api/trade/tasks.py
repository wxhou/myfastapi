import traceback
from sqlalchemy import update

from celery.utils.log import get_task_logger
from app.core.celery_app import celery
from app.extensions.db import async_session
from app.common.decorator import sync_run_async
from ..goods.model import Goods
from ..trade.model import ShoppingCart



logger = get_task_logger(__name__)


@celery.task
@sync_run_async
async def update_inventory(args: list):
    """更新库存"""
    async with async_session() as session:
        async with session.begin():
            for arg in args:
                await session.execute(update(Goods).where(Goods.id==arg['goods_id'], Goods.status==0).values(goods_num=Goods.goods_num+arg['goods_num']))
            await session.commit()


@celery.task
@sync_run_async
async def update_cart(goods, current_user_id):
    """更新购物车"""
    async with async_session() as session:
        async with session.begin():
            for gd in goods:
                await session.execute(update(ShoppingCart).where(
                    ShoppingCart.user_id==current_user_id,
                    ShoppingCart.goods_id==gd.goods_id,
                    ShoppingCart.status==0).values(
                        goods_num=ShoppingCart.goods_num-gd.goods_num))
            await session.commit()