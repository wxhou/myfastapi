import logging
from fastapi import FastAPI
from core.settings import settings

app = FastAPI(
    title='Weblog API',
    description='Weblog API',
    version='1.0.0',
)


@app.on_event("startup")
async def startup():
    """初始化"""
    from core.redis import init_redis_pool
    from core.exceptions import register_exceptions
    from core.middleware import register_middleware
    from apps.router import register_router

    register_router(app)
    register_exceptions(app)
    register_middleware(app)
    app.state.redis = await init_redis_pool()  # redis


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # 关闭 redis

if __name__ == '__main__':
    import uvicorn
    print(settings.PORT)
    uvicorn.run("weblog:app", host="127.0.0.1", port=settings.PORT,
                reload=settings.RELOAD, workers=1)
