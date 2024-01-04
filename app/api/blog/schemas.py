from typing import Optional
from pydantic import BaseModel, Field



class PostInsert(BaseModel):
    """新建文章"""
    title: str = Field(max_length=64, description='标题')
    body: str = Field(max_length=2048, description='内容')
    category_id: int = Field(ge=1, description='分类ID')
    is_publish: bool = Field(False, description='是否发布')


class PostUpdate(BaseModel):
    """更新文章"""
    title: Optional[str] = Field(default=None, max_length=64, description='标题')
    body: Optional[str] = Field(default=None, max_length=2048, description='内容')
    category_id: Optional[int] = Field(default=None, ge=1, description='分类ID')
    is_publish: Optional[bool] = Field(default=None, description='是否发布')


class CommentInsert(BaseModel):
    post_id: int = Field(ge=1, description='文章ID')
    comment_id: int = Field(default=0, description='评论ID')
    content: str = Field(max_length=2048, description='评论内容')