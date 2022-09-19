from fastapi import FastAPI
from app.api.base.router import base_router
from app.api.blog.router import blog_router
from app.api.message.router import message_router
from app.api.device.router import device_router

def register_router(app: FastAPI):
    """ 注册路由 """
    app.include_router(base_router, prefix='/base')
    app.include_router(blog_router, prefix='/blog')
    app.include_router(message_router, prefix='/message')
    app.include_router(device_router, prefix='/device')