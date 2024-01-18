from redis import Redis
import redis.asyncio as aioredis
from app.settings import settings


redis = aioredis.from_url(
    url=settings.REDIS_URL,
    encoding=settings.GLOBAL_ENCODING
)


redis_client = Redis.from_url(
    url=settings.REDIS_URL,
    encoding=settings.GLOBAL_ENCODING
)