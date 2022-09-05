from fastapi import FastAPI
from apps.base.router import base_router
from apps.blog.router import blog_router


def register_router(app: FastAPI):
    """ 注册路由 """
    app.include_router(base_router, prefix='/base')
    app.include_router(blog_router, prefix='/blog')