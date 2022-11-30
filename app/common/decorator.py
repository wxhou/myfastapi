import asyncio
import inspect
from functools import wraps
from redlock import RedLock, RedLockError
from app.utils.times import sleep


def sync_run_async(func):
    """运行异步函数"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if inspect.iscoroutine(func):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)

    return wrapper


def singe_task(lock_name, connection_details=None, seconds=1):
    """只运行一次任务"""
    def rlock(func):
        if inspect.iscoroutine(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    with RedLock(lock_name, connection_details=connection_details):
                        ret = await func(*args, **kwargs)
                        await asyncio.sleep(seconds)
                        return ret
                except RedLockError:
                    pass
            return wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    with RedLock(lock_name, connection_details=connection_details):
                        ret = func(*args, **kwargs)
                        sleep(seconds)
                        return ret
                except RedLockError:
                    pass
            return wrapper
    return rlock
