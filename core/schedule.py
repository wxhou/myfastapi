from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from core.settings import settings

class Singleton(type):
    """_summary_
    # https://zhuanlan.zhihu.com/p/37534850
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class MyScheduler(metaclass=Singleton):
    def __init__(self) -> None:
        self._scheduler = AsyncIOScheduler(
            jobstores={'default': SQLAlchemyJobStore(url=settings.SQLALCHEMY_DATABASE_URL)}
        )

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown()

    @property
    def state(self):
        return self._scheduler.state

    @property
    def schedule(self) -> AsyncIOScheduler:
        return self._scheduler

    def get_job(self, job_id, jobstore=None):
        """获取任务"""
        return self._scheduler.get_job(self, job_id, jobstore)

    def add_job(self, *args, **kwargs):
        """添加任务
        params: func, trigger=None, args=None, kwargs=None, id=None, name=None,
                misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined,
                next_run_time=undefined, jobstore='default', executor='default',
                replace_existing=False, **trigger_args
        """
        self._scheduler.add_job(*args, **kwargs)

    def remove_job(self, job_id, jobstore=None):
        """移除任务"""
        self._scheduler.remove_job(job_id, jobstore)


scheduler = MyScheduler()
