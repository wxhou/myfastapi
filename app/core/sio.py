from typing import Optional
import dill as pickle
import socketio
from ast import literal_eval
from collections import namedtuple
from app.core.settings import settings
from app.extensions.redis import redis
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
    """心跳 10S一次"""
    msg = literal_eval(message)
    logger.bind(websocket=True).info("[Socket.IO] OD({}) heartbeat {} to:{}".format(
        len(sio_line), msg['DeviceID'], sid))
    await sio_line.heartbeat(sid=sid, client_id=msg['DeviceID'])


class SocketIOnline:
    """在线设备"""

    __slots__ = ('device', 'key_fix')

    def __init__(self):
        self.device = namedtuple('OnlineDevice', 'sid device_id timestamp')
        self.key_fix: str = "socketio_active_connection"

    def dump_object(self, value):
        """Dumps an object into a string for redis.  By default it serializes
        integers as regular string and pickle dumps everything else.
        """
        t = type(value)
        if t == int:
            return str(value).encode("ascii")
        return b"!" + pickle.dumps(value)

    def load_object(self, value):
        """The reversal of :meth:`dump_object`.  This might be called with
        None.
        """
        if value is None:
            return None
        if value.startswith(b"!"):
            try:
                return pickle.loads(value[1:])
            except pickle.PickleError:
                return None
        try:
            return int(value)
        except ValueError:
            # before 0.8 we did not have serialization.  Still support that.
            return value

    def socketio_online(self):
        """获取所有的对象"""
        return (self.load_object(x) for x in redis.smembers(self.key_fix))

    def sadd(self, value):
        """添加对象"""
        redis.sadd(self.key_fix, self.dump_object(value))

    def srem(self, value):
        """移除对象"""
        redis.srem(self.key_fix, self.dump_object(value))

    async def heartbeat(self, sid, client_id):
        """心跳检测"""
        _this = False
        for device in self.socketio_online():
            if (timestamp() - device.timestamp) > 10:
                self.srem(device)
            if device.device_id == client_id:
                device._replace(sid=sid, timestamp=timestamp())
                _this = True
        if not _this:
            self.sadd(self.device(sid=sid, device_id=client_id, timestamp=timestamp()))

    def __contains__(self, client_id):
        return any(ret.device_id == client_id for ret in self.socketio_online())

    def __len__(self):
        return redis.scard(self.key_fix)

    async def emit(self, event, data=None, to=None, room=None, skip_sid=None,
                   namespace=None, callback=None, **kwargs):
        """重新封装发送消息"""
        await sio.emit(event, data=data, to=to, room=room, skip_sid=skip_sid,
                       namespace=namespace, callback=callback, **kwargs)

    async def emit_dispatch(self, event, data=None, to: Optional[list]=None, room=None, skip_sid=None,
                   namespace=None, callback=None, **kwargs):
        """可以发送给多个客户端"""
        for d in self.socketio_online():
            if d.device_id in to:
                await self.emit(event, data=data, to=d.sid, room=room, skip_sid=skip_sid,
                               namespace=namespace, callback=callback, **kwargs)


sio_line = SocketIOnline()
