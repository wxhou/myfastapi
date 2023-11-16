from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.settings import settings




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load
    from app.core.exceptions import register_exceptions
    from app.extensions import register_extensions
    from app.api.router import register_router
    register_exceptions(app)
    await register_extensions(app)
    register_router(app)
    yield
    # Clean
    await app.state.redis.close()  # 关闭 redis


app = FastAPI(
    title=settings.PROJECT_NAME,
    version='1.0.0',
    lifespan=lifespan,
    description=settings.SWAGGER_DESCRIPTION,
    servers=settings.SERVERS,
    docs_url=settings.SWAGGER_DOCS_URL,
    redoc_url=settings.SWAGGER_REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    swagger_ui_oauth2_redirect_url=settings.SWAGGER_UI_PARAMETERS,
    swagger_ui_parameters=settings.SWAGGER_SCHEMAS
)

from app.core.middleware import register_middleware

register_middleware(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8199)