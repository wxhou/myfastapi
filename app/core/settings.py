import os
import logging
from typing import List, Optional, Dict, Set
from functools import lru_cache
from pydantic import BaseSettings, AnyHttpUrl


class DevelopmentSettings(BaseSettings):
    """"开发设置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG: bool = True
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 'b7c890f9-983d-4950-9d99-228356a17203'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+aiomysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    SQLALCHEMY_ECHO: bool = True
    REDIS_URL: str = "redis://localhost:6379/2"

    CELERY_BROKER_URL: str = "redis://localhost:6379/6"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/7"
    CELERY_TIMEZONE:str = ""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # email
    MAIL_SERVER: str = 'smtp.126.com'
    MAIL_PORT: int = 25
    MAIL_USERNAME: str = 'twxhou@126.com'
    MAIL_PASSWORD: str = 'GQWJDUKVWNOJLPOH'

    LOGGER_LEVEL: int = logging.DEBUG
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

    SWAGGER_DOCS_URL: str = '/docs'
    SWAGGER_REDOC_URL: str ='/redocs'
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1} # https://github.com/tiangolo/fastapi/issues/2633

class TestingSettings(BaseSettings):
    """测试配置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG: bool = True
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 'b1fbb16c-de57-48a7-8ec1-0149d10fbd58'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+aiomysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    SQLALCHEMY_ECHO: bool = True
    REDIS_URL: str = "redis://localhost:6379/2"

    CELERY_BROKER_URL: str = "redis://localhost:6379/6"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/7"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # email
    MAIL_SERVER: str = 'smtp.126.com'
    MAIL_PORT: int = 25
    MAIL_USERNAME: str = 'twxhou@126.com'
    MAIL_PASSWORD: str = 'GQWJDUKVWNOJLPOH'

    LOGGER_LEVEL: int = logging.DEBUG
    LOGGER_FILE: str = './logs/server.log'
    LOGGER_FORMATTER: str = '[%(asctime)s] %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'

    # upload
    UPLOAD_MEDIA_FOLDER: str = os.path.join(BASEDIR, 'upload')
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS: Set[str] = {'.png', '.jpg', '.jpeg'}
    ALLOWED_AUDIO_EXTENSIONS: Set[str]  = {'.mp3'}
    ALLOWED_VIDEO_EXTENSIONS: Set[str] = {'.mp4'}

    PERMISSION_DATA: Dict[str, str] = {
        "admin": "管理员",
        "author": "作者",
        "user": "普通用户"
    }

    SWAGGER_DOCS_URL: str = '/docs'
    SWAGGER_REDOC_URL: str ='/redocs'
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1} # https://github.com/tiangolo/fastapi/issues/2633



class ProductionSettings(BaseSettings):
    """生产配置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG: bool = False
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 'c3ef509e-1ab9-4e94-b6af-68c4c12e4f25'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+aiomysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    SQLALCHEMY_ECHO: bool = True
    REDIS_URL: str = "redis://localhost:6379/2"

    CELERY_BROKER_URL: str = "redis://localhost:6379/6"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/7"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

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

    SWAGGER_DOCS_URL: Optional[str] = None
    SWAGGER_REDOC_URL: Optional[str] = None
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1} # https://github.com/tiangolo/fastapi/issues/2633


@lru_cache()
def get_settings():
    """获取配置信息"""
    env = os.environ.get('MY_WEBLOG_ENV', None)
    if env is None:
        raise EnvironmentError("MY_WEBLOG_ENV is Undefined!")
    env_config = {
        "development": DevelopmentSettings(),
        "testing": TestingSettings(),
        "production": ProductionSettings()
    }
    return env_config[env]


settings = get_settings()

if __name__ == '__main__':
    print(settings.PORT)
