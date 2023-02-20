
from math import ceil
from sqlalchemy import func, select



class PageNumberPagination(object):

    def __init__(self, db,
                page,
                page_size,
                ) -> None:
        self.db = db
        self.page = page
        self.page_size = page_size


    async def __call__(self, model, query_filter=[]):
        if not query_filter:
            query_filter = [model.status==0]
        objs = await self.db.scalars(select(model).where(*query_filter).offset(
            self.page_size * (self.page - 1)).limit(self.page_size))
        _total = await self.db.scalar(select(func.count()).where(*query_filter))
        _pages = int(ceil(_total / float(self.page_size)))
        return {"data": [obj.to_dict() for obj in objs], "total": _total, "pages": _pages}