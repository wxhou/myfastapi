
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


    async def get_objects(self, model, query_filter: list=[]):
        objs = await self.db.scalars(select(model).where(*query_filter).offset(
            self.page_size * (self.page - 1)).limit(self.page_size))
        return objs.all()

    async def metadata(self, query_filter: list=[]):
        _total = await self.db.scalar(select(func.count()).where(*query_filter))
        _pages = int(ceil(_total / float(self.page_size)))
        return {"total": _total, "pages": _pages}

    async def __call__(self, model, query_filter=[]):
        if not query_filter:
            query_filter = [model.status==0]
        objs = await self.get_objects(model, query_filter)
        ret = {"data": [obj.to_dict() for obj in objs]}
        ret.update(await self.metadata(query_filter))
        return ret