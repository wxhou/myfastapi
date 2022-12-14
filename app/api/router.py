from fastapi import FastAPI
from app.api.base.views_login import router_login
from app.api.base.router import base_router
from app.api.blog.router import blog_router
from app.api.message.router import message_router
from app.api.device.router import device_router
from app.api.goods.router import goods_router
from app.api.trade.router import trade_router
from app.api.form.router import form_router
from app.api.user.router import router as user_router


def register_router(app: FastAPI):
    """ 注册路由 """
    app.include_router(router_login)
    app.include_router(base_router, prefix='/base')
    app.include_router(blog_router, prefix='/blog')
    app.include_router(message_router, prefix='/message')
    app.include_router(device_router, prefix='/device')
    app.include_router(goods_router, prefix='/goods')
    app.include_router(trade_router, prefix='/trade')
    app.include_router(form_router, prefix='/form')
    app.include_router(user_router, prefix='/user')