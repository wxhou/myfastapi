import traceback
from typing import Optional
from math import ceil
from datetime import timedelta
from jose import jwt, JWTError
from sqlalchemy import func, or_, select, insert, values, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, Query
from apps.deps import get_db, get_redis
from core.redis import CustomRedis
from core.settings import settings
from core.exceptions import UserNotExist, AccessTokenFail
from common.response import ErrCode, response_ok, response_err
from common.security import set_password, verify_password, create_access_token
from utils.logger import logger
from apps.base.model import BaseUser
from apps.base.views_admin import get_current_active_user
from .model import Category, Post, Comment
from .schemas import PostInsert

router_blog_admin = APIRouter()


@router_blog_admin.get('/category/list/', summary='文章分类列表')
async def category_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    redis: CustomRedis = Depends(get_redis),
    current_user: BaseUser = Depends(get_current_active_user)
):
    """文章分类列表"""
    objs = await db.scalars(select(Category).filter(Category.status==0))
    return response_ok(data=[obj.to_dict() for obj in objs])


@router_blog_admin.post('/post/insert', summary='新建文章')
async def post_insert(request: Request,
                      args: PostInsert,
                      db: AsyncSession = Depends(get_db),
                      redis: CustomRedis = Depends(get_redis),
                      current_user=Depends(get_current_active_user)):
    """新建文章"""
    obj = Post(title=args.title, body=args.body,
            category_id=args.category_id,
            is_publish=args.is_publish)
    db.add(obj)
    await db.commit()
    return response_ok(data={"id": obj.id})