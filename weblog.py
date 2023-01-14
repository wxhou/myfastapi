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
    from app.core.exceptions import register_exceptions
    from app.core.middleware import register_middleware
    from app.core.socketio import sio, sio_asgi
    from app.extensions import register_extensions
    from app.api.router import register_router
    register_router(app)
    await register_extensions(app)
    register_exceptions(app)
    register_middleware(app)
    app.mount('/ws', sio_asgi, name='socket')
    app.state.sio = sio
  # redis


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # 关闭 redis


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8199)