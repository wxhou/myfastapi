from fastapi import APIRouter
from .views_admin import router_blog_admin


blog_router = APIRouter(tags=['Blog'])
blog_router.include_router(router_blog_admin, prefix='/admin')