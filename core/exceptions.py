import traceback
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, ProgrammingError
from common.response import ErrCode, response_err
from common.errors import UserNotExist, AccessTokenFail
from utils.logger import logger


def register_exceptions(app: FastAPI):
    """异常处理"""

    @app.exception_handler(UserNotExist)
    async def user_not_exists(request: Request, exc: UserNotExist):
        return response_err(ErrCode.USER_NOT_EXISTS)

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
        return response_err(ErrCode.COMMON_INTERNAL_ERR, detail=format(exc))

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """数据冲突"""
        logger.critical(traceback.format_exc())
        return response_err(ErrCode.DB_INTEGRITY_ERROR, detail=exc.detail)
