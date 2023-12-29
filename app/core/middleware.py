import traceback
from typing import Callable
from datetime import timedelta
from jose import jwt, JWTError
from sqlalchemy import select
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeRenderer

from app.settings import settings


# 权限验证 https://www.cnblogs.com/mazhiyong/p/13433214.html
# 得到真实ip https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
# nginx 解决跨域请求 https://segmentfault.com/a/1190000019227927


def register_middleware(app: FastAPI):
    """ 请求拦截与响应拦截 -- https://fastapi.tiangolo.com/tutorial/middleware/ """
    # app.add_middleware(CSRFMiddleware, secret=settings.SECRET_KEY) # 使用此插件无法使用websocket
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
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


    if settings.PROFILING_ENABLED is True:
        """性能分析"""
        @app.middleware("http")
        async def profile_request(request: Request, call_next: Callable):
            """Profile the current request

            Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
            with small improvements.

            """

            # if the `profile=true` HTTP query argument is passed, we profile the request
            if request.query_params.get("profile", False):
                # we map a profile type to a file extension, as well as a pyinstrument profile renderer
                profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
                profile_type_to_renderer = {
                    "html": HTMLRenderer,
                    "speedscope": SpeedscopeRenderer,
                }

                # The default profile format is speedscope
                profile_type = request.query_params.get("profile_format", "html")

                # we profile the request along with all additional middlewares, by interrupting
                # the program every 1ms1 and records the entire stack at that point
                with Profiler(interval=0.001, async_mode="enabled") as profiler:
                    response = await call_next(request)

                # we dump the profiling into a file
                extension = profile_type_to_ext[profile_type]
                renderer = profile_type_to_renderer[profile_type]()
                with open(f"profile.{extension}", "w") as out:
                    out.write(profiler.output(renderer=renderer))
                return response

            # Proceed without profiling
            return await call_next(request)