from fastapi import FastAPI
from apps.base.router import base_router



def register_router(app: FastAPI):
    """ 注册路由 """
    app.include_router(base_router, prefix='/base')