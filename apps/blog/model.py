from datetime import datetime
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Text
from apps.model import Base


class Category(Base):
    """文章分类"""
    __tablename__ = "t_blog_category"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "is_comment": self.is_comment,
            "is_publish": self.is_publish,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class Comment(Base):
    """评论"""
    __tablename__ = "t_blog_comment"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, index=True) # 评论用户ID
    post_id = Column(Integer, index=True) # 文章ID
    parent_id =Column(Integer, default=0) # 父评论ID
    content = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.id,
            "comment_id": self.parent_id,
            "content": self.content,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }