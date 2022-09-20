from fastapi import FastAPI
from app.core.settings import settings
from app.core.schedule import scheduler

app = FastAPI(
    title=settings.PROJECT_NAME,
    description='%s-API' % settings.PROJECT_NAME,
    version='1.0.0',
    docs_url=settings.SWAGGER_DOCS_URL,
    redoc_url=settings.SWAGGER_REDOC_URL,
    swagger_ui_parameters=settings.SWAGGER_SCHEMAS
)


@app.on_event("startup")
async def startup():
    """初始化"""
    from app.core.redis import init_redis_pool
    from app.core.exceptions import register_exceptions
    from app.core.middleware import register_middleware
    from app.api.socketio import register_socketio
    from app.api.router import register_router
    scheduler.start()
    register_router(app)
    register_exceptions(app)
    register_middleware(app)
    register_socketio(app)
    app.state.redis = await init_redis_pool()  # redis


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
    await app.state.redis.close()  # 关闭 redis

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("weblog:app", host="127.0.0.1", port=settings.PORT, reload=settings.RELOAD, workers=1)
