from typing import AsyncGenerator
from slowapi import Limiter
from slowapi.util import get_ipaddr
from .db import async_session, session, AsyncSession
from .cache import init_redis_pool, redis_client, AsyncRedis
from .mongo import get_mongo, MongoClient
from .websocket import websocket_manager
from .scheduler import job_scheduler


limiter = Limiter(key_func=get_ipaddr)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库连接"""
    async with async_session() as session:
        yield session


async def get_redis() -> AsyncRedis:
    """获取redis连接"""
    async with await init_redis_pool() as redis:
        yield redis


def register_extensions(app):
    """注册插件"""
    pass