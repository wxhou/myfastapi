from typing import AsyncGenerator
from slowapi import Limiter
from slowapi.util import get_ipaddr
from .db import async_session, session, AsyncSession
from .cache import redis, aioredis, redis_client, Redis
from .mongo import mongo, mongo_client, MongoClient
from .websocket import WebsocketManager
from .scheduler import job_scheduler


limiter = Limiter(key_func=get_ipaddr)
websocket_manager = WebsocketManager()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库连接"""
    async with async_session() as session:
        yield session

def get_mongo() -> MongoClient:
    """获取MongoDB链接"""
    return mongo


def get_redis() -> aioredis.Redis:
    """获取redis连接"""
    return redis