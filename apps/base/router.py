from fastapi import APIRouter
from .views_admin import router_base_admin

base_router = APIRouter(tags=['Base'])
base_router.include_router(router_base_admin, prefix='/admin')