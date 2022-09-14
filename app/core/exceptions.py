import traceback
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, ProgrammingError, OperationalError
from aioredis.exceptions import ConnectionError
from app.common.response import ErrCode, response_err
from app.common.errors import UserNotExist, UserNotActive, PermissionError, AccessTokenFail
from app.utils.logger import logger


def register_exceptions(app: FastAPI):
    """异常处理"""

    @app.exception_handler(UserNotExist)
    async def user_not_exists(request: Request, exc: UserNotExist):
        return response_err(ErrCode.USER_NOT_EXISTS)

    @app.exception_handler(UserNotActive)
    async def user_not_exists(request: Request, exc: UserNotActive):
        return response_err(ErrCode.USER_NOT_ACTIVE)

    @app.exception_handler(AccessTokenFail)
    async def access_token_error(request: Request, exc: AccessTokenFail):
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.TOKEN_INVALID_ERROR)

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
        return response_err(ErrCode.COMMON_PERMISSION_ERR, detail=exc.detail)


    @app.exception_handler(ConnectionError)
    async def redis_connect_error(request: Request, exc: ConnectionError):
        """Redis链接失败"""
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.REDIS_CONNECTION_ERROR)


    @app.exception_handler(OperationalError)
    async def db_connect_error(request: Request, exc: OperationalError):
        """数据库链接失败"""
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.DB_CONNECTION_ERROR)