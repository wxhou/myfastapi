from typing import Any
from aioredis import Redis as AsyncRedis
from app.common.resolve import load_object, dump_object
from app.utils.logger import logger
from app.core.settings import settings


class MyRedis(AsyncRedis):
    """自定义Redis"""

    async def get_pickle(self, key) -> Any:
        res = await self.get(key)
        return load_object(res)

    async def set_pickle(self, key, value, timeout=None, **kwargs):
        dump = dump_object(value)
        result = await self.set(key, value=dump, ex=timeout, **kwargs)
        return result

# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app


async def init_redis_pool() -> MyRedis:
    redis = await MyRedis.from_url(url=settings.REDIS_URL,
                                   encoding=settings.GLOBAL_ENCODING)
    return redis



from redis import Redis as SYNC_REDIS
from redis import ConnectionPool
redis = SYNC_REDIS(connection_pool=ConnectionPool.from_url(settings.REDIS_URL), decode_responses=True)