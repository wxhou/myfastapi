from math import ceil
from sqlalchemy import func, or_, select, update
from fastapi import APIRouter, Depends, Security, Request, Query, Header, WebSocket, WebSocketDisconnect
from app.api.deps import get_db, get_redis, MyRedis
from app.core.db import AsyncSession, engine
from app.core.settings import settings
from app.common.encoder import jsonable_encoder
from app.common.response import ErrCode, response_ok, response_err
from app.common.sockets import manager
from app.utils.logger import logger
from app.api.base.auth import get_current_active_user
from app.api.base.model import BaseUser
from .model import DeviceInfo
from .schemas import DeviceInsert, DeviceModify, DeviceDelete


router_device_admin = APIRouter()



@router_device_admin.post('/insert/', summary='创建设备')
async def device_insert(request: Request,
        args: DeviceInsert,
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Security(get_current_active_user, scopes=['admin'])):
    """新建设备"""
    obj = await db.scalar(select(DeviceInfo.id).filter(DeviceInfo.device_ip_addr==args.device_ip_addr,
                            DeviceInfo.device_mac_addr==args.device_mac_addr))
    if obj is not None:
        return response_err(ErrCode.QUERY_HAS_EXISTS)
    obj = DeviceInfo(**args.dict(exclude_none=True))
    db.add(obj)
    await db.flush()
    obj.generate_register_code(obj.device_type, obj.id)
    await db.commit()
    return response_ok(data={"id": obj.id})



@router_device_admin.post('/modify/', summary='修改设备')
async def device_modify(request: Request,
        args: DeviceModify,
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Security(get_current_active_user, scopes=['admin'])):
    """修改设备"""
    obj = await db.scalar(select(DeviceInfo).filter(DeviceInfo.id==args.id,
                            DeviceInfo.status==0,
                            DeviceInfo.is_registered==False))
    if obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await db.execute(update(DeviceInfo).filter(DeviceInfo.id==args.id,
                            DeviceInfo.status==0,
                            DeviceInfo.is_registered==False).values(args.dict(exclude={'id'}, exclude_none=True)))
    await db.commit()
    return response_ok(data=jsonable_encoder(obj, exclude={'status'}))


@router_device_admin.get('/list/', summary='设备列表')
async def device_list(
        request: Request,
        page: int = Query(default=1, ge=1, title='页码'),
        page_size: int = Query(default=15, ge=1, title='每页数量'),
        device_name: str = Query(default=None, title='设备名称'),
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Security(get_current_active_user, scopes=['admin'])):
    """设备列表信息"""
    query_filter = [DeviceInfo.status == 0]
    if device_name:
        query_filter.append(DeviceInfo.device_name.ilike(f'%{device_name}%'))
    objs = (await db.scalars(select(DeviceInfo).filter(
        *query_filter).limit(page_size).offset((page - 1) * page))).all()
    _count = await db.scalar(select(func.count(DeviceInfo.id)).filter(*query_filter))
    pages = int(ceil(_count / float(page_size)))
    return response_ok(data=[jsonable_encoder(obj, exclude={'status'}) for obj in objs], total=_count, pages=pages)


@router_device_admin.get('/info/', summary='设备详情')
async def device_info(
        request: Request,
        id : int = Query(description='设备ID'),
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Security(get_current_active_user, scopes=['admin'])):
    """设备详情信息"""
    obj = await db.scalar(select(DeviceInfo).filter(DeviceInfo.id==id,
                            DeviceInfo.status==0))
    if obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    return response_ok(data=jsonable_encoder(obj, exclude={'status'}))


@router_device_admin.post('/delete/', summary='删除设备')
async def device_delete(
        request: Request,
        args : DeviceDelete,
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Security(get_current_active_user, scopes=['admin'])):
    """删除设备"""
    obj = await db.scalar(select(DeviceInfo.id).filter(DeviceInfo.id==args.id,
                            DeviceInfo.status==0))
    if obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await db.execute(update(DeviceInfo).where(DeviceInfo.id==args.id,
                            DeviceInfo.status==0, DeviceInfo.is_registered==0).values(status=-1))
    await db.commit()
    return response_ok()
