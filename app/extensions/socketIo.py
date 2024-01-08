from typing import NamedTuple, AsyncGenerator

try:
    import socketio
except ImportError:
    pass
from ast import literal_eval
from collections import namedtuple
from app.common.resolve import load_object, dump_object

from app.settings import settings
from app.extensions import redis_client
from app.utils.logger import logger
from app.utils.times import timestamp



mgr = socketio.AsyncRedisManager(settings.REDIS_SOCKETIO_URL)
async_socket_io = socketio.AsyncServer(async_mode='asgi',
                            client_manager=mgr,
                            cors_allowed_origins=[]) # https://github.com/miguelgrinberg/python-socketio/issues/205
socket_io_asgi = socketio.ASGIApp(async_socket_io)


class SocketIOnline(object):
    """在线设备"""

    __slots__ = ('device', 'key_fix')

    def __init__(self):
        self.device: NamedTuple = namedtuple('OnlineDevice', 'sid device_id timestamp')
        self.key_fix: str = "socketio_active_connection"

    async def socketio_online(self) -> AsyncGenerator:
        """获取所有的对象"""
        return (load_object(x) for x in redis_client.smembers(self.key_fix))

    def sadd(self, value) -> None:
        """添加对象"""
        redis_client.sadd(self.key_fix, dump_object(value))

    def srem(self, value) -> None:
        """移除对象"""
        redis_client.srem(self.key_fix, dump_object(value))

    async def heartbeat(self, sid, client_id) -> None:
        """心跳检测"""
        _this = False
        async for device in self.socketio_online():
            if device.device_id == client_id:
                device._replace(sid=sid, timestamp=timestamp())
                _this = True
            if (timestamp() - device.timestamp) > 10:
                self.srem(device)
        if not _this:
            self.sadd(self.device(sid=sid, device_id=client_id, timestamp=timestamp()))

    def __contains__(self, client_id) -> bool:
        return any(ret.device_id == client_id async for ret in self.socketio_online())

    def __len__(self) -> int:
        return redis_client.scard(self.key_fix)

    async def get_sid(self, client_ids: list):
        """获取SID列表"""
        return [ret.sid async for ret in self.socketio_online() if ret.device_id in client_ids]


SocketIoOnline = SocketIOnline()


@async_socket_io.on("connect")
async def test_connect(sid: str, *args, **kwargs):
    """链接

    Args:
        sid (str): _description_
    """
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} is connect")

@async_socket_io.on("disconnect")
async def test_discontect(sid: str):
    """断开链接

    Args:
        sid (str): _description_
    """
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} close connect")


@async_socket_io.on('heartbeat')
async def device_heartbeat(sid:str , message):
    """_summary_
    心跳
    Args:
        sid (str): _description_
        message (_type_): _description_
    """
    msg = literal_eval(message)
    logger.bind(websocket=True).info("[Socket.IO] OD({}) heartbeat {} to:{}".format(
        len(SocketIoOnline), msg['DeviceID'], sid))
    await SocketIoOnline.heartbeat(sid=sid, client_id=msg['DeviceID'])

