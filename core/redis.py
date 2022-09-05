from aioredis import Redis
from .settings import settings


class CustomRedis(Redis):
    """自定义Redis"""
    pass

# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_redis_pool() -> Redis:
    redis = await Redis.from_url(url=settings.REDIS_URL,
                                 encoding=settings.GLOBAL_ENCODING,
                                 decode_responses=True)
    return redis
