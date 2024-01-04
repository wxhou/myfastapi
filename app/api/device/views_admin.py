from sqlalchemy import select, update
from fastapi import APIRouter, Query, Body, Security, Depends
from app.extensions import get_db, get_redis, AsyncSession, AsyncRedis
from app.common.pagation import PageNumberPagination
from app.common.response import ErrCode, response_ok, response_err
from app.utils.logger import logger
from app.api.base.auth import get_current_active_user
from app.api.user.model import BaseUser
from .model import DeviceInfo
from .schemas import DeviceInsert, DeviceUpdate


router_device_admin = APIRouter()



@router_device_admin.post('/insert/', summary='创建设备')
async def device_insert(
    args: DeviceInsert,
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user, scopes=['device_insert'])
):
    """新建设备"""
    obj = await db.scalar(select(DeviceInfo.id).filter(DeviceInfo.device_ip_addr==args.device_ip_addr,
                            DeviceInfo.device_mac_addr==args.device_mac_addr))
    if obj is not None:
        return response_err(ErrCode.DEVICE_IS_EXISTS)
    obj = DeviceInfo(**args.dict(exclude_none=True))
    db.add(obj)
    await db.flush()
    obj.generate_register_code(obj.device_type, obj.id)
    await db.commit()
    return response_ok(data={"id": obj.id})



@router_device_admin.put('/update/', summary='更新设备')
async def device_update(
    args: DeviceUpdate,
    db: AsyncSession = Depends(get_db),
    device_id: int = Query(description='设备ID', ge=1),
    current_user: BaseUser = Security(get_current_active_user, scopes=['device_modify'])
):
    """修改设备"""
    obj = await db.scalar(select(DeviceInfo).filter(DeviceInfo.id==device_id,
                            DeviceInfo.status==0,
                            DeviceInfo.is_registered==False))
    if obj is None:
        return response_err(ErrCode.DEVICE_NOT_FOUND)
    await db.execute(update(DeviceInfo).filter(DeviceInfo.id==device_id,
                            DeviceInfo.status==0,
                            DeviceInfo.is_registered==False).values(args.dict(exclude_none=True)))
    await db.commit()
    return response_ok(data=obj.to_dict())


@router_device_admin.get('/list/', summary='设备列表')
async def device_list(
    device_name: str = Query(default=None, description='设备名称'),
    paginate: PageNumberPagination = Depends(),
    current_user: BaseUser = Security(get_current_active_user, scopes=['device_list'])
):
    """设备列表信息"""
    query_filter = [DeviceInfo.status == 0]
    if device_name:
        query_filter.append(DeviceInfo.device_name.ilike(f'%{device_name}%'))
    result = await paginate(DeviceInfo, query_filter)
    return response_ok(**result)


@router_device_admin.get('/info/', summary='设备详情')
async def device_info(
    id : int = Query(description='设备ID'),
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user,scopes=['device_info'])
):
    """设备详情信息"""
    obj = await db.scalar(select(DeviceInfo).filter(DeviceInfo.id==id,
                            DeviceInfo.status==0))
    if obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    return response_ok(data=obj.to_dict())


@router_device_admin.delete('/delete/', summary='删除设备')
async def device_delete(
    device_id : int = Query(description='设备ID'),
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user, scopes=['device_delete'])
):
    """删除设备"""
    obj = await db.scalar(select(DeviceInfo.id).filter(DeviceInfo.id==device_id,
                            DeviceInfo.status==0))
    if obj is None:
        return response_err(ErrCode.QUERY_NOT_EXISTS)
    await db.execute(update(DeviceInfo).where(DeviceInfo.id==device_id,
                            DeviceInfo.status==0, DeviceInfo.is_registered==0).values(status=-1))
    await db.commit()
    return response_ok()
