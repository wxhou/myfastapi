from fastapi import APIRouter
from .views_admin import router_message_admin

message_router = APIRouter()
message_router.include_router(router_message_admin, prefix='/admin')
