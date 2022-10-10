import os, shutil
from uuid import uuid4
from datetime import timedelta
from tempfile import NamedTemporaryFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.common.encoder import jsonable_encoder
from app.api.deps import get_db, get_redis
from app.core.redis import MyRedis
from app.core.settings import settings
from app.common.response import ErrCode, response_ok, response_err
from app.common.security import create_access_token, create_refresh_token, decrypt_refresh_token
from app.utils.logger import logger
from .model import BaseUser, UploadModel, BasePermission
from .auth import oauth2_scheme, authenticate, get_current_active_user
from .schemas import Token, RefreshToken


router_login = APIRouter(tags=['Auth'])



@router_login.post('/login/', response_model=Token, summary='登录')
async def login_access_token(
        request: Request,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    """登录接口"""
    user = await authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        return response_err(ErrCode.UNAME_OR_PWD_ERROR)
    access_token = create_access_token(data={"sub": user.username, "id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.username, "id": user.id})
    await redis.set("weblog_access_token_{}".format(access_token), refresh_token,
                    ex=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    await redis.set("weblog_refresh_token_{}".format(refresh_token), access_token,
                    ex=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    # 'access_token'和'token_type'一定要写,否则get_current_user依赖拿不到token
    # 可添加字段(先修改schemas/token里面的Token返回模型)
    return JSONResponse({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "JWT"
    })


@router_login.post('/login/refresh/', summary='刷新Token')
async def login_refresh_token(
        request: Request,
        data: RefreshToken,
        db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis)
):
    """登录接口"""

    username, uid = await decrypt_refresh_token(data.refresh_token)
    _key_name = 'weblog_login_temporary'
    res = await redis.get_pickle(_key_name)
    if res:
        return JSONResponse(res)
    user_obj = await db.scalar(select(BaseUser).where(BaseUser.username==username, BaseUser.status==0))
    if user_obj is None:
        return response_err(ErrCode.TOKEN_INVALID_ERROR)
    if not (await redis.exists(f"weblog_refresh_token_{data.refresh_token}")):
        return response_err(ErrCode.TOKEN_INVALID_ERROR)
    access_token = create_access_token(data={"sub": username, "id": uid})
    await redis.set("weblog_access_token_{}".format(access_token), data.refresh_token,
                    ex=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    result = {"access_token": access_token, "token_type": "JWT"}
    await redis.set_pickle(_key_name, result, timeout=10)
    return JSONResponse(result)


@router_login.api_route('/logout/', methods=['GET', 'POST'], summary='退出登录')
async def logout(request: Request,
                 redis: MyRedis = Depends(get_redis),
                 token: str = Depends(oauth2_scheme)):
    """退出登录"""
    refresh_token = await redis.get("weblog_access_token_{}".format(token))
    await redis.delete("weblog_access_token_{}".format(token))
    if refresh_token:
        await redis.delete("weblog_refresh_token_{}".format(refresh_token))
    return response_ok()



@router_login.post("/upload/", summary='上传文件')
async def create_upload_file(file: UploadFile = File(),
                             db:AsyncSession = Depends(get_db),
                             current_user: BaseUser = Depends(get_current_active_user)):
    """上传文件"""
    ext = os.path.splitext(file.filename)[1]
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        return response_err(ErrCode.FILE_TYPE_ERROR)
    new_fname = "{}/{}{}".format(file.content_type, uuid4(), ext).replace('/', '-')
    save_file = os.path.join(settings.UPLOAD_MEDIA_FOLDER, new_fname)
    with open(save_file, 'wb+') as buffer:
        buffer.write(await file.read())
    obj = UploadModel(fileUrl='/upload/' + new_fname,
                      filename=file.filename,
                      content_type=file.content_type,
                      uid=current_user.id)
    db.add(obj)
    await db.commit()
    return response_ok(data=jsonable_encoder(obj, exclude={'status'}))


@router_login.get("/api/routes", summary="所有路由", deprecated=True)
async def api_routes(request: Request,
                     db:AsyncSession = Depends(get_db)):
    result = []
    number = 1
    for route in request.app.routes:
        items = {
            "name": route.name,
            "path": route.path
        }
        result.append(items)
        obj = BasePermission(name=route.path, function_name=route.name, order_num=number)
        number += 1
        db.add(obj)
    await db.commit()
    return response_ok(data=result)