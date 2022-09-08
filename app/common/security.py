from typing import Optional, Union, Any
from datetime import datetime, timedelta
from fastapi import Header
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.settings import settings


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
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# https://www.cnblogs.com/CharmCode/p/14191112.html?ivk_sa=1024320u


async def check_jwt_token(token: Optional[str] = Header(...)) -> Union[str, Any]:
    """ 解密token """
    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:  # jwt.JWTError, jwt.ExpiredSignatureError, AttributeError
        raise JWTError(f'token已过期! -- {e}')


if __name__ == '__main__':
    print(verify_password('hoou1993',
          '$2b$12$tw/fMjiLHEVMROj2y9tjVOeDL3O6alHPznyX13sp79cfXDhWkKEaS'))
