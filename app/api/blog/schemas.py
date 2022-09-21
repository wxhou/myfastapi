from typing import Optional
from pydantic import BaseModel, Field



class PostInsert(BaseModel):
    """新建文章"""
    title: str = Field(max_length=64, title='标题')
    body: str = Field(max_length=2048, title='内容')
    category_id: int = Field(ge=1, title='分类ID')
    is_publish: bool = Field(False, title='是否发布')


class PostUpdate(BaseModel):
    """更新文章"""
    id: int = Field(ge=1, title='文章ID')
    title: Optional[str] = Field(default=None, max_length=64, title='标题')
    body: Optional[str] = Field(default=None, max_length=2048, title='内容')
    category_id: Optional[int] = Field(default=None, ge=1, title='分类ID')
    is_publish: Optional[bool] = Field(default=None, title='是否发布')

class PostDelete(BaseModel):
    id: int = Field(ge=1, title='文章ID')


class CommentInsert(BaseModel):
    post_id: int = Field(ge=1, title='文章ID')
    comment_id: int = Field(default=0, title='评论ID')
    content: str = Field(max_length=2048, title='评论内容')