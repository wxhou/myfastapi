from fastapi import APIRouter
from .views_admin import router_goods_admin


goods_router = APIRouter()
goods_router.include_router(router_goods_admin, prefix='/admin')