from typing import Optional
import time
from datetime import datetime, timedelta


def timestamp(fmt: Optional[int]=None) -> int:
    """时间戳"""
    if fmt is None:
        return round(time.time())
    return round(time.time() * fmt)

def sleep(s=1):
    time.sleep(s)

def now(utc=False):
    if utc:
        return datetime.utcnow()
    return datetime.now()

def dt_strftime(dt=None, fmt: str="%Y-%m-%d %H:%M:%S"):
    """格式化当前时间"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)


if __name__=='__main__':
    print(dt_strftime())