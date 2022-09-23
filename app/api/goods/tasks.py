import traceback
from sqlalchemy import update
from asgiref.sync import async_to_sync
from celery.utils.log import get_task_logger
from app.core.celery_app import celery
from app.core.db import engine
from .model import Goods


logger = get_task_logger(__name__)


@celery.task(queue='transient')
def add_goods_click_num(obj_id):
    """增加商品点击数"""
    async def goods_click_num(obj_id):
        try:
            async with engine.begin() as db:
                await db.execute(update(Goods).where(Goods.id==obj_id, Goods.status==0).values(click_num=Goods.click_num+1))
                await db.commit()
        except Exception:
            logger.critical(traceback.format_exc())
        finally:
            await engine.dispose()
    async_to_sync(goods_click_num)(obj_id)
