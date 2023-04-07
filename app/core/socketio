from typing import Optional, NamedTuple, Generator
import socketio
from ast import literal_eval
from collections import namedtuple
from app.common.resolve import load_object, dump_object
from app.core.settings import settings
from app.extensions.redis import redis
from app.utils.logger import logger
from app.utils.times import timestamp



mgr = socketio.AsyncRedisManager(settings.REDIS_SOCKETIO_URL)
sio = socketio.AsyncServer(async_mode='asgi',
                            client_manager=mgr,
                            cors_allowed_origins=[]) # https://github.com/miguelgrinberg/python-socketio/issues/205
sio_asgi = socketio.ASGIApp(sio)


@sio.on("connect")
async def test_connect(sid: str, *args, **kwargs):
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} is connect")

@sio.on("disconnect")
async def test_discontect(sid: str, *args, **kwargs):
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} close connect")


@sio.on('heartbeat')
async def device_heartbeat(sid:str , message):
    msg = literal_eval(message)
    logger.bind(websocket=True).info("[Socket.IO] OD({}) heartbeat {} to:{}".format(
        len(sio_online), msg['DeviceID'], sid))
    await sio_online.heartbeat(sid=sid, client_id=msg['DeviceID'])



class SocketIOnline(object):
    """在线设备"""

    __slots__ = ('device', 'key_fix')

    def __init__(self):
        self.device: NamedTuple = namedtuple('OnlineDevice', 'sid device_id timestamp')
        self.key_fix: str = "socketio_active_connection"

    def socketio_online(self) -> Generator:
        """获取所有的对象"""
        return (load_object(x) for x in redis.smembers(self.key_fix))

    def sadd(self, value) -> None:
        """添加对象"""
        redis.sadd(self.key_fix, dump_object(value))

    def srem(self, value) -> None:
        """移除对象"""
        redis.srem(self.key_fix, dump_object(value))

    async def heartbeat(self, sid, client_id) -> None:
        """心跳检测"""
        _this = False
        for device in self.socketio_online():
            if device.device_id == client_id:
                device._replace(sid=sid, timestamp=timestamp())
                _this = True
            if (timestamp() - device.timestamp) > 10:
                self.srem(device)
        if not _this:
            self.sadd(self.device(sid=sid, device_id=client_id, timestamp=timestamp()))

    def __contains__(self, client_id) -> bool:
        return any(ret.device_id == client_id for ret in self.socketio_online())

    def __len__(self) -> int:
        return redis.scard(self.key_fix)

    async def get_sid(self, client_ids: list):
        """获取SID列表"""
        return [ret.sid for ret in self.socketio_online() if ret.device_id in client_ids]


sio_online = SocketIOnline()