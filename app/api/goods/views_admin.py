import json
from celery.schedules import crontab
from sqlalchemy import or_, select, update
from fastapi import APIRouter, Depends, Query, Security
from app.common.pagation import PageNumberPagination
from app.core.celery_app import redis_scheduler_entry
from app.common.response import ErrCode, response_ok, response_err
from app.extensions import get_db, get_redis, AsyncSession, aioredis, limiter, websocket
from app.utils.logger import logger
from app.utils.randomly import random_str
from app.api.user.model import BaseUser
from app.api.user.auth import get_current_active_user
from .model import Goods, GoodsCategory
from .schemas import GoodsInsert, GoodsUpdate
from .tasks import add_goods_click_task



router_goods_admin = APIRouter()


@router_goods_admin.get('/category/', summary='商品分类列表')
async def goods_category_list(
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user)
):
    """商品分类列表"""
    query_filter = [GoodsCategory.status == 0]
    objs = await db.scalars(select(GoodsCategory).filter(*query_filter))
    return response_ok(data=[obj.to_dict() for obj in objs])



@router_goods_admin.get('/list/', summary='商品列表')
async def goods_list(
    search: str = Query(default=None),
    paginate: PageNumberPagination = Depends(),
):
    """商品列表"""
    query_filter = [Goods.status == 0]
    if search:
        query_filter.append(or_(Goods.goods_name.ilike(f'%{search}%'), Goods.goods_sn.ilike(f"{search}")))
    res = await paginate(Goods, query_filter)
    return response_ok(**res)


@router_goods_admin.get('/info/', summary='商品详情')
async def goods_info(
    goods_id: int = Query(..., description='商品ID'),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
):
    obj = await db.scalar(select(Goods).where(Goods.id==goods_id, Goods.status==0))
    if obj is None:
        return response_err(ErrCode.GOODS_NOT_FOUND)
    add_goods_click_task.delay(goods_id)
    await websocket.broadcast(json.dumps({'data': 'foobar'}))
    return response_ok(data=obj.to_dict())



@router_goods_admin.post('/insert/', summary='新建商品')
async def goods_insert(
    goods: GoodsInsert,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['goods_insert'])
):
    """更新用户信息"""
    args = goods.model_dump(exclude_none=True)
    args['goods_sn'] = random_str()
    obj = Goods(**args)
    db.add(obj)
    await db.commit()
    if _num := args.get("goods_num"):
        await redis.set(f"goods_num_{args['id']}", _num)
    await redis_scheduler_entry.save('hellogoods', 'app.api.goods.tasks.hello_goods',
                                      crontab(), args=(obj.id,))
    return response_ok(data={"id": obj.id})


@router_goods_admin.put('/update/', summary='更新商品')
async def goods_update(
    goods: GoodsUpdate,
    goods_id: int = Query(default=True, ge=1, description='商品ID'),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['goods_update'])
):
    """更新用户信息"""
    args = goods.model_dump(exclude_none=True)
    obj: Goods = await db.scalar(select(Goods).where(Goods.id==goods_id, Goods.status==0))
    if obj is None:
        return response_err(ErrCode.GOODS_NOT_FOUND)
    await db.execute(update(Goods).where(Goods.id==goods_id, Goods.status==0).values(**args))
    await db.commit()
    if _num := args.get("goods_num"):
        await redis.set(f"goods_num_{args['id']}", _num)
    return response_ok(data=obj.to_dict())


@router_goods_admin.delete('/delete/', summary='删除商品')
async def goods_delete(
    goods_id: int = Query(ge=1, description='商品ID'),
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user, scopes=['goods_delete'])
):
    """更新用户信息"""
    await db.execute(update(Goods).where(Goods.id==goods_id, Goods.status==0).values(status=-1))
    await db.commit()
    return response_ok()
