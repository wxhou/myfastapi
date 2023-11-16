from typing import Optional
from sqlalchemy import select
from fastapi import Depends, Header
from app.extensions import get_db, get_redis, AsyncSession, AsyncRedis
from app.api.device.model import DeviceInfo
from app.common.error import DeviceNotFound



async def check_device_exists(
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis),
    device_id: Optional[str] =Header(default=None),
):
    """检查设备是否存在"""
    if device_id is None:
        raise DeviceNotFound
    obj = await db.execute(select(DeviceInfo).where(DeviceInfo.id==device_id, DeviceInfo.status==0,
                                                    DeviceInfo.is_registered==1))
    if obj is None:
        raise DeviceNotFound
    if not (await redis.sismember('jl_online_device', device_id)):
        await redis.sadd('jl_online_device', device_id)
    return device_id