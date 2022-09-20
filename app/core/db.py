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

# https://www.cnpython.com/qa/1324022
# sqlalchemy.exc.InvalidRequestError: A transaction is already begun on this Session.
# async def async_main():
#     engine = create_async_engine(
#         "postgresql+asyncpg://scott:tiger@localhost/test", echo=True,
#     )
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

#     async with AsyncSession(engine) as session:
#         async with session.begin():
#             session.add_all(
#                 [
#                     A(bs=[B(), B()], data="a1"),
#                     A(bs=[B()], data="a2"),
#                     A(bs=[B(), B()], data="a3"),
#                 ]
#             )

#         await session.run_sync(fetch_and_update_objects)

#         await session.commit()

#     # for AsyncEngine created in function scope, close and
#     # clean-up pooled connections
#     await engine.dispose()