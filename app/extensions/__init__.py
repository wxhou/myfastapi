import motor.motor_asyncio
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_ipaddr
from app.core.settings import settings
from .db import async_session
from .redis import init_redis_pool, redis
from .websocket import manager as ws_manage


limiter = Limiter(key_func=get_ipaddr)



async def register_extensions(app: FastAPI):
    app.state.mongo = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
    app.state.redis = await init_redis_pool()
    app.state.limiter = limiter
