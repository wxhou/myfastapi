import os
from typing import Dict
from functools import lru_cache
from .development import DevelopmentSettings
from .testing import TestingSettings
from .production import ProductionSettings


@lru_cache()
def get_settings():
    """获取配置信息"""
    env = os.environ.get('MY_WEBLOG_ENV', None)
    env_config: Dict = {
        "development": DevelopmentSettings(),
        "testing": TestingSettings(),
        "production": ProductionSettings()
    }
    if env is None or env not in env_config:
        raise EnvironmentError("MY_WEBLOG_ENV is Undefined!")
    return env_config[env]


settings = get_settings()


from .celery import development, production, testing

@lru_cache()
def get_celery_settings():
    """获取celery配置信息"""
    env = os.environ.get('MY_WEBLOG_ENV', None)
    env_config: Dict = {
        "development": development,
        "testing": testing,
        "production": production
    }
    if env is None or env not in env_config:
        raise EnvironmentError("MY_WEBLOG_ENV is Undefined!")
    return env_config[env]

celery_settings = get_celery_settings()


if __name__ == '__main__':
    print(settings.BASEDIR)
