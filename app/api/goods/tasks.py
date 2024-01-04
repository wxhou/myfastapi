from sqlalchemy import update
from celery.utils.log import get_task_logger
from app.core.celery_app import celery
from app.extensions import session, redis_client
from .model import Goods


logger = get_task_logger(__name__)


@celery.task(queue='weblog_transient')
def add_goods_click_task(obj_id):
    """增加商品点击数"""
    with session() as db:
        with db.begin():
            db.execute(update(Goods).where(Goods.id==obj_id, Goods.status==0).values(click_num=Goods.click_num+1))
            db.commit()
    redis_client.incr("add_goods_click_num", 1)