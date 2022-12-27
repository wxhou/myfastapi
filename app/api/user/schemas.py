from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    """注册用户"""
    username: str = Field(title='用户名', min_length=1, max_length=16)
    password: str = Field(title='密码', regex=r'[A-Za-z0-9]', min_length=8, max_length=16)
    nickname: str = Field(title='昵称', min_length=1, max_length=16)
    email: Optional[EmailStr] = Field(default=None, title='邮箱')


class UserModify(BaseModel):
    """
    修改用户schema
    """
    id: int = Field(title='用户ID', ge=1)
    username: str = Field(default=None, title='用户名', min_length=1, max_length=16)
    nickname: str = Field(default=None, title='昵称', min_length=1, max_length=16)
    email: Optional[EmailStr] = Field(default=None, title='邮箱')


class UserList(BaseModel):
    """
    修改用户schema
    """
    username: Optional[str] = Field(default=None, title='用户名', min_length=1, max_length=16)
    email: Optional[EmailStr] = Field(default=None, title='邮箱')


class UserAddressUpdate(BaseModel):
    """
    修改用户地址
    """
    id: int = Field(default=None, title='用户ID', ge=1)
    province: str = Field(default=None, title='省份', min_length=1, max_length=64)
    city: str = Field(default=None, title='城市', min_length=1, max_length=64)
    district: str = Field(default=None, title='区域')
    address: str = Field(default=None, title='详细地址', max_length=128)
    signer_name: str = Field(default=None, title='签收人', max_length=128)
    signer_mobile: str = Field(default=None, title='签收电话', max_length=11)
