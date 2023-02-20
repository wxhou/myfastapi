from typing import Union, List, Dict, Tuple
from starlette import status
from fastapi.responses import JSONResponse


class ErrCode(object):
    """错误码"""
    # 公共错误
    SYSTEM_ERROR = (1000, '系统错误')
    QUERY_NOT_EXISTS = (1001, "数据不存在")
    QUERY_HAS_EXISTS = (1002, "数据已存在")
    COMMON_INTERNAL_ERR = (1004, '内部错误')
    COMMON_PERMISSION_ERR = (1005, '无访问权限')
    REQUEST_PARAMS_ERROR = (1006, "请求参数错误")
    DB_INTEGRITY_ERROR = (1007, '数据冲突')
    DB_CONNECTION_ERROR = (1008, 'DB连接失败')
    TOO_MANY_REQUEST = (1009, "太多的请求")

    # 登录用户相关
    USER_NOT_EXISTS = (2000, '用户不存在')
    USER_HAS_EXISTS = (2001, '用户已存在')
    USER_NOT_ACTIVE = (2002, '用户未激活')
    UNAME_OR_PWD_ERROR = (2003, "用户名或密码错误")
    TOKEN_INVALID_ERROR = (2004, 'Token错误')
    TOKEN_EXPIRED_ERROR = (2005, 'Token过期')

    # 文件相关
    FILE_TYPE_ERROR = (3000, "文件类型错误")
    FILE_MD5_ERROR = (3001, "文件校验失败")

    # device
    DEVICE_NOT_FOUND = (4000, "设备不存在")
    DEVICE_IS_EXISTS = (4001, "设备已存在")

    # goods
    GOODS_NOT_FOUND = (5000, '商品走丢了')
    GOODS_NUM_NOT_ENOUGH = (5001, '库存不够了')
    GOODS_SELL_OUT = (5002, '商品售罄了')
    ORDER_NOT_FOUND = (5003, '订单不存在')


def response_ok(data: Union[List, Dict, None] = None, msg: str = 'success', status_code=status.HTTP_200_OK,  **kwargs) -> JSONResponse:
    """正确返回"""
    ret = {'errcode': 0, 'errmsg': msg}
    if data is not None:
        ret['data'] = data
    ret.update({k:v for k, v in kwargs.items() if k not in ret})
    return JSONResponse(ret, status_code=status_code)


def response_err(errcode: Tuple[int, str], detail: Union[List, Dict, None]=None, status_code=status.HTTP_200_OK) -> JSONResponse:
    """错误返回"""
    ret = {"errcode": errcode[0], "errmsg": errcode[1]}
    if detail is not None:
        ret['detail'] = detail
    return JSONResponse(ret, status_code=status_code)
