from sqlalchemy import select
from fastapi import Depends, Security
from fastapi.security import SecurityScopes
from app.settings import settings
from app.core.oauth2 import CustomOAuth2PasswordBearer
from app.extensions import get_db, get_redis, AsyncSession, aioredis
from app.common.security import verify_password, decrypt_access_token
from app.common.error import UserNotExist, UserNotActive, PermissionError, TokenExpiredError
from app.utils.logger import logger
from app.api.user.model import BaseUser, BasePermission, BaseRolePermission
from .schemas import TokenData



oauth2_scheme = CustomOAuth2PasswordBearer(
    tokenUrl=settings.SWAGGER_LOGIN,
    scheme_name=settings.JWT_TOKEN_TYPE
)


async def get_current_user(db: AsyncSession = Depends(get_db),
                           redis: aioredis.Redis = Depends(get_redis),
                           token: str = Depends(oauth2_scheme)):
    """获取当前登录用户"""
    is_token_alive = await redis.exists("weblog_access_token_{}".format(token))
    if not is_token_alive:
        raise TokenExpiredError
    username, uid = decrypt_access_token(token)
    token_data = TokenData(username=username)
    obj = await db.scalar(select(BaseUser).where(BaseUser.id==uid,
                                                 BaseUser.username == token_data.username,
                                                 BaseUser.status == 0))
    if obj is None:
        raise UserNotExist
    return obj

async def get_current_active_user(
    security_scopes: SecurityScopes,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
    current_user: BaseUser = Depends(get_current_user)):
    """
    获取激活用户
    """
    if not current_user.is_active:
        raise UserNotActive
    scopes = security_scopes.scopes
    if not scopes:
        return current_user
    if current_user.username == 'wxhou':
        return current_user
    if current_user.role_id is None:
        raise PermissionError
    perm_ids = await db.scalars(select(BasePermission.id).filter(
        BasePermission.function_name.in_(scopes), BasePermission.status==0))
    if perm_ids is None:
        raise PermissionError
    sql = select(BaseRolePermission.id).filter(BaseRolePermission.role_id==current_user.role_id,
                                    BaseRolePermission.permission_id.in_(perm_ids))
    res = await db.scalar(sql)
    if res is None:
        raise PermissionError
    return current_user


async def authenticate(db: AsyncSession, username: str, password: str):
    """ 验证用户 """
    sql = select(BaseUser).where(BaseUser.username == username,
                                 BaseUser.status == 0)
    user = (await db.execute(sql)).scalar_one_or_none()
    if user and verify_password(password, user.password_hash):
        return user
    return False