from fastapi import APIRouter
from .views_admin import router_device_admin


device_router = APIRouter(tags=['Device'])
device_router.include_router(router_device_admin, prefix='/admin', tags=['Base'])
