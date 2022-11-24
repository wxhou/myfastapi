import os
import sys
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
import json

from sqlalchemy import select, values, delete
from app.core.db import async_session
from app.utils.logger import logger
from app.utils.snowflake import snow_flake
from app.api.goods.model import Goods, GoodsCategory



async def init_goods_category():
    async with async_session() as db:
        await db.execute(delete(GoodsCategory))
        fp = open(os.path.join(BASE_DIR, 'script', 'data', 'goods_category.json'))
        for lev1_cat in json.load(fp):
            lev1_cat_obj = GoodsCategory(name=lev1_cat['name'], code=lev1_cat['code'])
            db.add(lev1_cat_obj)
            await db.flush()
            for lev2_cat in lev1_cat['sub_categorys']:
                lev2_cat_obj = GoodsCategory(name=lev2_cat['name'], code=lev2_cat['code'], parent_id=lev1_cat_obj.id)
                db.add(lev2_cat_obj)
                await db.flush()
                for lev3_cat in lev1_cat['sub_categorys']:
                    lev3_cat_obj = GoodsCategory(name=lev3_cat['name'], code=lev3_cat['code'], parent_id=lev2_cat_obj.id)
                    db.add(lev3_cat_obj)
                    await db.flush()
        fp.close()
        await db.commit()


async def init_goods():
    async with async_session() as db:
        await db.execute(delete(Goods))
        fp = open(os.path.join(BASE_DIR, 'script', 'data', 'goods.json'))
        for row in json.load(fp):
            cate_id = await db.scalar(select(GoodsCategory.id).where(GoodsCategory.name==row['categorys'][-1]))
            obj = Goods(goods_name=row['name'],
                  market_price=int(row['market_price'][1:-1]),
                  goods_brief=row['desc'],
                  goods_sn=snow_flake.get_id(),
                  shop_price=int(row['sale_price'][1:-1]),
                  category_id=cate_id)
            db.add(obj)
        fp.close()
        await db.commit()


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_goods())
