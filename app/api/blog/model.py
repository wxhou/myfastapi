from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Text
from app.api.model import Base


class Category(Base):
    """文章分类"""
    __tablename__ = "t_blog_category"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), unique=True)


class Post(Base):
    """文章"""
    __tablename__ = "t_blog_post"
    id = Column(BigInteger, primary_key=True)
    title = Column(String(64))  # 标题
    body = Column(Text)  # 内容
    user_id = Column(Integer, index=True) # 创建人ID
    category_id = Column(Integer, index=True) # 分类ID
    is_comment = Column(Boolean, default=True) # 是否可以评论
    is_publish = Column(Boolean) # 是否发布


class Comment(Base):
    """评论"""
    __tablename__ = "t_blog_comment"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, index=True) # 评论用户ID
    post_id = Column(Integer, index=True) # 文章ID
    parent_id =Column(Integer, default=0) # 父评论ID
    content = Column(Text)