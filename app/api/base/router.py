from fastapi import APIRouter
from .views import router as bs_router
from .views_user import router_base_admin
# from .views_role import router_role_admin

base_router = APIRouter()
base_router.include_router(bs_router, tags=['Base'])
base_router.include_router(router_base_admin, prefix='/user', tags=['User'])
# base_router.include_router(router_role_admin, prefix='/role', tags=['Role'])