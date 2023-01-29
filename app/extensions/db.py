# https://www.osgeo.cn/sqlalchemy/orm/extensions/asyncio.html?highlight=async#asynchronous-i-o-asyncio

from asyncio import current_task
from sqlalchemy.sql.dml import Update, Delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker
from ..core.settings import settings


engine = create_async_engine(
    url=settings.ASYNC_SQLALCHEMY_DATABASE_URL,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    echo=settings.SQLALCHEMY_ECHO,
    future=True
)

class AsyncRoutingSession(AsyncSession):
    """读写分离"""
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete)):
            return engine
        else:
            return engine


async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False # 防止提交后属性过期
)


async_session = async_scoped_session(async_session_factory, scopefunc=current_task)

# https://www.cnpython.com/qa/1324022