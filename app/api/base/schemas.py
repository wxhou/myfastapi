from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    """ token """
    access_token: str
    refresh_token: str
    token_type: str
    data: dict
    errcode: int

class RefreshToken(BaseModel):
    refresh_token: str = Field(title='刷新token')

class TokenData(BaseModel):
    """token data"""
    username: Optional[str] = None


class InputText(BaseModel):
    """输入文本"""
    text: str = Field(max_length=2048, title='内容')