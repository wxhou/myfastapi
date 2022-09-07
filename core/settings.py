import os
from typing import List
from logging import DEBUG as debug_mode
from functools import lru_cache
from pydantic import BaseSettings, AnyHttpUrl


class DevelopmentSettings(BaseSettings):
    """"开发设置"""
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

    LOGGER_LEVEL: int = debug_mode
    LOGGER_FILE: str = './logs/server.log'
    LOGGER_FORMATTER: str = '[%(asctime)s] %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'

    # upload
    UPLOAD_MEDIA_FOLDER = os.path.join(BASEDIR, 'upload')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
    ALLOWED_AUDIO_EXTENSIONS = {'.mp3'}
    ALLOWED_VIDEO_EXTENSIONS = {'.mp4'}

    PERMISSION_DATA = {
        "admin": "管理员",
        "author": "作者",
        "user": "普通用户"
    }

    SWAGGER_DOCS_URL = '/docs'
    SWAGGER_REDOC_URL ='/redocs'
    SWAGGER_SCHEMAS = {"defaultModelsExpandDepth": -1} # https://github.com/tiangolo/fastapi/issues/2633

class TestingSettings(BaseSettings):
    """测试配置"""
    DEBUG = True
    PORT = 8099
    RELOAD = True
    SECRET_KEY = 'b7c890f9-983d-4950-9d99-228356a17203'

    ASYNC_SQLALCHEMY_DATABASE_URL = "mysql://root:root1234@127.0.0.1/db_weblog"
    REDIS_URL = "redis://localhost:6379/2"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"


class ProductionSettings(BaseSettings):
    """生产配置"""
    DEBUG = True
    PORT = 8099
    ASYNC_SQLALCHEMY_DATABASE_URL = ''
    SECRET_KEY = ''
    RELOAD = True


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
