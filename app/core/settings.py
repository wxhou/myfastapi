import os
from functools import lru_cache
from app.config.development import DevelopmentSettings
from app.config.testing import TestingSettings
from app.config.production import ProductionSettings


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
