from fastapi import APIRouter
from .views import router as bs_router

base_router = APIRouter()
base_router.include_router(bs_router, tags=['Base'])
