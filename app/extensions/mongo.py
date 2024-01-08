import motor.motor_asyncio
from pymongo import MongoClient
from app.settings import settings



def get_mongo() -> MongoClient:
    """获取MongoDB链接"""
    return motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)




mongo_client: MongoClient = MongoClient(settings.MONGO_URL)