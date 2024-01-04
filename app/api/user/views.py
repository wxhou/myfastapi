from datetime import timedelta
from sqlalchemy import or_, select, update
from fastapi import APIRouter, Depends, Request, Query, Path, Security
from app.extensions import get_db, get_redis, AsyncSession, AsyncRedis
from app.common.pagation import PageNumberPagination
from app.common.response import ErrCode, response_ok, response_err
from app.common.security import set_password, create_access_token
from app.utils.logger import logger
from app.api.base.auth import get_current_active_user
from .model import BaseUser, BaseUserCollect, BaseUserAddress
from .tasks import send_register_email_task
from .schemas import UserRegister, UserModify, UserAddressUpdate


router_admin = APIRouter()


@router_admin.post('/register/', summary='用户注册,并发送邮件')
async def user_register(
    request: Request,
    user: UserRegister,
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis)
):
    """用户注册"""
    obj = await db.execute(select(BaseUser).where(or_(BaseUser.username == user.username,
                                    BaseUser.email == user.email)))
    if obj.one_or_none() is not None:
        return response_err(ErrCode.USER_HAS_EXISTS)
    obj = BaseUser(username=user.username,
                    email=user.email, nickname=user.nickname)
    db.add(obj)
    obj.password_hash = set_password(user.password)
    await db.commit()
    expires_delta = 24*60*60
    access_token = create_access_token(
        data={"sub": obj.username}, expires_delta=timedelta(seconds=expires_delta)
    )
    await redis.set(f"user_register_{access_token}", value=obj.id, ex=expires_delta)
    send_register_email_task.delay(request.url_for("user_active", token=access_token), obj.email)
    return response_ok(data=obj.id)


@router_admin.get('/active/{token}', summary='用户激活')
async def user_active(
    token :str = Path(description="激活用户token"),
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedis = Depends(get_redis)
):
    """用户激活"""
    _uid = await redis.get(f"user_register_{token}")
    obj = await db.scalar(select(BaseUser).where(BaseUser.id==_uid, BaseUser.status==0))
    if obj is None:
        return response_err(ErrCode.USER_HAS_EXISTS)
    obj.is_active = True
    await db.commit()
    return response_ok()


@router_admin.put('/update/', summary='更新用户信息')
async def user_update(
    user: UserModify,
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user, scopes=['user_update'])
):
    """更新用户信息"""
    sql = select(BaseUser).where(BaseUser.id == current_user.id, BaseUser.status == 0)
    obj = await db.scalar(sql)
    if obj is None:
        return response_err(ErrCode.USER_NOT_EXISTS)
    await db.execute(update(BaseUser).where(BaseUser.id == current_user.id,
                                            BaseUser.status == 0).values(user.model_dump(exclude_none=True)))
    await db.commit()
    return response_ok(data=obj.id)


@router_admin.get('/list/', summary='用户列表')
async def user_list(
    username: str = Query(default=None),
    email: str = Query(default=None),
    paginate: PageNumberPagination = Depends(),
    current_user: BaseUser = Security(get_current_active_user, scopes=['user_list'])
):
    """更新用户信息"""
    query_filter = [BaseUser.status == 0]
    if username:
        query_filter.append(BaseUser.username.ilike(f'%{username}%'))
    if email:
        query_filter.append(BaseUser.email.ilike(f"%{email}%"))
    result = await paginate(BaseUser, query_filter)
    return response_ok(**result)


@router_admin.put('/address/update/', summary='更新用户地址')
async def user_address_update(
    addr: UserAddressUpdate,
    addr_id: int = Query(ge=1, description='用户ID'),
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user, scopes=['user_address_update'])
):
    """更新用户信息"""
    args = addr.model_dump(exclude_none=True)
    obj = await db.scalar(select(BaseUserAddress).where(BaseUserAddress.id==addr_id,
                                                    BaseUserAddress.user_id==current_user.id,
                                                    BaseUserAddress.status==0))
    if obj is None:
        obj = BaseUserAddress(**args)
        obj.user_id = current_user.id
        db.add(obj)
        await db.flush()
    else:
        sql = update(BaseUserAddress).where(BaseUserAddress.id==addr_id,
                                        BaseUserAddress.user_id==current_user.id,
                                        BaseUserAddress.status==0).values(**args)
        await db.execute(sql)
    await db.commit()
    return response_ok(data=obj.to_dict())


@router_admin.get('/address/list/', summary='用户地址列表')
async def user_address_list(
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Security(get_current_active_user, scopes=['user_address_list'])
):
    """用户地址列表"""
    objs = await db.scalars(select(BaseUserAddress).where(BaseUserAddress.user_id==current_user.id,
                                               BaseUserAddress.status==0))
    return response_ok(data=[obj.to_dict() for obj in objs])