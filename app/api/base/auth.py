from typing import Optional, Dict
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security import OAuth2, SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from fastapi import Request, Depends, Security
from app.api.deps import get_db, get_redis
from app.core.redis import MyRedis
from app.core.settings import settings
from app.common.security import verify_password
from app.common.errors import UserNotExist, UserNotActive, PermissionError, AccessTokenFail, NotAuthenticated
from app.utils.logger import logger
from .model import BaseUser, BaseRole, BasePermission, RolePermission
from .schemas import TokenData


class OAuth2PasswordJWT(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "jwt":
            if self.auto_error:
                raise NotAuthenticated
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordJWT(tokenUrl="/login/",
                                  scheme_name='JWT')

async def get_current_user(db: AsyncSession = Depends(get_db),
                           redis: MyRedis = Depends(get_redis),
                           token: str = Depends(oauth2_scheme)):
    """获取当前登录用户"""
    is_token = await redis.get("weblog_access_token_{}".format(token))
    if is_token is None:
        raise NotAuthenticated
    payload = jwt.decode(is_token, settings.JWT_SECRET_KEY,
                            algorithms=[settings.ALGORITHM])
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise AccessTokenFail
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
