from fastapi import APIRouter
from .views_admin import router_device_admin
from .views_client import router_device_client

device_router = APIRouter()
device_router.include_router(router_device_admin, prefix='/admin')
device_router.include_router(router_device_client, prefix='/client')