from typing import Annotated, AsyncGenerator
import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends
from slowapi import Limiter
from slowapi.util import get_ipaddr
from pymongo import MongoClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.extensions.db import async_session
from app.extensions.redis import AsyncRedis
from app.settings import settings
from .db import async_session
from .redis import init_redis_pool, redis
from .websocket import manager as websocket


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库连接"""
    async with async_session() as session:
        yield session


async def get_redis(request: Request) -> AsyncRedis:
    """获取redis连接"""
    return await request.app.state.redis

async def get_mongo(request: Request) -> MongoClient:
    """获取MongoDB链接"""
    return request.app.state.mongo


async_db = Annotated[AsyncSession, Depends(get_db)]
async_redis = Annotated[AsyncRedis, Depends(get_redis)]
async_mongo = Annotated[MongoClient, Depends(get_mongo)]
limiter = Limiter(key_func=get_ipaddr)



async def register_extensions(app: FastAPI):
    app.state.mongo = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
    app.state.redis = await init_redis_pool()
    app.state.limiter = limiter
