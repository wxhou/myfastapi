from math import ceil
from datetime import timedelta
from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Security, Request, Query, Path, BackgroundTasks, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.api.deps import get_db, get_redis
from app.core.redis import MyRedis
from app.core.settings import settings
from app.common.response import ErrCode, response_ok, response_err
from app.utils.logger import logger
from app.api.base.auth import get_current_active_user
from app.api.base.model import BaseUser, UploadModel
from .model import DeviceInfo
from .schemas import DeviceRegister


router_device_admin = APIRouter()



@router_device_admin.post('/register/', summary='设备注册')
async def device_register(request: Request,
        args: DeviceRegister,
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Security(get_current_active_user, scopes=['admin'])):
    """新建设备"""
    obj = await db.scalar(select(DeviceInfo.id).filter(DeviceInfo.device_ip_addr==args.device_ip_addr,
                            DeviceInfo.device_mac_addr==args.device_mac_addr))
    if obj is not None:
        return response_err(ErrCode.QUERY_HAS_EXISTS)
    obj = DeviceInfo(
        device_name=args.device_name,
        device_type=args.device_type,
        device_position=args.device_position,
        device_number=args.device_number,
        device_screen_number=args.device_screen_number,
        device_mac_addr=args.device_mac_addr,
        device_ip_addr=args.device_ip_addr,
        annotation=args.annotation
    )
    db.add(obj)
    await db.commit()
    return response_ok(data={"id": obj.id})

