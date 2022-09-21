import pickle
from typing import Any
from aioredis import Redis
from app.utils.logger import logger
from .settings import settings


class MyRedis(Redis):
    """自定义Redis"""

    def dump_object(self, value):
        """Dumps an object into a string for redis.  By default it serializes
        integers as regular string and pickle dumps everything else.
        """
        t = type(value)
        if t == int:
            return str(value).encode("ascii")
        return b"!" + pickle.dumps(value)

    def load_object(self, value):
        """The reversal of :meth:`dump_object`.  This might be called with
        None.
        """
        if value is None:
            return None
        if value.startswith(b"!"):
            try:
                return pickle.loads(value[1:])
            except pickle.PickleError:
                return None
        try:
            return int(value)
        except ValueError:
            # before 0.8 we did not have serialization.  Still support that.
            return value

    async def get_pickle(self, key) -> Any:
        res = await self.get(key)
        return self.load_object(res)

    async def set_pickle(self, key, value, timeout=None, **kwargs):
        dump = self.dump_object(value)
        result = await self.set(key, value=dump, ex=timeout, **kwargs)
        return result

# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_redis_pool() -> MyRedis:
    redis = await MyRedis.from_url(url=settings.REDIS_URL,
                                 encoding=settings.GLOBAL_ENCODING)
    return redis
