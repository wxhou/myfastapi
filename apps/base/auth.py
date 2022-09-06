from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from fastapi import Request, Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from apps.deps import get_db, get_redis
from core.redis import CustomRedis
from core.settings import settings
from common.security import verify_password
from common.errors import UserNotExist, UserNotActive, PermissionError, AccessTokenFail
from .model import BaseUser, BaseRole, BasePermission, RolePermission
from .schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/base/admin/user/login/", scopes=settings.PERMISSION_DATA)


async def get_current_user(security_scopes: SecurityScopes,
                           db: AsyncSession = Depends(get_db),
                           redis: CustomRedis = Depends(get_redis),
                           token: str = Depends(oauth2_scheme)):
    """获取当前登录用户"""
    try:
        is_token = await redis.get("weblog_{}".format(token))
        if is_token is None:
            raise AccessTokenFail
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AccessTokenFail
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(username=username, scopes=token_scopes)
        if not any(scope in token_data.scopes for scope in security_scopes.scopes):
            raise PermissionError
    except JWTError:
        raise AccessTokenFail
    obj = await db.scalar(select(BaseUser).where(BaseUser.username == token_data.username))
    if obj is None:
        raise UserNotExist
    return obj


async def get_current_active_user(current_user: BaseUser = Security(get_current_user, scopes=['user'])):
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


# def check_user_permission(permission_name: str):
#     """权限检查依赖"""

#     async def has_permission(request: Request,
#                              db: AsyncSession = Depends(get_db),
#                              current_user: BaseUser = Depends(get_current_active_user)):
#         if current_user.role_id is None:
#             raise PermissionError
#         perm_id = await db.scalar(select(BasePermission.id).filter(BasePermission.function_name==permission_name,
#                                                             BasePermission.status==0))
#         if perm_id is None:
#             raise PermissionError
#         sql = select(RolePermission.id).filter(RolePermission.role_id==current_user.role_id,
#                                       RolePermission.permission_id==perm_id)
#         res = await db.scalar(sql)
#         if res is None:
#             raise PermissionError
#         return current_user
#     return has_permission