from datetime import datetime
from sqlalchemy import Column, String, SmallInteger, Integer, BigInteger, Boolean, Numeric, DATETIME
from app.api.model import Base


class FormTemplate(Base):
    """表单模板"""
    __tablename__ = 't_form_template'
    id = Column(Integer, primary_key=True)
    name = Column(String(128)) # 模板名称
    type = Column(SmallInteger)
    college = Column(String(128)) # 集合名称


class FormTemplateVersion(Base):
    """表单版本"""
    __tablename__ = 't_form_template_version'
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, index=True) # 模板ID
    object_id = Column(String(128), index=True) # mongo_ID
    is_active = Column(Boolean, default=False)  # 是否激活
    is_publish = Column(Boolean, default=False) # 是否发布
    creator_id = Column(Integer) # 用户ID


class FormFillRecord(Base):
    """表单填报记录"""
    __tablename__ = 't_form_fill_record'
    id = Column(BigInteger, primary_key=True)
    template_id = Column(Integer, index=True) # 模板ID
    object_id = Column(String(128)) # Template_object_ID
    fill_id = Column(String(128)) # 填报ID


##### 其他数据存储在MongoDB中 #####