from sqlalchemy import Column, String, SmallInteger, Integer, BigInteger, Boolean, Text, JSON
from app.api.model import Base


class BaseUser(Base):
    """用户表"""
    __tablename__ = "t_base_user"
    id = Column(BigInteger, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    nickname = Column(String(64), unique=True, index=True)
    password_hash = Column(String(255))
    phone = Column(String(11)) # 手机
    email = Column(String(254), unique=True, index=True) # 邮箱
    avatar_id = Column(Integer, index=True) # 头像ID
    is_active = Column(Boolean, default=0, nullable=False) # 是否激活

    def __str__(self) -> str:
        return "{}({})".format(self.username, self.id)

    def to_dict(self):
        return super().to_dict(exclude={'status', 'password_hash', 'is_active'})

class BaseRole(Base):
    """角色表"""
    __tablename__ = "t_base_role"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), unique=True, index=True)  # 角色名称
    order_num = Column(String(64), unique=True, index=True)  # 排序



class UserRole(Base):
    __tablename__ = 't_base_user_role'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    role_id = Column(BigInteger, nullable=False, index=True)


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
    role_id = Column(BigInteger, nullable=False, index=True)
    permission_id = Column(BigInteger, nullable=False, index=True)


class DataRule(Base):
    __tablename__ = 't_base_data_rule'
    id = Column(BigInteger, primary_key=True)
    rule_name = Column(String(128)) #
    rule_conditions = Column(String(128))
    rule_values = Column(JSON) # ARRAY(INTEGER)


class DataRuleSet(Base):
    __tablename__ = 't_base_data_rule_set'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(128)) # 名称
    column = Column(JSON) # 字段 ARRAY(INTEGER)
    op_type = Column(SmallInteger, default=1) # 1,2
    rule_id = Column(BigInteger)



class UserCollect(Base):
    """用户收藏"""
    __tablename__ = 't_base_user_collect'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True) # 用户ID
    goods_id = Column(Integer, index=True) # 商品ID


class UserAddress(Base):
    __tablename__ = 't_base_user_address'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True) # 用户ID
    province = Column(String(64)) # 省份
    city = Column(String(64)) # 城市
    district = Column(String(128)) # 区域
    address = Column(String(128)) # 详细地址
    signer_name = Column(String(128)) # 签收人
    signer_mobile = Column(String(11)) # 签收电话


class UserComment(Base):
    """用户评论"""
    __tablename__ = 't_base_user_comment'
    id = Column(Integer, primary_key=True)
    msg_type = Column(SmallInteger) # "留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)"
    subject = Column(String(64)) # 主题
    message = Column(String(128)) # 浏览内容
    file_id = Column(Integer, index=True) # 图片ID