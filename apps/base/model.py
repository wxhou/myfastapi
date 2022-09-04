from datetime import datetime
from sqlalchemy import Column, String, SmallInteger, Integer, BigInteger, Boolean, Text, DATETIME
from apps.model import Base


class BaseUser(Base):
    """用户表"""
    __tablename__ = "t_base_user"
    id = Column(BigInteger, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    nickname = Column(String(64), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(254), unique=True, index=True)
    role_id = Column(Integer, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "email": self.email
        }


class BaseRole(Base):
    """角色表"""
    __tablename__ = "t_base_role"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), unique=True, index=True)  # 角色名称
    order_num = Column(String(64), unique=True, index=True)  # 排序


class BasePermission(Base):
    """权限表"""
    __tablename__ = "t_base_permission"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64))  # 名称
    function_name = Column(String(64), unique=True, index=True)  # 角色名称
    order_num = Column(String(64), unique=True, index=True)  # 排序
    remark = Column(String(512))


class RolePermission(Base):
    """角色权限关系表"""
    __tablename__ = 't_base_role_permission'
    id = Column(BigInteger, primary_key=True)
    role_id = Column(Integer, nullable=False, index=True)
    permission_id = Column(Integer, nullable=False, index=True)
