from datetime import datetime, date
from sqlalchemy import func, Column, DateTime, SmallInteger
from sqlalchemy.orm import DeclarativeBase
from fastapi.encoders import jsonable_encoder


class Base(DeclarativeBase):

    __mapper_args__ = {"eager_defaults": True}  # 防止 insert 插入后不刷新,如不添加created update不显示,但是会增加性能消耗
    # https://www.wenjiangs.com/doc/sqlalchemy-orm-mapping_api

    status = Column(SmallInteger, server_default="0", comment='是否删除')
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @property
    def fields(self):
        return (field for field in self.__dict__.keys() if not field.startswith('_'))

    def to_dict(self,
                exclude={'status'},
                custom_encoder={
                    date: lambda dt: dt.strftime("%Y-%m-%d"),
                    datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
                }):
        return jsonable_encoder(self, exclude=exclude, custom_encoder=custom_encoder)