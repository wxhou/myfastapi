import os
import logging
from typing import List, Optional, Dict, Set, Sequence
from pydantic import BaseSettings



class ProductionSettings(BaseSettings):
    """生产配置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))))
    DEBUG: bool = False
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 'Xs8nWV1P45jiKrjLV6OSnj'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[str] = ['http://localhost']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+asyncmy://root:root1234@127.0.0.1:3306/db_weblog?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@127.0.0.1:3306/db_weblog?charset=utf8"
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_ECHO: bool = False
    REDIS_URL: str = "redis://localhost:6379/2"

    CELERY_SECURITY_KEY: str = "vGf6eLwM2V5F5Qskoz8G3X"
    CELERY_BROKER_URL: str = "redis://localhost:6379/6"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/7"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "TExvm2$vmC!RECAyO9DDst"
    JWT_REFRESH_SECRET_KEY: str = "x&I^jl6n9D0aOgGn7USf7#"
    JWT_TOKEN_TYPE: str = 'Bearer'

    # email
    MAIL_SERVER: str = 'smtp.126.com'
    MAIL_PORT: int = 25
    MAIL_USERNAME: str = 'twxhou@126.com'
    MAIL_PASSWORD: str = 'GQWJDUKVWNOJLPOH'

    LOGGER_LEVEL: int = logging.INFO
    LOGGER_FILE: str = './logs/server.log'
    LOGGER_FORMATTER: str = '[%(asctime)s] %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'

    # upload
    UPLOAD_MEDIA_FOLDER: str = os.path.join(BASEDIR, 'upload')
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS: Set[str] = {'.png', '.jpg', '.jpeg'}
    ALLOWED_AUDIO_EXTENSIONS: Set[str] = {'.mp3'}
    ALLOWED_VIDEO_EXTENSIONS: Set[str] = {'.mp4'}

    PERMISSION_DATA: Dict[str, str] = {
        "admin": "管理员",
        "author": "作者",
        "user": "普通用户"
    }

    SERVERS: Optional[str] = None
    SWAGGER_LOGIN = "/login/"
    SWAGGER_DOCS_URL: Optional[str] = None
    SWAGGER_REDOC_URL: Optional[str] = None
    OPENAPI_URL: str = "/openapi.json"
    SWAGGER_DESCRIPTION: str = f'{PROJECT_NAME}-生产环境API'
    # https://github.com/tiangolo/fastapi/issues/2633
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1}
    SWAGGER_UI_PARAMETERS: str = '/docs/oauth2-redirect'

