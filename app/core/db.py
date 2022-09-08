# https://www.osgeo.cn/sqlalchemy/orm/extensions/asyncio.html?highlight=async#asynchronous-i-o-asyncio

from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker
from .settings import settings


engine = create_async_engine(
    url=settings.ASYNC_SQLALCHEMY_DATABASE_URL,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    echo=settings.SQLALCHEMY_ECHO,
    future=True
)
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # 防止提交后属性过期
)


async_session = async_scoped_session(async_session_factory, scopefunc=current_task)