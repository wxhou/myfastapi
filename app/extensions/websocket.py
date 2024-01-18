import asyncio
from typing import Dict
from fastapi import WebSocket
from app.common.channel import RedisPubSubManger, PubSub
from app.settings import settings
from app.utils.logger import logger


class WebsocketManager(object):
    """websocket manager

    Args:
        object (_type_): _description_
    """

    def __init__(self):
        self.channels: Dict[str, Dict[str, WebSocket]] = {}
        self.pubsub_client = RedisPubSubManger(redis_url=settings.REDIS_SOCKETIO_URL)


    def channel_connections(self, channel: str):
        """频道链接数

        Args:
            channel (_type_): 频道名

        Returns:
            _type_: _description_
        """
        if channel not in self.channels:
            return 0
        return len(self.channels[channel])

    async def add_to_channel(self, channel:str, _id: str, websocket: WebSocket):
        """加入频道

        Args:
            channel (str): _description_
            _id (str): _description_
            websocket (WebSocket): _description_
        """
        await websocket.accept()
        if channel in self.channels:
            self.channels[channel][_id] = websocket
        else:
            self.channels[channel] = {_id: websocket}
        self.pubsub_client.connect()
        pubsub_subscriber = await self.pubsub_client.subscribe(channel)
        asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))
        logger.bind(websocket=True).warning('Add to channel {} websocket id {}!'.format(channel, _id))


    async def leave_to_channel(self, channel, _id: str, websocket: WebSocket):
        """离开频道

        Args:
            channel (_type_): _description_
            _id (str): _description_
            websocket (WebSocket): _description_
        """
        _websocket = self.channels[channel].pop(_id)
        logger.bind(websocket=True).warning('Leave to channel {} websocket id {}!'.format(channel, _id))
        if _websocket != websocket:
            logger.bind(websocket=True).warning('Leave to channel websocket not diff!')
        if len(self.channels[channel]) == 0:
            self.channels.pop(channel)
            await self.pubsub_client.unsubscribe(channel)

    async def broadcast_to_channel(self, channel: str, message: str):
        """广播到频道

        Args:
            channel (str): _description_
            message (str): _description_
        """
        await self.pubsub_client.publish(channel, message)

    async def _pubsub_data_reader(self, pubsub_subscriber: PubSub):
        """Reads and broadcasts messages received from Redis PubSub.

        Args:
            pubsub_subscriber (_type_): _description_
        """
        while True:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True)
            if message is not None:
                logger.bind(websocket=True).info("Broadcast message: {}".format(message))
                _channel = message['channel'].decode('utf-8')
                for _, websocket in self.channels[_channel].items():
                    data = message['data'].decode('utf-8')
                    await websocket.send_text(data)
            await asyncio.sleep(0.01)