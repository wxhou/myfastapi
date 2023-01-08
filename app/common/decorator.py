import asyncio
from functools import wraps
from app.utils.times import sleep
from asgiref.sync import sync_to_async, async_to_sync # NO DEL
from app.extensions.redis import redis_redlock, RedLockError


def sync_run_async(func):
    """同步中运行异步函数
    : celery
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            loop = asyncio.get_event_loop()
            task = loop.create_task(func(*args, **kwargs))
            loop.run_until_complete(task)
            return task.result()
            # return async_to_sync(func)(*args, **kwargs) # QA Fail
        else:
            return func(*args, **kwargs)

    return wrapper


def singe_task(lock_name: str, seconds: int=0.5):
    """只运行一次任务"""
    def rlock(func):
        if asyncio.iscoroutinefunction(func):
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
