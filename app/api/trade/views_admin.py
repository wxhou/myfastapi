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
from .model import ShoppingCart, ShoppingOrder, ShoppingOrderGoods
from .schemas import ShoppingChartInsert, ShoppingChartDelete, ShoppingOrderInsert, ShoppingOrderDelete
from .tasks import update_inventory, update_cart
from ..goods.model import Goods
from ..base.model import UserAddress


router_trade_admin = APIRouter()


@router_trade_admin.get('/shopping/chart/', summary='购物车列表')
async def trade_shopping_list(request: Request,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, ge=1),
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Depends(check_user_permission('trade_shopping_list'))):
    """购物车列表"""
    query_filter = [ShoppingCart.status == 0, ShoppingCart.user_id==current_user.id]
    objs = await db.scalars(select(ShoppingCart).where(*query_filter).limit(page_size).offset((page - 1) * page))
    result_data = []
    for obj in objs:
        goods_obj = await db.scalar(select(Goods).where(Goods.id==obj.goods_id, Goods.status==0))
        items = {
            "goods": jsonable_encoder(goods_obj, exclude={'status'}),
            "goods_num": obj.goods_num
        }
        result_data.append(items)
    _count = await db.scalar(select(func.count()).filter(*query_filter))
    pages = int(ceil(_count / float(page_size)))
    return response_ok(data=result_data, total=_count, pages=pages)


@router_trade_admin.post('/shopping/insert/', summary='购物车新增商品')
async def trade_shopping_insert(request: Request,
        args: ShoppingChartInsert,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        current_user: BaseUser = Depends(check_user_permission('trade_shopping_insert'))):
    """购物车新增"""
    _key_name = f"goods_num_{args.goods_id}"
    rs1_num = await redis.get(_key_name)
    if rs1_num and int(rs1_num) < 1:
        return response_err(ErrCode.GOODS_SELL_OUT)
    rs2_num = await db.scalar(select(Goods.goods_num).where(Goods.id==args.goods_id, Goods.status==0))
    if rs1_num != rs2_num:
        await redis.set(_key_name, rs2_num)
    if rs2_num <1:
        return response_err(ErrCode.GOODS_SELL_OUT)
    if args.goods_num > rs2_num:
        return response_err(ErrCode.GOODS_NUM_NOT_ENOUGH)
    obj = ShoppingCart(
        user_id=current_user.id,
        goods_id=args.goods_id,
        goods_num=args.goods_num
    )
    db.add(obj)
    await db.commit()
    await redis.decr(_key_name, args.goods_num)
    update_inventory.delay([{"goods_id": args.goods_id, "goods_num": -args.goods_num}])
    return response_ok()


@router_trade_admin.post('/shopping/delete/', summary='购物车删除商品')
async def trade_shopping_delete(request: Request,
        args: ShoppingChartDelete,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        current_user: BaseUser = Depends(check_user_permission('trade_shopping_delete'))):
    """购物车删除"""
    good_num = await db.scalar(select(ShoppingCart.goods_num).where(ShoppingCart.user_id==current_user.id,
                                                                    ShoppingCart.goods_id==args.goods_id))
    sql = update(ShoppingCart).where(ShoppingCart.user_id==current_user.id,
                                               ShoppingCart.goods_id==args.goods_id)
    if good_num > 0:
        await db.execute(sql.values(goods_num=ShoppingCart.goods_num-1))
    else:
        await db.execute(sql.values(status=-1))
    await db.commit()
    await redis.incr(f"goods_num_{args.goods_id}", 1)
    update_inventory.delay([{"goods_id": args.goods_id, "goods_num": 1}])
    return response_ok()


@router_trade_admin.post('/order/insert/', summary='新增订单')
async def trade_order_insert(request: Request,
        args: ShoppingOrderInsert,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        current_user: BaseUser = Depends(check_user_permission('trade_order_insert'))):
    """新增订单"""
    obj = ShoppingOrder(user_id=current_user.id,
                order_sn=snow_flake.get_id(),
                user_address_id=args.address_id,
                order_post=args.order_post)
    db.add(obj)
    await db.flush()
    db.add_all(
        [
            ShoppingOrderGoods(order_id=obj.id,
            goods_id=obj.goods_id,
            goods_num=obj.goods_num) for obj in args.goods
        ]
    )
    await db.commit()
    update_cart.delay(args.goods, current_user.id)
    return response_ok(data={"id": obj.id, "order_sn": obj.order_sn})


@router_trade_admin.get('/order/info/', summary='订单详情')
async def trade_order_info(request: Request,
        order_id : int = Query(description='订单ID'),
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        current_user: BaseUser = Depends(check_user_permission('trade_order_info'))):
    """详情订单"""
    obj = await db.scalar(select(ShoppingOrder).where(ShoppingOrder.id==order_id,
                                                      ShoppingOrder.user_id==current_user.id,
                                                      ShoppingOrder.status==0))
    if obj is None:
        return response_err(ErrCode.ORDER_NOT_FOUND)
    result = jsonable_encoder(obj, exclude={'status'})
    addr_obj = await db.scalar(select(UserAddress).where(UserAddress.id==result['user_address_id'],
                                                         UserAddress.status==0))
    result['address_info'] = jsonable_encoder(addr_obj, exclude={'status'})
    order_goods_objs = await db.scalars(select(ShoppingOrderGoods).where(ShoppingOrderGoods.order_id==result['id'],
                                                                   ShoppingOrderGoods.status==0))
    result['goods_info'] = []
    for order_good_obj in order_goods_objs:
        goods_obj = await db.scalar(select(Goods).where(Goods.id==order_good_obj.goods_id,
                                                        Goods.status==0))
        items = jsonable_encoder(goods_obj, exclude={'goods_num', 'status'})
        items['goods_num'] = order_good_obj.goods_num
        result['goods_info'].append(items)
    return response_ok(data=result)


@router_trade_admin.post('/order/delete/', summary='删除订单')
async def trade_order_delete(request: Request,
        args: ShoppingOrderDelete,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        current_user: BaseUser = Depends(check_user_permission('trade_order_delete'))):
    """删除订单"""
    obj = await db.scalar(select(ShoppingOrder).where(ShoppingOrder.id==args.order_id,
                                                      ShoppingOrder.user_id==current_user.id,
                                                      ShoppingOrder.status==0))
    if obj is None:
        return response_err(ErrCode.ORDER_NOT_FOUND)
    await db.execute(update(ShoppingOrder).where(ShoppingOrder.id==args.order_id,
                                                ShoppingOrder.user_id==current_user.id,
                                                ShoppingOrder.status==0).values(status=-1))
    await db.commit()
    shop_order_objs = await db.scalars(select(ShoppingOrderGoods).where(
        ShoppingOrderGoods.order_id==args.order_id, ShoppingOrderGoods.status==0))
    update_inventory.delay([{"goods_id": obj.goods_id, "goods_num": -obj.goods_num}
                            for obj in shop_order_objs])
    return response_ok()