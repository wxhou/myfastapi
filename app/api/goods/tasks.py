from fastapi import Depends
from sqlalchemy import select
from asgiref.sync import async_to_sync
from app.core.celery_app import celery
from app.core.redis import init_redis_pool
from app.core.db import async_session
from .model import Goods



@celery.task(queue='transient')
def add_goods_click_num(_key, num):
    """增加商品点击数"""
    async def goods_click_num(_key, num):
        redis = await init_redis_pool()
        await redis.incr(num)

    async_to_sync(goods_click_num)(_key, num)
