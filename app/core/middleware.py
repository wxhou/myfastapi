import traceback
from datetime import timedelta
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.exc import OperationalError
from aioredis.exceptions import ConnectionError
from app.core.settings import settings
from app.core.redis import MyRedis
from app.utils.logger import logger
from app.common.response import ErrCode, response_err

# 权限验证 https://www.cnblogs.com/mazhiyong/p/13433214.html
# 得到真实ip https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
# nginx 解决跨域请求 https://segmentfault.com/a/1190000019227927


def register_middleware(app: FastAPI):
    """ 请求拦截与响应拦截 -- https://fastapi.tiangolo.com/tutorial/middleware/ """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=("GET", "POST", "PUT", "DELETE"),
        allow_headers=("*", "Authorization"),
    )
    # 500字节以上才开启gzip
    app.add_middleware(
        GZipMiddleware,
        minimum_size=500
    )

    @app.middleware("http")
    async def many_request(request: Request, call_next):
        try:
            redis: MyRedis = await request.app.state.redis
            _key_name = request.client.host + str(request.url)
            amount = await redis.get(_key_name)
            if amount and int(amount) > 60:
                return response_err(ErrCode.TOO_MANY_REQUEST)
            await redis.incr(_key_name)
            await redis.expire(_key_name, timedelta(minutes=1))
            return await call_next(request)  # 返回请求(跳过token)
        except ConnectionError:
            logger.critical(traceback.format_exc())
            return response_err(ErrCode.REDIS_CONNECTION_ERROR)
        except OperationalError:
            logger.critical(traceback.format_exc())
            return response_err(ErrCode.DB_CONNECTION_ERROR)
