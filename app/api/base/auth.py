from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request, Depends
from app.api.deps import get_db, get_redis
from app.core.redis import MyRedis
from app.core.settings import settings
from app.common.security import verify_password, OAuth2PasswordJWT, decrypt_access_token
from app.common.errors import UserNotExist, UserNotActive, PermissionError, AccessTokenFail, NotAuthenticated
from app.utils.logger import logger
from .model import BaseUser, BasePermission, RolePermission
from .schemas import TokenData



oauth2_scheme = OAuth2PasswordJWT(tokenUrl="/login/",
                                  scheme_name='JWT')

async def get_current_user(db: AsyncSession = Depends(get_db),
                           redis: MyRedis = Depends(get_redis),
                           token: str = Depends(oauth2_scheme)):
    """获取当前登录用户"""
    is_token_alive = await redis.exists("weblog_access_token_{}".format(token))
    if not is_token_alive:
        raise NotAuthenticated
    username = await decrypt_access_token(token)
    token_data = TokenData(username=username)
    obj = await db.scalar(select(BaseUser).where(BaseUser.username == token_data.username,
                                                 BaseUser.status == 0))
    if obj is None:
        raise UserNotExist
    return obj


async def get_current_active_user(current_user: BaseUser = Depends(get_current_user)):
    """
    获取激活用户
    """
    if not current_user.is_active:
        raise UserNotActive
    return current_user


async def authenticate(db: AsyncSession, username: str, password: str):
    """ 验证用户 """
    sql = select(BaseUser).where(BaseUser.username == username,
                                 BaseUser.status == 0)
    user = (await db.execute(sql)).scalar_one_or_none()
    if user and verify_password(password, user.password_hash):
        return user
    return False


def check_user_permission(permission_name: str):
    """权限检查依赖"""
    async def has_permission(request: Request,
                             db: AsyncSession = Depends(get_db),
                             current_user: BaseUser = Depends(get_current_active_user)):
        if settings.DEBUG:
            return current_user
        if current_user.role_id is None:
            raise PermissionError
        perm_id = await db.scalar(select(BasePermission.id).filter(BasePermission.function_name==permission_name,
                                                            BasePermission.status==0))
        if perm_id is None:
            raise PermissionError
        sql = select(RolePermission.id).filter(RolePermission.role_id==current_user.role_id,
                                      RolePermission.permission_id==perm_id)
        res = await db.scalar(sql)
        if res is None:
            raise PermissionError
        return current_user
    return has_permission
