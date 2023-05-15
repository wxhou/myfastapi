import traceback
from datetime import timedelta
from jose import jwt, JWTError
from sqlalchemy import select
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_csrf import CSRFMiddleware
from starlette.authentication import AuthCredentials, AuthenticationBackend, SimpleUser
from starlette.middleware.authentication import AuthenticationMiddleware
from app.core.settings import settings
from app.extensions.db import async_session
from app.utils.logger import logger
from app.common.error import UserNotExist, TokenExpiredError
from app.common.response import ErrCode, response_err
from app.common.security import decrypt_access_token
from app.api.base.schemas import TokenData
from app.api.user.model import BaseUser

# 权限验证 https://www.cnblogs.com/mazhiyong/p/13433214.html
# 得到真实ip https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
# nginx 解决跨域请求 https://segmentfault.com/a/1190000019227927


def register_middleware(app: FastAPI):
    """ 请求拦截与响应拦截 -- https://fastapi.tiangolo.com/tutorial/middleware/ """
    app.add_middleware(CSRFMiddleware, secret=settings.SECRET_KEY) # 使用此插件无法使用websocket
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    # 500字节以上才开启gzip
    app.add_middleware(
        GZipMiddleware,
        minimum_size=500
    )

    # @app.middleware("http")
    # async def many_request(request: Request, call_next):
    #     redis = await request.app.state.redis
    #     _key_name = request.client.host + str(request.url)
    #     amount = await redis.get(_key_name)
    #     if amount and int(amount) > 60 :
    #         return response_err(ErrCode.TOO_MANY_REQUEST)
    #     await redis.incr(_key_name)
    #     await redis.expire(_key_name, timedelta(minutes=1))
    #     return await call_next(request)  # 返回请求(跳过token)