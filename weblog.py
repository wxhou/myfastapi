from fastapi import FastAPI
from app.core.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version='1.0.0',
    description=settings.SWAGGER_DESCRIPTION,
    servers=settings.SERVERS,
    docs_url=settings.SWAGGER_DOCS_URL,
    redoc_url=settings.SWAGGER_REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    swagger_ui_oauth2_redirect_url=settings.SWAGGER_UI_PARAMETERS,
    swagger_ui_parameters=settings.SWAGGER_SCHEMAS
)


@app.on_event("startup")
async def startup():
    """初始化"""
    import motor.motor_asyncio
    from app.core.exceptions import register_exceptions
    from app.core.middleware import register_middleware
    from app.extensions.redis import init_redis_pool
    from app.extensions.socketio import register_socketio
    from app.api.router import register_router
    register_router(app)
    register_exceptions(app)
    register_middleware(app)
    register_socketio(app)
    app.state.mongo = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
    app.state.redis = await init_redis_pool()  # redis


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # 关闭 redis


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8199)