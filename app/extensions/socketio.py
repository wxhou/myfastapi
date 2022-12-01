import socketio
from fastapi import FastAPI
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
    async def test_connect(sid: str, *args, **kwargs):
        logger.bind(websocket=True).info(f"{sid} is connect")

    @sio.on("disconnect")
    async def test_discontect(sid: str, *args, **kwargs):
        logger.bind(websocket=True).info(f"{sid} close connect")