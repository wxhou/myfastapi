from typing import Optional
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN



class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != self.scheme_name.lower():
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": self.scheme_name},
                )
            else:
                return None
        return param