import redis.asyncio as aioredis
from redis.asyncio.client import PubSub


class RedisPubSubManger(object):
    """生产者消费者

    Args:
        object (_type_): _description_
    """

    def __init__(self, redis_con: aioredis.Redis = None, redis_url: str = None) -> None:
        if redis_con is None and redis_url is None:
            raise aioredis.ConnectionError("redis_con or redis_con is None")
        self.redis_con = redis_con or aioredis.from_url(redis_url)
        self.pubsub: PubSub = None

    def connect(self):
        """链接"""
        self.pubsub = self.redis_con.pubsub()

    async def publish(self, channel: str, message: str):
        """向频道推送消息

        Args:
            channel (str): _description_
            message (str): _description_
        """
        await self.redis_con.publish(channel=channel, message=message)

    async def subscribe(self, channel) -> PubSub:
        """订阅频道

        Args:
            channel (_type_): 频道名

        Returns:
            _type_: _description_
        """
        await self.pubsub.subscribe(channel)
        return self.pubsub

    async def unsubscribe(self, channel):
        """离开频道

        Args:
            channel (_type_): _description_
        """
        await self.pubsub.unsubscribe(channel)
