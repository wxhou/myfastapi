import os
import logging
from typing import List, Optional, Dict, Set, ClassVar
from pydantic_settings import BaseSettings



class ProductionSettings(BaseSettings):
    """生产配置"""
    PROJECT_NAME: ClassVar = 'weblog'
    BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DEBUG: bool = False
    PORT: int = 8199
    RELOAD: bool = False
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    GLOBAL_ENCODING: str = 'utf-8'
    CORS_ORIGINS: List[str] = ['*']
    PER_PAGE_NUMBER: int = 15
    PROFILING_ENABLED: bool=False

    # DB
    SQLALCHEMY_DATABASE: ClassVar = os.getenv("SQLALCHEMY_DATABASE")
    # MySQL(异步)
    SQLALCHEMY_DATABASE_ASYNC_URL: str = f"mysql+asyncmy://{SQLALCHEMY_DATABASE}?charset=utf8"
    # MySQL(同步)
    SQLALCHEMY_DATABASE_SYNC_URL: str = f"mysql+pymysql://{SQLALCHEMY_DATABASE}?charset=utf8"
    SQLALCHEMY_POOL_RECYCLE: int = 60 * 30
    SQLALCHEMY_POOL_PRE_PING: bool = True
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_ECHO: bool = False

    # Redis
    REDIS_URL: str = os.getenv('REDIS_URL')
    REDIS_SOCKETIO_URL: str = os.getenv('REDIS_SOCKETIO_URL')
    # MongoDB
    MONGO_URL: str = os.getenv('MONGO_URL')

    # celery
    CELERY_SECURITY_KEY: str = os.getenv('CELERY_SECURITY_KEY')
    CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND: str = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_REDBEAT_REDIS_URL: str = os.getenv('CELERY_REDBEAT_REDIS_URL')

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY')
    JWT_TOKEN_TYPE: str = os.getenv('JWT_TOKEN_TYPE')

    # MINIO
    MINIO_HOST: str = os.getenv('MINIO_HOST')
    MINIO_ACCESS_KEY: str = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = os.getenv('MINIO_SECRET_KEY')

    # alipay
    ALIPAY_SERVER_URL: str = os.getenv('ALIPAY_SERVER_URL')
    ALIPAY_APP_ID: str = os.getenv('ALIPAY_APP_ID')
    ALIPAY_APP_PRIVATE_KEY: str = os.getenv('ALIPAY_APP_PRIVATE_KEY')
    ALIPAY_PUBLIC_KEY: str = os.getenv('ALIPAY_PUBLIC_KEY')

    # email
    MAIL_SERVER: str = os.getenv('MAIL_SERVER')
    MAIL_PORT: int = os.getenv('MAIL_PORT')
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')

    # LOGGER
    LOGGER_LEVEL: int = logging.INFO
    LOGGER_FILE: str = './logs/server.log'
    LOGGER_FORMATTER: str = '[%(asctime)s] %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'

    # upload
    UPLOAD_MEDIA_FOLDER: ClassVar = os.path.join(BASEDIR, 'upload')
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS: Set[str] = {'.png', '.jpg', '.jpeg'}
    ALLOWED_AUDIO_EXTENSIONS: Set[str] = {'.mp3'}
    ALLOWED_VIDEO_EXTENSIONS: Set[str] = {'.mp4'}

    # SWAGGER
    SERVERS: Optional[str] = None
    SWAGGER_LOGIN: str = "/login/"
    SWAGGER_DOCS_URL: Optional[str] = None
    SWAGGER_REDOC_URL: Optional[str] = None
    OPENAPI_URL: str = "/openapi.json"
    SWAGGER_DESCRIPTION: str = f'{PROJECT_NAME}-生产环境API'
    # https://github.com/tiangolo/fastapi/issues/2633
    SWAGGER_SCHEMAS: Dict[str, int] = {"defaultModelsExpandDepth": -1}
    SWAGGER_UI_PARAMETERS: str = '/docs/oauth2-redirect'

    EDGE_VOICE_LANG: Dict[str, str] = {"zh": "zh-CN-XiaoxiaoNeural", 'en': 'en-CA-ClaraNeural'}