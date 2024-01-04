from contextlib import asynccontextmanager
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from app.settings import settings
from app.utils.logger import logger


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.org/swagger-ui/5.9.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.org/swagger-ui/5.9.0/swagger-ui.min.css")

applications.get_swagger_ui_html = swagger_monkey_patch



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load
    logger.info("Load Start Event!")
    from app.extensions import register_extensions
    from app.api.router import register_router
    register_extensions(app)
    register_router(app)
    yield
    # Clean
    logger.info("Clean End Event!")


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
from app.core.exceptions import register_exceptions

register_middleware(app)
register_exceptions(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("weblog:app", host='0.0.0.0', port=settings.PORT,
                reload=settings.RELOAD,
                reload_excludes=['env', 'venv', 'alembic', 'vscode'])