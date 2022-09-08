from fastapi import APIRouter
from .views_admin import router_base_admin
# from .views_role import router_role_admin

base_router = APIRouter()
base_router.include_router(router_base_admin, prefix='/admin', tags=['Base'])
# base_router.include_router(router_role_admin, prefix='/role', tags=['Role'])