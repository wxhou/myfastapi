from math import ceil
from datetime import timedelta
from sqlalchemy import func, or_, select, update
from fastapi import APIRouter, Depends, Request, Query
from app.api.deps import get_db, get_redis, MyRedis, AsyncSession
from app.core.settings import settings
from app.common.response import ErrCode, response_ok, response_err
from app.common.encoder import jsonable_encoder
from app.utils.logger import logger
from app.utils.snowflake import snow_flake
from app.api.base.model import BaseUser
from app.api.base.auth import check_user_permission, get_current_active_user
from .model import Goods, GoodsCategory
from .schemas import GoodsInsert, GoodsUpdate, GoodsDelete
from .tasks import add_goods_click_num



router_goods_admin = APIRouter()

@router_goods_admin.get('/category/', summary='商品分类列表')
async def goods_category_list(request: Request,
                        db: AsyncSession = Depends(get_db),
                        current_user: BaseUser = Depends(get_current_active_user)):
    """商品分类列表"""
    query_filter = [GoodsCategory.status == 0]
    objs = await db.scalars(select(GoodsCategory).filter(*query_filter))
    return response_ok(data=[jsonable_encoder(obj, exclude={'status'}) for obj in objs])



@router_goods_admin.get('/list/', summary='商品列表')
async def goods_list(request: Request,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, ge=1),
        search: str = Query(default=None),
        db: AsyncSession = Depends(get_db)):
    """商品列表"""
    query_filter = [Goods.status == 0]
    if search:
        query_filter.append(or_(Goods.goods_name.ilike(f'%{search}%'), Goods.goods_sn.ilike(f"{search}")))
    objs = await db.scalars(select(Goods).filter(*query_filter).limit(page_size).offset((page - 1) * page))
    _count = await db.scalar(select(func.count()).filter(*query_filter))
    pages = int(ceil(_count / float(page_size)))
    return response_ok(data=[jsonable_encoder(obj, exclude={'status'}) for obj in objs], total=_count, pages=pages)


@router_goods_admin.get('/info/', summary='商品详情')
async def goods_info(request: Request,
                    id: int = Query(..., description='商品ID'),
                    db: AsyncSession = Depends(get_db),
                    redis: MyRedis = Depends(get_redis)):
    obj = await db.scalar(select(Goods).where(Goods.id==id, Goods.status==0))
    if obj is None:
        return response_err(ErrCode.GOODS_NOT_FOUND)
    result = jsonable_encoder(obj, exclude={'status'})
    add_goods_click_num.delay(obj.id)
    return response_ok(data=result)



@router_goods_admin.post('/insert/', summary='新建商品')
async def goods_insert(
        request: Request,
        goods: GoodsInsert,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        current_user: BaseUser = Depends(check_user_permission('goods_insert'))):
    """更新用户信息"""
    args = goods.dict(exclude_none=True)
    args['goods_sn'] = snow_flake.get_id()
    obj = Goods(**args)
    db.add(obj)
    await db.commit()
    if _num := args.get("goods_num"):
        await redis.set(f"goods_num_{args['id']}", _num)
    return response_ok(data={"id": obj.id})


@router_goods_admin.post('/update/', summary='更新商品')
async def goods_update(
        request: Request,
        goods: GoodsUpdate,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        current_user: BaseUser = Depends(check_user_permission('goods_update'))):
    """更新用户信息"""
    args = goods.dict(exclude_none=True)
    obj = await db.scalar(select(Goods).where(Goods.id==args.get('id', None), Goods.status==0))
    if obj is None:
        return response_err(ErrCode.GOODS_NOT_FOUND)
    await db.execute(update(Goods).where(Goods.id==args.pop('id', None), Goods.status==0).values(**args))
    await db.commit()
    if _num := args.get("goods_num"):
        await redis.set(f"goods_num_{args['id']}", _num)
    return response_ok(data=jsonable_encoder(obj, exclude={'status'}))


@router_goods_admin.post('/delete/', summary='删除商品')
async def goods_delete(
        request: Request,
        goods: GoodsDelete,
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Depends(check_user_permission('goods_delete'))):
    """更新用户信息"""
    await db.execute(update(Goods).where(Goods.id==goods.id, Goods.status==0).values(status=-1))
    await db.commit()
    return response_ok()
