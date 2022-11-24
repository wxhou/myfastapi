import time
import socketio
from fastapi import FastAPI, Depends, Request
from app.api.deps import get_db, get_redis, MyRedis
from app.core.settings import settings
from app.utils.logger import logger

def register_socketio(app: FastAPI):
    sio = socketio.AsyncServer(async_mode='asgi',
                               cors_allowed_origins=[] # https://github.com/miguelgrinberg/python-socketio/issues/205
                               )
    asgi = socketio.ASGIApp(sio)
    app.mount('/ws', asgi, name='socket')
    app.state.sio = sio

    @sio.on("connect")
    async def test_connect(sid: str, request: Request, *args, **kwargs):
        logger.bind(websocket=True).info(request.get('headers'))
        logger.bind(websocket=True).info(f"{sid} is connect")

    @sio.on("disconnect")
    async def test_discontect(sid: str, *args, **kwargs):
        logger.bind(websocket=True).info(f"{sid} close connect")

    @sio.on('heartbeat')
    async def device_heartbeat(sid:str , message, redis: MyRedis = Depends(get_redis)):
        _timestamp = int(time.time()*1000)
        await redis.hset('jl_online_device', message['DeviceID'], _timestamp)
        onlines = await redis.hgetall('jl_online_device')
        for k, v in onlines:
            if v <= (_timestamp - 10 * 60 * 1000):
                await redis.hdel('jl_online_device', k)