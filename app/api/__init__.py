# 把模型在此引入才能被alembic检测到
from .base.model import BaseUser, BaseRole, BasePermission
from .blog.model import Category, Post, Comment