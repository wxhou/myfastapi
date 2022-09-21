from typing import Union, List, Tuple, Dict, Any
from starlette import status
from fastapi.responses import JSONResponse


class ErrCode(object):
    """错误码"""
    USER_NOT_EXISTS = (1000, '用户不存在')
    USER_HAS_EXISTS = (1001, '用户已存在')
    UNAME_OR_PWD_ERROR = (1002, "用户名或密码错误")
    TOKEN_EXPIRED_ERROR = (1003, 'Token过期')
    TOKEN_INVALID_ERROR = (1004, 'Token错误')
    USER_NOT_ACTIVE = (1005, '用户未激活')
    FILE_TYPE_ERROR = (1006, "文件类型错误")
    QUERY_NOT_EXISTS = (1007, "数据不存在")
    QUERY_HAS_EXISTS = (1008, "数据已存在")
    TOO_MANY_REQUEST = (1009, "太多的请求")
    DEVICE_NOT_FOUND = (1010, "设备不存在")
    DEVICE_IS_EXISTS = (1011, "设备已存在")
    NOT_AUTHENTICATED = (1012, "JWT验证失败")
    # params
    REQUEST_PARAMS_ERROR = (2000, "请求参数错误")
    COMMON_INTERNAL_ERR = (2001, '内部错误')
    DB_INTEGRITY_ERROR = (2002, '数据冲突')
    REDIS_CONNECTION_ERROR = (2003, 'redis连接失败')
    DB_CONNECTION_ERROR = (2004, 'DB连接失败')
    COMMON_PERMISSION_ERR = (2005, '无访问权限')


def response_ok(data: Union[List, Dict, None] = None, msg='success', **kwargs) -> Dict:
    """正确返回"""
    ret = {'code': 0, 'errmsg': msg}
    if data is not None:
        ret['data'] = data
    for k, v in kwargs.items():
        if k not in ret:
            ret[k] = v
    return JSONResponse(ret, status_code=status.HTTP_200_OK)


def response_err(errcode, detail=None, status_code=status.HTTP_200_OK):
    """错误返回"""
    ret = {"code": errcode[0], "errmsg": errcode[1]}
    if detail is not None:
        ret['detail'] = detail
    return JSONResponse(ret, status_code=status_code)
