import os
import sys
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
import asyncio

from sqlalchemy import select, values
from apps.blog.model import Category
from core.db import async_session


async def init_category(cname):
    async with async_session() as session:
        sql = select(Category).where(Category.name == cname)
        obj = await session.scalar(sql)
        if obj is None:
            obj = Category(name=cname)
            session.add(obj)
            await session.commit()


async def init_category_names():
    """初始化文章分类"""
    category_names = ("python", "selenium")
    cnames = [init_category(cname) for cname in category_names]
    await asyncio.gather(*cnames)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_category_names())
