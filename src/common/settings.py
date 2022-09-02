import os
from functools import lru_cache
from pydantic import BaseSettings



class DevelopmentSettings(BaseSettings):
    """"开发设置"""
    DEBUG = True
    PORT = 8099
    SQLALCHEMY_DATABASE_URL = ''
    SECRET_KEY = ''
    RELOAD = True


class TestingSettings(BaseSettings):
    """测试配置"""
    DEBUG = True
    PORT = 8099
    SQLALCHEMY_DATABASE_URL = ''
    SECRET_KEY = ''
    RELOAD = True


class ProductionSettings(BaseSettings):
    """生产配置"""
    DEBUG = True
    PORT = 8099
    SQLALCHEMY_DATABASE_URL = ''
    SECRET_KEY = ''
    RELOAD = True


@lru_cache()
def get_settings():
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