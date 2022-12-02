import os
import logging
from typing import List, Dict, Set, Sequence
from pydantic import BaseSettings



class TestingSettings(BaseSettings):
    """"测试设置"""
    PROJECT_NAME = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DEBUG: bool = True
    PORT: int = 8199
    RELOAD: bool = True
    SECRET_KEY: str = 'WeH0a!lIsBx7xYxUpaM5Wb'
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: Sequence[str] = ['*']

    # ASYNC_SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./sql_app.db?check_same_thread=False'
    # MySQL(异步)
    ASYNC_SQLALCHEMY_DATABASE_URL: str = "mysql+asyncmy://root:root1234@localhost:3306/db_weblog"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:root1234@localhost:3306/db_weblog"
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_ECHO: bool = True
    REDIS_URL: str = "redis://localhost:26379/12"
    REDIS_CONNECTIONS = [
        {
            'host': 'localhost',
            'port': 26379,
            'db': 11,
        },
        {
            'host': 'localhost',
            'port': 26379,
            'db': 12,
        }
    ]

    MONGO_URL: str = 'mongodb://admin:123456@127.0.0.1:27017'

    CELERY_SECURITY_KEY: str = "'XBDGwqmFoTE4m2F$y3ZX#6'"
    CELERY_BROKER_URL: str = "redis://localhost:26379/12"
    CELERY_RESULT_BACKEND: str = "redis://localhost:26379/11"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "DXaPkfReer04uwIQU06Enl"
    JWT_REFRESH_SECRET_KEY: str = "o7Ooj6lswdtXUtfuSnjvQS"

    # MINIO
    MINIO_HOST: str = "192.168.0.174:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "admin123"

    # alipay
    ALIPAY_SERVER_URL: str = "https://openapi.alipay.com/gateway.do"
    ALIPAY_APP_ID: str = os.path.join(BASEDIR, 'cert', 'ALIPAY_APP_ID.txt')
    ALIPAY_APP_PRIVATE_KEY: str = os.path.join(BASEDIR, 'cert', 'ALIPAY_APP_PRIVATE_KEY.txt')
    ALIPAY_PUBLIC_KEY: str = os.path.join(BASEDIR, 'cert', 'ALIPAY_PUBLIC_KEY.txt')

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

    SERVERS: List[Dict[str, str]] = [{"url":"https://tx.yunjinginc.com/weblog"}]
    SWAGGER_LOGIN = f"/{PROJECT_NAME}/login/"
    SWAGGER_DOCS_URL: str = f'/{PROJECT_NAME}/docs'
    SWAGGER_REDOC_URL: str = f'/{PROJECT_NAME}/redocs'
    OPENAPI_URL: str = f'/{PROJECT_NAME}/openapi.json'
    SWAGGER_DESCRIPTION: str = f'{PROJECT_NAME}-测试环境API'
    # https://github.com/tiangolo/fastapi/issues/2633
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1}
    SWAGGER_UI_PARAMETERS: str = f'/{PROJECT_NAME}/docs/oauth2-redirect'
