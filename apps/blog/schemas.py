from pydantic import BaseModel, constr, conint



class PostInsert(BaseModel):
    """新建文章"""
    title: str = constr(max_length=64)
    body: str = constr(max_length=2048)
    category_id: int = conint(ge=1)
    is_publish: bool = False