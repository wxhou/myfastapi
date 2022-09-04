# https://www.osgeo.cn/sqlalchemy/orm/extensions/asyncio.html?highlight=async#asynchronous-i-o-asyncio

from asyncio import current_task
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import as_declarative, sessionmaker, declared_attr
from .settings import settings


engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    future=True
)
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # 防止提交后属性过期
)


async_session = async_scoped_session(async_session_factory, scopefunc=current_task)