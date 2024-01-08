from fastapi import APIRouter, Depends, Security
from app.common.pagation import PageNumberPagination
from app.common.response import response_ok
from app.extensions import get_db, AsyncSession
from app.api.user.model import BaseUser
from app.api.user.auth import get_current_active_user
from .models import LogLogin, LogOperation



router = APIRouter()





@router.get('/log/login/list', summary='登录日志列表')
async def log_login_list(
    paginate: PageNumberPagination = Depends(),
    current_user: BaseUser = Security(get_current_active_user, scopes=['log_login_list'])
):
    """获取登录日志列表"""
    result_data = await paginate(LogLogin, query_filter=[LogLogin.status==0])
    return response_ok(**result_data)



@router.get('/log/operation/list', summary='操作日志列表')
async def log_operation_list(
    paginate: PageNumberPagination = Depends(),
    current_user: BaseUser = Security(get_current_active_user, scopes=['log_operation_list'])
):
    """获取登录日志列表"""
    result_data = await paginate(LogOperation, query_filter=[LogOperation.status==0])
    return response_ok(**result_data)
