# https://www.osgeo.cn/sqlalchemy/orm/extensions/asyncio.html?highlight=async#asynchronous-i-o-asyncio

from asyncio import current_task
from sqlalchemy.sql.dml import Update, Delete
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker
from app.settings import settings


engine = create_engine(
    url=settings.SQLALCHEMY_DATABASE_SYNC_URL,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    echo=settings.SQLALCHEMY_ECHO
)
session = sessionmaker(engine)


async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_ASYNC_URL,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    echo=settings.SQLALCHEMY_ECHO,
    future=True
)

class AsyncRoutingSession(AsyncSession):
    """读写分离"""
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete)):
            return async_engine
        else:
            return async_engine


async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False # 防止提交后属性过期
)


async_session = async_scoped_session(async_session_factory, scopefunc=current_task)

# https://www.cnpython.com/qa/1324022