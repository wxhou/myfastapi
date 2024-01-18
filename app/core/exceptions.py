import traceback
from jose import JWTError
from fastapi import FastAPI, Request

from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import IntegrityError, ProgrammingError, OperationalError
from aioredis.exceptions import ConnectionError
from app.common.response import ErrCode, response_err
from app.common.error import UserNotExist, UserNotActive, PermissionError, DeviceNotFound, TokenExpiredError
from app.extensions import limiter
from app.utils.logger import logger


def register_exceptions(app: FastAPI):
    """异常处理"""
    @app.exception_handler(RateLimitExceeded)
    async def many_request(request: Request, exc: RateLimitExceeded):
        """请求过多处理"""
        logger.error(request.url)
        response = response_err(ErrCode.TOO_MANY_REQUEST, detail=f"Rate limit exceeded: {exc.detail}")
        response = limiter._inject_headers(
            response, request.state.view_rate_limit
        )
        return response

    @app.exception_handler(TokenExpiredError)
    async def token_expired(request: Request, exc: TokenExpiredError):
        """token过期"""
        return response_err(ErrCode.TOKEN_EXPIRED_ERROR)

    @app.exception_handler(JWTError)
    async def token_error(request: Request, exc: JWTError):
        """token错误"""
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.TOKEN_INVALID_ERROR)

    @app.exception_handler(UserNotExist)
    async def user_not_exists(request: Request, exc: UserNotExist):
        return response_err(ErrCode.USER_NOT_EXISTS)

    @app.exception_handler(UserNotActive)
    async def user_not_active(request: Request, exc: UserNotActive):
        return response_err(ErrCode.USER_NOT_ACTIVE)

    @app.exception_handler(DeviceNotFound)
    async def device_not_found(request: Request, exc: DeviceNotFound):
        return response_err(ErrCode.DEVICE_NOT_FOUND)

    @app.exception_handler(RequestValidationError)
    async def validation_request_handler(request: Request, exc: RequestValidationError):
        """请求参数错误"""
        logger.debug(request.url)
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.REQUEST_PARAMS_ERROR, detail=exc.errors())

    @app.exception_handler(Exception)
    async def internal_err_handler(request: Request, exc: Exception):
        """内部错误"""
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.COMMON_INTERNAL_ERR, detail=str(exc))

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """数据冲突"""
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.DB_INTEGRITY_ERROR, detail=exc.detail)

    @app.exception_handler(PermissionError)
    async def permission_error_handler(request: Request, exc: PermissionError):
        """无访问权限"""
        return response_err(ErrCode.COMMON_PERMISSION_ERR)