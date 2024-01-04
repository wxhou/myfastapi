from typing import AsyncGenerator
import motor.motor_asyncio
from fastapi import FastAPI, Depends
from slowapi import Limiter
from slowapi.util import get_ipaddr
from pymongo import MongoClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.extensions.db import async_session
from app.extensions.redis import AsyncRedis
from app.settings import settings
from .db import async_session, session
from .redis import init_redis_pool, redis_client
from .websocket import manager as websocket


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库连接"""
    async with async_session() as session:
        yield session


async def get_redis() -> AsyncRedis:
    """获取redis连接"""
    async with await init_redis_pool() as redis:
        yield redis


def get_mongo() -> MongoClient:
    """获取MongoDB链接"""
    return motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)


limiter = Limiter(key_func=get_ipaddr)



def register_extensions(app: FastAPI,
                        redis: AsyncRedis = Depends(get_redis),
                        mongo: MongoClient = Depends(get_mongo)):
    app.state.mongo = mongo
    app.state.redis = redis
    app.state.limiter = limiter
