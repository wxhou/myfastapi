from typing import Optional
from pydantic import BaseModel, Field


class InputText(BaseModel):
    """输入文本"""
    text: str = Field(max_length=2048, description='内容')