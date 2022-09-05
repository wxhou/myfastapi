from typing import Optional, Union
from pydantic import BaseModel, EmailStr, constr, conint


class Token(BaseModel):
    """ token """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """token data"""
    username: Union[str, None] = None


class UserRegister(BaseModel):
    """注册用户"""
    username: constr(min_length=1, max_length=16)
    password: constr(regex=r'[A-Za-z0-9]', min_length=8, max_length=16)
    nickname: constr(min_length=1, max_length=16)
    email: EmailStr = None


class UserModify(BaseModel):
    """
    修改用户schema
    """
    id: conint(ge=1)
    username: Optional[str] = None
    nick_name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_id: Optional[int] = None

class UserList(BaseModel):
    """
    修改用户schema
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None