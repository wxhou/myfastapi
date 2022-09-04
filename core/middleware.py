import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from aioredis.exceptions import ConnectionError
from core.settings import settings
from utils.logger import logger
from common.response import ErrCode, response_err

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

    @app.middleware("http")
    async def intercept(request: Request, call_next):
        logger.info(
            f"访问记录:IP:{request.client.host}-method:{request.method}-url:{request.url}")
        try:
            # redis 请求数量 (自增 1)
            await request.app.state.redis.incr('request_num')
            return await call_next(request)  # 返回请求(跳过token)
        except ConnectionError as e:
            logger.critical(traceback.format_exc())
            return response_err(ErrCode.REDIS_CONNECTION_ERROR)
        except OperationalError as e:
            logger.critical(traceback.format_exc())
            return response_err(ErrCode.DB_CONNECTION_ERROR)
