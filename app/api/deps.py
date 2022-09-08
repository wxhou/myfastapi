from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session
from app.core.redis import Redis


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库连接"""
    async with async_session() as session:
        yield session


async def get_redis(request: Request) -> Redis:
    """获取redis连接"""
    return await request.app.state.redis


