from fastapi import APIRouter
from .views import router as admin_router


system_router = APIRouter()
system_router.include_router(admin_router, tags=['System'])