from typing import Optional, List, Literal
from pydantic import BaseModel, Field



class TemplateInsert(BaseModel):
    """新建模板"""
    name: str = Field(title="模板名称", min_length=1, max_length=128)
    type: Literal[1,2,3] = Field(title='模板分类', description="1:2:3:")