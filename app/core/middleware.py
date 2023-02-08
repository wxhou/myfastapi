import traceback
from datetime import timedelta
from jose import jwt, JWTError
from sqlalchemy import select
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware, AuthenticationBackend
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
    # app.add_middleware(CSRFMiddleware, secret=settings.SECRET_KEY) # 使用此插件无法使用websocket
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
    app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())
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


# Authentication Backend Class
class BearerTokenAuthBackend(AuthenticationBackend):
    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """
    async def authenticate(self, request):
        # This function is inherited from the base class and called by some other class
        if "Authorization" not in request.headers:
            return
        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            is_token_alive = await request.app.state.redis.exists("weblog_access_token_{}".format(token))
            if not is_token_alive:
                raise TokenExpiredError
            username, uid = await decrypt_access_token(token)
        except (ValueError, UnicodeDecodeError, JWTError) as exc:
            raise JWTError
        token_data = TokenData(username=username)
        async with async_session() as db:
            obj = await db.scalar(select(BaseUser).where(BaseUser.id==uid,
                                                    BaseUser.username == token_data.username,
                                                    BaseUser.status == 0))
            if obj is None:
                raise UserNotExist
        return auth, obj