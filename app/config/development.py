import os
import logging
from typing import List, Optional, Dict, Set
from pydantic import BaseSettings


class DevelopmentSettings(BaseSettings):
    """"开发设置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DEBUG: bool = True
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 's2JNHjKeZCj5b2brh4so34'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[str] = ['*']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+asyncmy://root:root1234@localhost:3306/db_weblog?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_ECHO: bool = True

    # Redis
    REDIS_URL: str = "redis://localhost:6379/2"
    REDIS_SOCKETIO_URL: str = "redis://localhost:6379/3"
    REDIS_CONNECTIONS = [
        {
            'host': 'localhost',
            'port': 6379,
            'db': db_number,
        } for db_number in range(1, 17)
    ]

    # MongoDB
    MONGO_URL: str = 'mongodb://admin:123456@127.0.0.1:27017'

    # celery
    CELERY_SECURITY_KEY: str = "'R9NrIpN5zbMpbcuzNL75BU'"
    CELERY_BROKER_URL: str = "redis://localhost:6379/6"
    CELERY_RESULT_BACKEND: str = "db+mysql+pymysql://root:root1234@localhost:3306/db_weblog?charset=utf8"
    # CELERY_RESULT_BACKEND: str = "redis://localhost:6379/7"

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "DXaPkfReer04uwIQU06Enl"
    JWT_REFRESH_SECRET_KEY: str = "o7Ooj6lswdtXUtfuSnjvQS"
    JWT_TOKEN_TYPE: str = 'Bearer'

    # MINIO
    MINIO_HOST: str = "192.168.0.174:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "admin123"

    # alipay
    ALIPAY_SERVER_URL: str = "https://openapi.alipaydev.com/gateway.do"
    ALIPAY_APP_ID: str = ''
    ALIPAY_APP_PRIVATE_KEY: str = ''
    ALIPAY_PUBLIC_KEY: str = ''

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


    # swagger
    SERVERS: Optional[List] = None
    SWAGGER_LOGIN = "/login/"
    SWAGGER_DOCS_URL: str = '/docs'
    SWAGGER_REDOC_URL: str = '/redocs'
    OPENAPI_URL: str = "/openapi.json"
    SWAGGER_DESCRIPTION: str = f'{PROJECT_NAME}-开发环境API'
    # https://github.com/tiangolo/fastapi/issues/2633
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1}
    SWAGGER_UI_PARAMETERS: str = '/docs/oauth2-redirect'
