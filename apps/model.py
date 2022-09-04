from sqlalchemy import func, Column, DateTime, SmallInteger
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:

    # __mapper_args__ = {"eager_defaults": True}  # 防止 insert 插入后不刷新

    @declared_attr
    def status(cls):  # 创建时间
        return Column(SmallInteger, server_default="0", comment='状态')

    @declared_attr
    def create_time(cls):  # 创建时间
        return Column(DateTime(timezone=True), server_default=func.now(), comment='创建时间')

    @declared_attr
    def update_time(cls):  # 更新时间
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
