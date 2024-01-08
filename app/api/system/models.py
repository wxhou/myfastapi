from sqlalchemy import Column, String, BigInteger, SmallInteger
from app.api.model import Base




class LogLogin(Base):
    """登录日志"""
    __tablename__ = 't_log_login'
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger, index=True)
    uname = Column(String(64))
    ip_addr = Column(String(64))
    ip_position = Column(String(64))
    client_type = Column(String(64))
    client_brower = Column(String(64))
    client_app = Column(String(16), doc='自主登录|三方验证')
    remark = Column(String(128))


class LogOperation(Base):
    """操作日志"""
    __tablename__ = 't_log_operation'
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger, index=True)
    uname = Column(String(64))
    ip_addr = Column(String(64))
    ip_position = Column(String(64))
    module = Column(String(64))
    type_op = Column(String(32))
    detail = Column(String(1024))