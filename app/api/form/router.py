from fastapi import APIRouter
from .views import router_form_admin


form_router = APIRouter(tags=['Form'])
form_router.include_router(router_form_admin)