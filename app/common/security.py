from typing import Optional, Union, Any
from datetime import datetime, timedelta
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



async def decrypt_refresh_token(token: str)-> Union[str, Any]:
    """ 解密token """
    payload = jwt.decode(token=token, key=settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise JWTError
    return username


if __name__ == '__main__':
    print(verify_password('hoou1993',
          '$2b$12$tw/fMjiLHEVMROj2y9tjVOeDL3O6alHPznyX13sp79cfXDhWkKEaS'))
