from typing import Optional, Union, List
from pydantic import BaseModel, Field, EmailStr, constr, conint


class Token(BaseModel):
    """ token """
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str = Field(title='刷新token')

class TokenData(BaseModel):
    """token data"""
    username: Optional[str] = None

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