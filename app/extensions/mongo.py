import motor.motor_asyncio
from pymongo import MongoClient
from app.settings import settings



mongo: MongoClient = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)

mongo_client: MongoClient = MongoClient(settings.MONGO_URL)