import time
import socketio
from fastapi import FastAPI, Depends
from app.api.deps import get_db, get_redis, MyRedis
from app.core.settings import settings
from app.utils.logger import logger


mgr = socketio.AsyncRedisManager(settings.REDIS_URL)
sio = socketio.AsyncServer(
    client_manager=mgr,
    async_mode='asgi',
    cors_allowed_origins='*'
)
sio_app = socketio.ASGIApp(sio)


@sio.on("connect")
async def test_connect(sid: str, *args, **kwargs):
    logger.bind(websocket=True).info(f"{sid} is connect")

@sio.on("disconnect")
async def test_discontect(sid: str, *args, **kwargs):
    logger.bind(websocket=True).info(f"{sid} close connect")