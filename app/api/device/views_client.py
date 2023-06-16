from sqlalchemy import select, update
from fastapi import APIRouter, Depends, Security, Request, Query, Header
from app.extensions import async_db, async_redis
from app.settings import settings
from app.common.response import ErrCode, response_ok, response_err
from app.utils.logger import logger
from .auth import check_device_exists
from .model import DeviceInfo
from .schemas import DeviceRegister


router_device_client = APIRouter()



@router_device_client.post('/register/', summary='设备注册')
async def device_register(request: Request,
        args: DeviceRegister,
        db: async_db):
    """新建设备"""
    obj = await db.scalar(select(DeviceInfo.id).filter(DeviceInfo.device_register_code==args.device_register_code,
                            DeviceInfo.is_registered==0, DeviceInfo.status==0))
    if obj is not None:
        return response_err(ErrCode.DEVICE_IS_EXISTS)
    await db.execute(update(DeviceInfo).where(DeviceInfo.device_register_code==args.device_register_code,
                            DeviceInfo.is_registered==0, DeviceInfo.status==0).values(is_registered=1))
    await db.commit()
    return response_ok(data=obj.to_dict())


@router_device_client.get('/info/', summary='设备详情')
async def device_detail(
        request: Request,
        db: async_db,
        id : int = Query(description='设备ID')):
    """设备详情信息"""
    obj = await db.scalar(select(DeviceInfo).filter(DeviceInfo.id==id,
                            DeviceInfo.status==0))
    if obj is None:
        return response_err(ErrCode.DEVICE_NOT_FOUND)
    return response_ok(data=obj.to_dict())

