import databases
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from .settings import settings


Base = MetaData()
database = databases.Database(settings.SQLALCHEMY_DATABASE_URL)
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Base.create_all(engine)