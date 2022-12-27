from fastapi import APIRouter
from .views import router_admin
# from .views_role import router_role_admin


router = APIRouter()
router.include_router(router_admin, tags=['User'])
