from fastapi import FastAPI
from app.core.settings import settings
from app.core.sio import sio, sio_app
from app.extensions.schedule import scheduler

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
    import motor.motor_asyncio
    from app.core.exceptions import register_exceptions
    from app.core.middleware import register_middleware
    from app.extensions.redis import init_redis_pool
    from app.api.router import register_router
    register_router(app)
    register_exceptions(app)
    register_middleware(app)
    app.state.mongo = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
    app.state.redis = await init_redis_pool()  # redis
    app.state.sio = sio
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
    await app.state.redis.close()  # 关闭 redis
