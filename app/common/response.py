from typing import Union, List, Dict, Tuple
from starlette import status
from fastapi.responses import ORJSONResponse


class ErrCode(object):
    """错误码"""
    USER_NOT_EXISTS = (1000, '用户不存在')
    USER_HAS_EXISTS = (1001, '用户已存在')
    UNAME_OR_PWD_ERROR = (1002, "用户名或密码错误")
    TOKEN_EXPIRED_ERROR = (1003, 'Token过期')
    TOKEN_INVALID_ERROR = (1004, 'Token错误')
    USER_NOT_ACTIVE = (1005, '用户未激活')
    FILE_TYPE_ERROR = (1006, "文件类型错误")
    FILE_MD5_ERROR = (1006, "文件校验失败")
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
    # goods
    GOODS_NOT_FOUND = (3000, '商品走丢了')
    GOODS_NUM_NOT_ENOUGH = (3001, '库存不够了')
    GOODS_SELL_OUT = (3002, '商品售罄了')
    ORDER_NOT_FOUND = (3003, '订单不存在')


def response_ok(data: Union[List, Dict, None] = None, msg: str = 'success', status_code=status.HTTP_200_OK,  **kwargs) -> ORJSONResponse:
    """正确返回"""
    ret = {'errcode': 0, 'errmsg': msg}
    if data is not None:
        ret['data'] = data
    ret.update({k:v for k, v in kwargs.items() if k not in ret})
    return ORJSONResponse(ret, status_code=status_code)


def response_err(errcode: Tuple[int, str], detail: Union[List, Dict, None]=None, status_code=status.HTTP_200_OK) -> ORJSONResponse:
    """错误返回"""
    ret = {"errcode": errcode[0], "errmsg": errcode[1]}
    if detail is not None:
        ret['detail'] = detail
    return ORJSONResponse(ret, status_code=status_code)
