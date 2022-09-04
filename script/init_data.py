import os
import sys
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
from core.db import engine, Base


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"创建表失败!!! -- 错误信息如下:\n{e}")
    finally:
        await engine.dispose()


async def drop_db():
    """ 删除 models/__init__ 下的所有表 """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("删除表成功!!!")
    except Exception as e:
        print(f"删除表失败!!! -- 错误信息如下:\n{e}")
    finally:
        await engine.dispose()


if __name__ == '__main__':
    import asyncio
    asyncio.run(init_db())
