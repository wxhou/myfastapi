import traceback
from sqlalchemy import update
from celery.utils.log import get_task_logger
from app.core.celery_app import celery
from app.extensions.db import async_session
from app.extensions.redis import redis
from app.common.decorator import sync_run_async
from .model import Goods


logger = get_task_logger(__name__)


@celery.task(queue='transient')
@sync_run_async
async def add_goods_click_num(obj_id):
    """增加商品点击数"""
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(Goods).where(Goods.id==obj_id, Goods.status==0).values(click_num=Goods.click_num+1))
            await session.commit()
    redis.incr("add_goods_click_num", 1)

@celery.task
def hello_goods(obj_id):
    """商品测试"""
    print('hello good', obj_id)