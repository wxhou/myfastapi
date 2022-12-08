from typing import Union
import ulid
from random import randint
from .times import timestamp


def get_ulid(is_str: bool=True) -> Union[ulid.ULID, str]:
    """唯一标识码"""
    ret = ulid.new()
    return ret.str if is_str else ret


def random_str() -> str:
    """随机字符串"""
    return "{}{}".format(timestamp(1000), randint(1000, 9999))