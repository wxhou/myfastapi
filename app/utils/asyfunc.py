import asyncio
from functools import wraps



def sync_run_async(func):
    """运行异步函数"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func(*args, **kwargs))

    return wrapper

