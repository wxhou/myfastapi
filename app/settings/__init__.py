import os
from typing import Dict
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv('.env')

from app.settings.development import DevelopmentSettings
from app.settings.testing import TestingSettings
from app.settings.production import ProductionSettings


@lru_cache()
def get_settings():
    """获取配置信息"""
    env = os.getenv('MY_WEBLOG_ENV', None)
    env_config: Dict = {
        "development": DevelopmentSettings(),
        "testing": TestingSettings(),
        "production": ProductionSettings()
    }
    if env is None or env not in env_config:
        raise EnvironmentError("MY_WEBLOG_ENV is Undefined!")
    print(env)
    return env_config[env]


settings = get_settings()

if __name__ == '__main__':
    print(settings.BASEDIR)
