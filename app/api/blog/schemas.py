from typing import Optional
from pydantic import BaseModel, constr, conint



class PostInsert(BaseModel):
    """新建文章"""
    title: constr(max_length=64)
    body: constr(max_length=2048)
    category_id: conint(ge=1)
    is_publish: bool = False


class PostUpdate(BaseModel):
    """更新文章"""
    id: conint(ge=1)
    title: Optional[constr(max_length=64)]
    body: Optional[constr(max_length=2048)]
    category_id: Optional[conint(ge=1)]
    is_publish: Optional[bool] = None

class PostDelete(BaseModel):
    id: conint(ge=1)


class CommentInsert(BaseModel):
    post_id: conint(ge=1)
    comment_id: conint(ge=0) = 0
    content: constr(max_length=2048)