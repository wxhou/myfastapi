import traceback
from typing import Optional
from math import ceil
from datetime import timedelta
from jose import jwt, JWTError
from sqlalchemy import func, or_, select, insert, values, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from apps.deps import get_db
from core.settings import settings
from core.exceptions import UserNotExist, AccessTokenFail
from common.response import ErrCode, response_ok, response_err
from common.security import set_password, verify_password, create_access_token
from utils.logger import logger
from .model import BaseUser
from .schemas import Token, TokenData, UserRegister, UserModify, UserList

router_base_admin = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/base/admin/user/login/")


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(oauth2_scheme)):
    """获取当前登录用户"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AccessTokenFail
        token_data = TokenData(username=username)
    except JWTError:
        raise AccessTokenFail
    obj = await db.scalar(select(BaseUser).where(BaseUser.username == token_data.username))
    logger.info(obj)
    if obj is None:
        raise UserNotExist
    return obj


async def authenticate(db: AsyncSession, username: str, password: str):
    """ 验证用户 """
    sql = select(BaseUser).where(BaseUser.username ==
                                 username, BaseUser.status == 0)
    user = (await db.execute(sql)).scalar_one_or_none()
    if user and verify_password(password, user.password_hash):
        return user
    return False


@router_base_admin.post('/user/login/', response_model=Token, summary='登录')
async def login_access_token(
        request: Request,
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    """登录接口"""
    user = await authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        return response_err(ErrCode.UNAME_OR_PWD_ERROR)
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # 'access_token'和'token_type'一定要写,否则get_current_user依赖拿不到token
    # 可添加字段(先修改schemas/token里面的Token返回模型)
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})


@router_base_admin.post('/user/register/', summary='用户注册')
async def user_register(request: Request, user: UserRegister,
                        session: AsyncSession = Depends(get_db)):
    """用户注册"""
    async with session.begin():
        obj = await session.execute(select(BaseUser).where(or_(BaseUser.username == user.username,
                                         BaseUser.email == user.email)))
        if obj.one_or_none() is not None:
            return response_err(ErrCode.USER_HAS_EXISTS)
        obj = BaseUser(username=user.username,
                       email=user.email, nickname=user.nickname)
        session.add(obj)
        obj.password_hash = set_password(user.password)
        await session.commit()
    return response_ok(data=obj.id)


@router_base_admin.post('/user/update/', summary='更新用户信息')
async def user_update(
        request: Request,
        user: UserModify,
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Depends(get_current_user)):
    """更新用户信息"""
    print(current_user.username)
    sql = select(BaseUser).where(BaseUser.id == user.id, BaseUser.status == 0)
    obj = (await db.execute(sql)).scalar_one_or_none()
    if obj is None:
        return response_err(ErrCode.USER_NOT_EXISTS)
    obj.email = user.username
    obj.nick_name = user.nick_name
    obj.email = user.email
    db.commit()
    return response_ok(data={"uid": obj.id})


@router_base_admin.get('/user/list/', summary='用户列表')
async def user_list(
        request: Request,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=15, ge=1),
        username: str = Query(default=None),
        email: str = Query(default=None),
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Depends(get_current_user)):
    """更新用户信息"""
    query_filter = [BaseUser.status == 0]
    if username:
        query_filter.append(BaseUser.username.ilike(f'%{username}%'))
    if email:
        query_filter.append(BaseUser.email.ilike(f"%{email}%"))
    objs = (await db.scalars(select(BaseUser).filter(
        *query_filter).limit(page_size).offset((page - 1) * page))).all()
    _count = await db.scalar(select(func.count(BaseUser.id)))
    pages = int(ceil(_count / float(page_size)))
    return response_ok(data=[obj.to_dict() for obj in objs], total=_count, pages=pages)
