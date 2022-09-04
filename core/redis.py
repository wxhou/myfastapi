from aioredis import Redis
from .settings import settings


# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_redis_pool() -> Redis:
    redis = await Redis.from_url(url=settings.REDIS_URL,
                                 encoding=settings.GLOBAL_ENCODING,
                                 decode_responses=True)
    return redis
