from sqlalchemy import select, update
from fastapi import APIRouter, Depends, Request, Query, Security
from fastapi.responses import Response
from app.extensions import get_db, get_redis, AsyncSession, AsyncRedis
from app.settings import settings
from app.common.pagation import PageNumberPagination
from app.common.response import ErrCode, response_ok, response_err
from app.utils.logger import logger
from app.utils.randomly import random_str
from app.utils.AliPay import ALIPAY, AlipayTradePagePayModel, AlipayTradePagePayRequest, verify_with_rsa
from app.api.user.model import BaseUser, BaseUserAddress
from app.api.goods.model import Goods
from app.api.base.auth import get_current_active_user
from .model import ShoppingCart, ShoppingOrder, ShoppingOrderGoods
from .schemas import ShoppingChartInsert, ShoppingOrderInsert
from .tasks import update_inventory_task, update_cart_task


router_trade_admin = APIRouter()


@router_trade_admin.get('/shopping/chart/', summary='购物车列表')
async def trade_shopping_list(
    paginate: PageNumberPagination = Depends(),
    current_user: BaseUser = Security(get_current_active_user, scopes=['trade_shopping_list'])
):
    """购物车列表"""
    query_filter = [ShoppingCart.status == 0, ShoppingCart.user_id==current_user.id]
    result = await paginate(ShoppingCart, query_filter)

    result_data = []
    for data in result['data']:
        goods_obj = await paginate.db.scalar(select(Goods).where(Goods.id==data['goods_id'], Goods.status==0))
        items = {
            "goods": goods_obj.to_dict(),
            "goods_num": data['goods_num']
        }
        result_data.append(items)
    return response_ok(data=result_data, total=result['total'], pages=result['pages'])


@router_trade_admin.post('/shopping/insert/', summary='购物车新增商品')
async def trade_shopping_insert(request: Request,
    args: ShoppingChartInsert,
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['trade_shopping_insert'])
):
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
    update_inventory_task.delay([{"goods_id": args.goods_id, "goods_num": -args.goods_num}])
    return response_ok()


@router_trade_admin.delete('/shopping/delete/', summary='购物车删除商品')
async def trade_shopping_delete(request: Request,
    goos_id: int = Query(description='商品ID', ge=1),
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['trade_shopping_delete'])
):
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
    update_inventory_task.delay([{"goods_id": args.goods_id, "goods_num": 1}])
    return response_ok()


@router_trade_admin.post('/order/insert/', summary='新增订单')
async def trade_order_insert(request: Request,
    args: ShoppingOrderInsert,
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['trade_order_insert'])
):
    """新增订单"""
    obj = ShoppingOrder(user_id=current_user.id,
                order_sn=random_str(),
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
    update_cart_task.delay(args.goods, current_user.id)
    return response_ok(data={"id": obj.id, "order_sn": obj.order_sn})


@router_trade_admin.get('/order/info/', summary='订单详情')
async def trade_order_info(request: Request,
    order_id : int = Query(description='订单ID'),
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['trade_order_info'])
):
    """详情订单"""
    obj = await db.scalar(select(ShoppingOrder).where(ShoppingOrder.id==order_id,
                                                      ShoppingOrder.user_id==current_user.id,
                                                      ShoppingOrder.status==0))
    if obj is None:
        return response_err(ErrCode.ORDER_NOT_FOUND)
    result = obj.to_dict()
    addr_obj = await db.scalar(select(BaseUserAddress).where(BaseUserAddress.id==result['user_address_id'],
                                                         BaseUserAddress.status==0))
    result['address_info'] = addr_obj.to_dict()
    order_goods_objs = await db.scalars(select(ShoppingOrderGoods).where(ShoppingOrderGoods.order_id==result['id'],
                                                                   ShoppingOrderGoods.status==0))
    result['goods_info'] = []
    for order_good_obj in order_goods_objs:
        goods_obj = await db.scalar(select(Goods).where(Goods.id==order_good_obj.goods_id,
                                                        Goods.status==0))
        items = goods_obj.to_dict(exclude={'goods_num', 'status'})
        items['goods_num'] = order_good_obj.goods_num
        result['goods_info'].append(items)
    return response_ok(data=result)


@router_trade_admin.get('/order/pay/', summary='订单支付')
async def trade_order_pay(request: Request,
    order_id : int = Query(description='订单ID'),
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['trade_order_info'])
):
    """详情订单"""
    # https://blog.csdn.net/tonny7501/article/details/103029757
    obj = await db.scalar(select(ShoppingOrder).where(ShoppingOrder.id==order_id,
                                                      ShoppingOrder.user_id==current_user.id,
                                                      ShoppingOrder.status==0))
    if obj is None:
        return response_err(ErrCode.ORDER_NOT_FOUND)
    order_goods_objs = await db.scalars(select(ShoppingOrderGoods).where(ShoppingOrderGoods.order_id==order_id,
                                                                   ShoppingOrderGoods.status==0))
    goods_price = await db.execute(select(Goods.id, Goods.shop_price).where(
        Goods.id.in_([x.goods_id for x in order_goods_objs]), Goods.status==0))
    goods_price_dict = dict(goods_price.all())
    model = AlipayTradePagePayModel()
    model.out_trade_no = obj.order_sn
    model.total_amount = sum(goods_price_dict.get(order_good_obj.goods_id) * order_good_obj.goods_num for order_good_obj in order_goods_objs)
    model.subject = 'weblog支付'
    model.timeout_express = '10m'
    pay_request = AlipayTradePagePayRequest(biz_model=model)
    pay_request.notify_url = request.url_for("trade_order_notice")
    pay_url = ALIPAY.client().page_execute(pay_request, http_method='GET')
    return response_ok(data={"url": pay_url, "order_id": order_id})
    # TODO WeChat支付
    return response_ok()


@router_trade_admin.post('/order/pay/notice/', summary='订单支付通知')
async def trade_order_notice(data: dict):
    sign, sign_type = data.pop('sign', None), data.pop('sign_type', None)
    params = sorted(data.items(), key=lambda e: e[0], reverse=False)
    message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()
    if verify_with_rsa(settings.ALIPAY_PUBLIC_KEY, message, sign):
        return Response('success')
    else:
        return Response('error')


@router_trade_admin.delete('/order/delete/', summary='删除订单')
async def trade_order_delete(request: Request,
    order_id: int = Query(description='订单ID', ge=1),
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis),
    current_user: BaseUser = Security(get_current_active_user, scopes=['trade_order_delete'])
):
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
    update_inventory_task.delay([{"goods_id": obj.goods_id, "goods_num": -obj.goods_num}
                            for obj in shop_order_objs])
    return response_ok()