import os, uuid
from typing import Optional
from math import ceil
from datetime import timedelta
import shutil
from jose import jwt, JWTError
from sqlalchemy import func, or_, select, insert, values, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, Query, Path, BackgroundTasks, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from apps.deps import get_db, get_redis
from core.redis import CustomRedis
from core.settings import settings
from common.errors import UserNotExist, UserNotActive, AccessTokenFail
from common.response import ErrCode, response_ok, response_err
from common.security import set_password, verify_password, create_access_token
from utils.logger import logger
from .model import BaseUser, UploadModel
from .task import send_register_email
from .schemas import Token, TokenData, UserRegister, UserModify, UserList

router_base_admin = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/base/admin/user/login/")


async def get_current_user(db: AsyncSession = Depends(get_db),
                           redis: CustomRedis = Depends(get_redis),
                           token: str = Depends(oauth2_scheme)):
    """获取当前登录用户"""
    try:
        is_token = await redis.get("weblog_{}".format(token))
        if is_token is None:
            raise AccessTokenFail
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AccessTokenFail
        token_data = TokenData(username=username)
    except JWTError:
        raise AccessTokenFail
    obj = await db.scalar(select(BaseUser).where(BaseUser.username == token_data.username))
    if obj is None:
        raise UserNotExist
    return obj


async def get_current_active_user(current_user: BaseUser = Depends(get_current_user)):
    """
    获取激活用户
    """
    if not current_user.is_active:
        raise UserNotActive
    return current_user


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
        redis: CustomRedis = Depends(get_redis),
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
    await redis.set("weblog_{}".format(access_token), 1, ex=access_token_expires)
    # 'access_token'和'token_type'一定要写,否则get_current_user依赖拿不到token
    # 可添加字段(先修改schemas/token里面的Token返回模型)
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})

@router_base_admin.post('/logout/', summary='退出登录')
async def logout(request: Request,
                 redis: CustomRedis = Depends(get_redis),
                 current_user: BaseUser = Depends(get_current_active_user)):
    """退出登录"""
    if token := request.headers.get('authorization'):
        token = token.split(' ', 1)[1]  # 去除token前面的 Bearer
        await redis.delete("weblog_{}".format(token))
    return response_ok()


@router_base_admin.post('/user/register/', summary='用户注册,并发送邮件')
async def user_register(request: Request,
                        user: UserRegister,
                        background_tasks: BackgroundTasks,
                        session: AsyncSession = Depends(get_db),
                        redis: CustomRedis = Depends(get_redis)):
    """用户注册"""
    obj = await session.execute(select(BaseUser).where(or_(BaseUser.username == user.username,
                                        BaseUser.email == user.email)))
    if obj.one_or_none() is not None:
        return response_err(ErrCode.USER_HAS_EXISTS)
    obj = BaseUser(username=user.username,
                    email=user.email, nickname=user.nickname)
    session.add(obj)
    obj.password_hash = set_password(user.password)
    await session.commit()
    expires_delta = 24*60*60
    access_token = create_access_token(
        data={"sub": obj.username}, expires_delta=timedelta(seconds=expires_delta)
    )
    await redis.set(f"user_register_{access_token}", value=obj.id, ex=expires_delta)
    background_tasks.add_task(send_register_email, request.url_for("user_active", token=access_token), obj.email)
    return response_ok(data=obj.id)


@router_base_admin.get('/user/active/{token}', summary='用户激活')
async def user_active(request: Request,
                    token :str = Path(title="激活用户token"),
                    session: AsyncSession = Depends(get_db),
                    redis: CustomRedis = Depends(get_redis)):
    """用户激活"""
    _uid = await redis.get(f"user_register_{token}")
    logger.info(_uid)
    obj = await session.scalar(select(BaseUser).where(BaseUser.id==_uid))
    if obj is None:
        return response_err(ErrCode.USER_HAS_EXISTS)
    obj.is_active = True
    await session.commit()
    return response_ok()


@router_base_admin.post('/user/update/', summary='更新用户信息')
async def user_update(
        request: Request,
        user: UserModify,
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Depends(get_current_active_user)):
    """更新用户信息"""
    sql = select(BaseUser).where(BaseUser.id == user.id, BaseUser.status == 0)
    obj = (await db.execute(sql)).scalar_one_or_none()
    if obj is None:
        return response_err(ErrCode.USER_NOT_EXISTS)
    obj.email = user.username
    obj.nick_name = user.nick_name
    obj.email = user.email
    obj.avatar_id = user.avatar_id
    await db.commit()
    return response_ok(data={"uid": obj.id})


@router_base_admin.get('/user/list/', summary='用户列表')
async def user_list(
        request: Request,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=15, ge=1),
        username: str = Query(default=None),
        email: str = Query(default=None),
        db: AsyncSession = Depends(get_db),
        current_user: BaseUser = Depends(get_current_active_user)):
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


@router_base_admin.post("/upload/", summary='上传文件')
async def create_upload_file(file: UploadFile = File(),
                             db:AsyncSession = Depends(get_db),
                             current_user: BaseUser = Depends(get_current_active_user)):
    """上传文件"""
    ext = os.path.splitext(file.filename)[1]
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        return response_err(ErrCode.FILE_TYPE_ERROR)
    filename = uuid.uuid4().hex
    save_file = os.path.join(settings.UPLOAD_MEDIA_FOLDER, filename + ext)
    with open(save_file, 'wb+') as buffer:
        buffer.write(await file.read())
        file.read()
    obj = UploadModel(url='/upload/{}{}'.format(filename, ext))
    db.add(obj)
    await db.commit()
    return response_ok(data=obj.to_dict())