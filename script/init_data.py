import json, click
from sqlalchemy import select, values, delete
from app.extensions.db import engine, async_session
from app.utils.logger import logger
from app.utils.randomly import random_str

from app.api.model import Base
from app.api.user.model import BaseUser
from app.api.goods.model import Goods, GoodsCategory
from app.common.security import set_password

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()


async def init_super_user(username, password, email, nickname):
    async with async_session() as db:
        obj = await db.execute(select(BaseUser).where(BaseUser.status==0))
        if obj.first():
            click.echo('######Super User is Exists!######')
            return
        obj = BaseUser(username=username,
                       email=email,
                       nickname=nickname)
        db.add(obj)
        obj.is_active=True
        obj.password_hash = set_password(password)
        await db.commit()


async def init_goods_category():
    async with async_session() as db:
        await db.execute(delete(GoodsCategory))
        fp = open('./script/data/goods_category.json')
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
        async with db.begin():
            await db.execute(delete(Goods))
            fp = open('./script/data/goods.json')
            for row in json.load(fp):
                cate_id = await db.scalar(select(GoodsCategory.id).where(GoodsCategory.name==row['categorys'][-1]))
                obj = Goods(goods_name=row['name'],
                    market_price=int(row['market_price'][1:-1]),
                    goods_brief=row['desc'],
                    goods_sn=random_str(),
                    shop_price=int(row['sale_price'][1:-1]),
                    category_id=cate_id)
                db.add(obj)
            fp.close()
            await db.commit()