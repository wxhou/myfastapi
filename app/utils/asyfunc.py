from asgiref.sync import async_to_sync
from functools import wraps



def sync_run_async(func):
    """运行异步函数"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return async_to_sync(func)(*args, **kwargs)

    return wrapper