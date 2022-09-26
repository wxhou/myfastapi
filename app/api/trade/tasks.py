import traceback
from sqlalchemy import update

from celery.utils.log import get_task_logger
from app.core.celery_app import celery
from app.core.db import engine
from app.utils.asyfunc import sync_run_async
from ..goods.model import Goods
from ..trade.model import ShoppingCart



logger = get_task_logger(__name__)


@celery.task
@sync_run_async
async def update_inventory(args: list):
    """更新库存"""
    try:
        async with engine.begin() as db:
            for arg in args:
                await db.execute(update(Goods).where(Goods.id==arg['goods_id'], Goods.status==0).values(goods_num=Goods.goods_num+arg['goods_num']))
            await db.commit()
    except Exception:
        logger.critical(traceback.format_exc())
    finally:
        await engine.dispose()


@celery.task
@sync_run_async
async def update_cart(goods, current_user_id):
    """更新购物车"""
    try:
        async with engine.begin() as db:
            for gd in goods:
                await db.execute(update(ShoppingCart).where(
                    ShoppingCart.user_id==current_user_id,
                    ShoppingCart.goods_id==gd.goods_id,
                    ShoppingCart.status==0).values(
                        goods_num=ShoppingCart.goods_num-gd.goods_num))
            await db.commit()
    except Exception:
        logger.critical(traceback.format_exc())
    finally:
        await engine.dispose()