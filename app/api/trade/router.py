from fastapi import APIRouter
from .views_admin import router_trade_admin


trade_router = APIRouter(tags=['Trade'])
trade_router.include_router(router_trade_admin, prefix='/admin')