from typing import AsyncGenerator

from fastapi import Request
from pymongo import MongoClient
from sqlalchemy.ext.asyncio import AsyncSession
from socketio.asyncio_server import AsyncServer
from app.extensions.db import async_session
from app.extensions.redis import MyRedis


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库连接"""
    async with async_session() as session:
        yield session


async def get_redis(request: Request) -> MyRedis:
    """获取redis连接"""
    return await request.app.state.redis

async def get_mongo(request: Request) -> MongoClient:
    """获取MongoDB链接"""
    return request.app.state.mongo


async def get_socketio(request: Request) -> AsyncServer:
    """获取socketio"""
    return request.app.state.sio