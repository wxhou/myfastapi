import os
import logging
from typing import List, Optional, Dict, Set, Sequence
from functools import lru_cache
from pydantic import BaseSettings, AnyHttpUrl


class DevelopmentSettings(BaseSettings):
    """"开发设置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DEBUG: bool = True
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 's2JNHjKeZCj5b2brh4so34'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: Sequence[str] = ['*']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+asyncmy://root:root1234@localhost:3306/db_weblog?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_ECHO: bool = True
    REDIS_URL: str = "redis://localhost:6379/2"

    MONGO_URL: str = 'mongodb://admin:123456@127.0.0.1:27017'

    CELERY_SECURITY_KEY: str = "'R9NrIpN5zbMpbcuzNL75BU'"
    CELERY_BROKER_URL: str = "redis://localhost:6379/6"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/7"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "DXaPkfReer04uwIQU06Enl"
    JWT_REFRESH_SECRET_KEY: str = "o7Ooj6lswdtXUtfuSnjvQS"

    # MINIO
    MINIO_HOST = "192.168.0.174:9000"
    MINIO_ACCESS_KEY = "admin"
    MINIO_SECRET_KEY = "admin123"

    # alipay
    ALIPAY_SERVER_URL = "https://openapi.alipay.com/gateway.do"
    ALIPAY_APP_ID = os.path.join(BASEDIR, 'cert', 'ALIPAY_APP_ID.txt')
    ALIPAY_APP_PRIVATE_KEY = os.path.join(BASEDIR, 'cert', 'ALIPAY_APP_PRIVATE_KEY.txt')
    ALIPAY_PUBLIC_KEY = os.path.join(BASEDIR, 'cert', 'ALIPAY_PUBLIC_KEY.txt')

    # email
    MAIL_SERVER: str = 'smtp.126.com'
    MAIL_PORT: int = 25
    MAIL_USERNAME: str = 'twxhou@126.com'
    MAIL_PASSWORD: str = 'GQWJDUKVWNOJLPOH'

    LOGGER_LEVEL: int = logging.DEBUG
    LOGGER_SERVER_FILE: str = './logs/server.log'
    LOGGER_ERROR_FILE: str = './logs/error.log'
    WEBSOCKET_LOGGER_FILE: str = './logs/websocket.log'
    PAY_LOGGER_FILE: str = './logs/weblog_pay.log'

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
    SWAGGER_REDOC_URL: str = '/redocs'
    # https://github.com/tiangolo/fastapi/issues/2633
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1}


class TestingSettings(BaseSettings):
    """测试配置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))))
    DEBUG: bool = True
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 'FPX5zXhNVCbLPmSPnJLgmG'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+asyncmy://root:root1234@localhost:3306/db_weblog?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_ECHO: bool = True
    REDIS_URL: str = "redis://localhost:6379/2"

    CELERY_SECURITY_KEY: str = "k75rBIhvnZpOtYiH4rJfWv"
    CELERY_BROKER_URL: str = "redis://localhost:6379/6"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/7"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # MINIO
    MINIO_HOST = "10.12.52.212:9000"
    MINIO_ACCESS_KEY = "admin"
    MINIO_SECRET_KEY = "admin123"

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
    SWAGGER_REDOC_URL: str = '/redocs'
    # https://github.com/tiangolo/fastapi/issues/2633
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1}


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
    CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

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
    # https://github.com/tiangolo/fastapi/issues/2633
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1}


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
