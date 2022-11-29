from typing import Optional, Union, Any, Dict
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security import OAuth2
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.settings import settings
from app.common.error import NotAuthenticated


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # 加密密码


def set_password(password):
    """加密明文密码"""
    return pwd_context.hash(password)


def verify_password(password, password_hash):
    """解密"""
    return pwd_context.verify(password, password_hash)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """生成token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# https://www.cnblogs.com/CharmCode/p/14191112.html?ivk_sa=1024320u
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def decrypt_access_token(token: str)-> Union[str, Any]:
    """ 解密token """
    payload = jwt.decode(token=token, key=settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM)
    username = payload.get("sub")
    uid = payload.get("id")
    if username is None or uid is None:
        raise JWTError
    return username, uid


async def decrypt_refresh_token(token: str)-> Union[str, Any]:
    """ 解密token """
    payload = jwt.decode(token=token, key=settings.JWT_REFRESH_SECRET_KEY, algorithms=settings.ALGORITHM)
    username = payload.get("sub")
    uid = payload.get("id")
    if username is None or uid is None:
        raise JWTError
    return username, uid


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


if __name__ == '__main__':
    print(verify_password('hoou1993',
          '$2b$12$tw/fMjiLHEVMROj2y9tjVOeDL3O6alHPznyX13sp79cfXDhWkKEaS'))
