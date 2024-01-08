from typing import Callable
import sys, asyncio
from functools import wraps
from app.utils.times import sleep
from app.extensions.cache import redis_client


def sync_run_async(func: Callable):
    """同步中运行异步函数
    : celery
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            return func(*args, **kwargs)
        # if sys.platform == 'win32':
            # return async_to_sync(func)(*args, **kwargs) # QA Fail
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            task = loop.create_task(func(*args, **kwargs))
            loop.run_until_complete(task)
            return task.result()
    return wrapper


class Singleton(type):
    """一个单例
    # https://zhuanlan.zhihu.com/p/37534850
    """

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instances"):
            cls._instances = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances



def singe_task(lock_name: str, seconds: int=60*60):
    """只运行一次任务
    APScheduler专用函数
    """
    def rlock(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                with redis_client.lock(lock_name, blocking_timeout=seconds):
                    ret = await func(*args, **kwargs)
                    return ret
            return wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                with redis_client.lock(lock_name, blocking_timeout=seconds):
                    return func(*args, **kwargs)
            return wrapper
    return rlock
