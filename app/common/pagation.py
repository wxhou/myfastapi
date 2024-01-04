
from math import ceil
from sqlalchemy import func, select
from fastapi import Depends, Query
from app.extensions import get_db, AsyncSession


class PageNumberPagination(object):

    def __init__(self, db: AsyncSession = Depends(get_db),
                page: int =  Query(default=1, description='页数'),
                page_size: int = Query(default=15, description='每页数量'),
                ) -> None:
        self.db = db
        self.page = page
        self.page_size = page_size

    async def metadata(self, query_filter: list):
        _total = await self.db.scalar(select(func.count()).where(*query_filter))
        _pages = int(ceil(_total / float(self.page_size)))
        return {"total": _total, "pages": _pages}

    async def __call__(self, model, query_filter=None, order_by=None):
        if not query_filter is None:
            query_filter = [model.status==0]
        if order_by is None:
            order_by = model.id.desc()
        objs = await self.db.stream_scalars(select(model).where(*query_filter).order_by(order_by).offset(
            self.page_size * (self.page - 1)).limit(self.page_size), execution_options={'execution_options': True, 'max_row_buffer': 1000})
        ret = {"data": [obj.to_dict() async for obj in objs.yield_per(self.page_size)]}
        ret.update(await self.metadata(query_filter))
        return ret