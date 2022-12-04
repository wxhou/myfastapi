import asyncio
import inspect
from functools import wraps
from app.utils.times import sleep
from app.extensions.redis import redis_redlock, RedLockError


def sync_run_async(func):
    """运行异步函数"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func(*args, **kwargs))

    return wrapper


def singe_task(lock_name, seconds=0.5):
    """只运行一次任务"""
    def rlock(func):
        if inspect.iscoroutine(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    with redis_redlock.create_lock(lock_name):
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
                    with redis_redlock.create_lock(lock_name):
                        ret = func(*args, **kwargs)
                        sleep(seconds)
                        return ret
                except RedLockError:
                    pass
            return wrapper
    return rlock
