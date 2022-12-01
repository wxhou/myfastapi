import asyncio
import inspect
from functools import wraps
from redlock import RedLock, RedLockError
from app.utils.times import sleep
from app.core.settings import settings

def sync_run_async(func):
    """运行异步函数"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func(*args, **kwargs))

    return wrapper


def singe_task(lock_name, seconds=1):
    """只运行一次任务"""
    def rlock(func):
        if inspect.iscoroutine(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    with RedLock(lock_name, connection_details=settings.REDIS_CONNECTIONS):
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
                    with RedLock(lock_name, connection_details=settings.REDIS_CONNECTIONS):
                        ret = func(*args, **kwargs)
                        sleep(seconds)
                        return ret
                except RedLockError:
                    pass
            return wrapper
    return rlock
