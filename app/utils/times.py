import time
from datetime import datetime, timedelta


def timestamp(fmt=None):
    """时间戳"""
    if fmt is None:
        return round(time.time())
    return round(time.time() * fmt)

def sleep(s=1):
    time.sleep(s)


def dt_strftime(t=datetime.now(), fmt="%Y-%m-%d %H:%M:%S"):
    """格式化当前时间"""
    return t.strftime(fmt)


if __name__=='__main__':
    dt_strftime()