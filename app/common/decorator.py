import sys, asyncio
from functools import wraps
from app.utils.times import sleep
from asgiref.sync import sync_to_async, async_to_sync # NO DEL
from app.extensions.redis import redis


def sync_run_async(func):
    """同步中运行异步函数
    : celery
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            if sys.platform == 'win32':
                return async_to_sync(func)(*args, **kwargs) # QA Fail
            loop = asyncio.get_event_loop()
            task = loop.create_task(func(*args, **kwargs))
            loop.run_until_complete(task)
            return task.result()
        else:
            return func(*args, **kwargs)

    return wrapper


def singe_task(lock_name: str, seconds: int=60*60):
    """只运行一次任务"""
    def rlock(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                with redis.lock(lock_name, blocking_timeout=seconds):
                    ret = await func(*args, **kwargs)
                    return ret
            return wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                with redis.lock(lock_name, blocking_timeout=seconds):
                    return func(*args, **kwargs)
            return wrapper
    return rlock
