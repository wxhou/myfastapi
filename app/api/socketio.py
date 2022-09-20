import logging
import socketio
from fastapi import FastAPI, Depends
from app.api.deps import get_db, get_redis, MyRedis
from app.core.settings import settings

websocket_logger = logging.getLogger('websocket')

def register_socketio(app: FastAPI):
    # https://github.com/miguelgrinberg/python-socketio/issues/205
    sio = socketio.AsyncServer(async_mode='asgi',
                               cors_allowed_origins=[],
                               logger=True,
                               engineio_logger=True)
    asgi = socketio.ASGIApp(sio)
    app.mount('/ws', asgi, name='socket')

    @sio.on("connect")
    async def test_connect(sid: str, *args, **kwargs):
        websocket_logger.info(f"{sid} is connect")

    @sio.on("disconnect")
    async def test_discontect(sid: str, *args, **kwargs):
        websocket_logger.info(f"{sid} close connect")

    @sio.on('heartbeat')
    async def device_heartbeat(sid:str , message, redis: MyRedis = Depends(get_redis)):
        if not (await redis.sismember('jl_online_device', message['DeviceID'])):
            await redis.sadd('jl_online_device', message['DeviceID'])