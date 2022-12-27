from sqlalchemy import Column, String, SmallInteger, Integer, BigInteger, Boolean, Text, DATETIME
from app.api.model import Base


class UploadModel(Base):
    """文件上传"""
    __tablename__ = 't_base_upload'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer) # 用户ID
    uniqueId = Column(String(128), unique=True)
    filename = Column(String(128)) # 图片名称
    fileUrl = Column(String(256)) # 图片地址
    content_type = Column(String(128))