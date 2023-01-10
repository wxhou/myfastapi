from typing import Optional, NamedTuple, Generator
import socketio
from ast import literal_eval
from collections import namedtuple
from app.common.resolve import load_object, dump_object
from app.core.settings import settings
from app.extensions.redis import redis
from app.utils.logger import logger
from app.utils.times import timestamp

"""
fastapi用gunicorn workers大于1时需要单独起服务,一般情况下用=1的
"""


mgr = socketio.AsyncRedisManager(settings.REDIS_SOCKETIO_URL)
sio = socketio.AsyncServer(
    client_manager=mgr,
    async_mode='asgi',
    cors_allowed_origins='*'
)
sio_app = socketio.ASGIApp(sio)


@sio.on("connect")
async def test_connect(sid: str, *args, **kwargs) -> None:
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} is connect")


@sio.on("disconnect")
async def test_discontect(sid: str) -> None:
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} close connect")


@sio.on("heartbeat")
async def test_heartbeat(sid: str, message) -> None:
    """心跳 10S一次"""
    msg = literal_eval(message)
    logger.bind(websocket=True).info("[Socket.IO] heartbeat {} to:{}".format(msg['DeviceID'], sid))