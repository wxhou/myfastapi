from typing import Set
import socketio
from ast import literal_eval
from collections import namedtuple
from app.core.settings import settings
from app.utils.logger import logger
from app.utils.times import timestamp


mgr = socketio.AsyncRedisManager(settings.REDIS_URL)
sio = socketio.AsyncServer(
    client_manager=mgr,
    async_mode='asgi',
    cors_allowed_origins='*'
)
sio_app = socketio.ASGIApp(sio)


@sio.on("connect")
async def test_connect(sid: str, *args, **kwargs):
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} is connect")


@sio.on("disconnect")
async def test_discontect(sid: str):
    logger.bind(websocket=True).info(f"[Socket.IO] {sid} close connect")


@sio.on("heartbeat")
async def test_heartbeat(sid: str, message):
    """心跳"""
    msg = literal_eval(message)
    logger.bind(websocket=True).info("[Socket.IO] OD({}) heartbeat {} to:{}".format(
        len(sio_line), msg['DeviceID'], sid))
    sio_line.heartbeat(sid=sid, client_id=msg['DeviceID'])


class SocketIOnline:
    """在线设备"""

    __slots__ = ('device', 'active_devices')

    def __init__(self):
        self.device = namedtuple('OnlineDevice', 'sid device_id timestamp')
        self.active_devices: Set[self.device] = set()

    def heartbeat(self, sid, client_id):
        _this = False
        for device in self.active_devices.copy():
            if (timestamp() - device.timestamp) > 10:
                self.active_devices.remove(device)
            if device.device_id == client_id:
                device._replace(sid=sid, timestamp=timestamp())
                _this = True
        if not _this:
            self.active_devices.add(self.device(
                sid=sid, device_id=client_id, timestamp=timestamp()))

    def __len__(self):
        return len(self.active_devices)

    async def emit(self, event, data=None, to=None, room=None, skip_sid=None,
                   namespace=None, callback=None, **kwargs):
        """重新封装发送消息"""
        _to = [d.sid for d in self.active_devices if d.device_id in to] if to else None
        await sio.emit(event, data=data, to=_to, room=room, skip_sid=skip_sid,
                       namespace=namespace, callback=callback, **kwargs)


sio_line = SocketIOnline()
