from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

from app.common.decorator import Singleton
from app.settings import settings
from app.utils.logger import logger

class JobAPScheduler(metaclass=Singleton):
    def __init__(self):
        self._scheduler = AsyncIOScheduler()
        self.load_config()

    def load_config(self):
        jobstores = {'default': SQLAlchemyJobStore(url=settings.SQLALCHEMY_DATABASE_SYNC_URL)}
        executors = {'default': AsyncIOExecutor()}
        job_defaults = {'coalesce': True, 'max_instances': 1}
        self._scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    def start(self):
        logger.warning("启动调度器!!!")
        self._scheduler.start()

    def shutdown(self):
        logger.warning("停止调度器!!!")
        self._scheduler.shutdown()

    @property
    def state(self):
        return self._scheduler.state

    @property
    def schedule(self):
        return self._scheduler

    def get_job(self, job_id, jobstore=None):
        """获取任务"""
        return self._scheduler.get_job(job_id, jobstore)

    def add_job(self, *args, **kwargs):
        """添加任务"""
        return self._scheduler.add_job(*args, **kwargs)

    def remove_job(self, job_id, jobstore=None):
        """移除任务"""
        self._scheduler.remove_job(job_id, jobstore)

    @property
    def task(self):
        """获取调度器的基本装饰器"""
        return self._scheduler.scheduled_job

job_scheduler: JobAPScheduler = JobAPScheduler()

def hello_scheduler():
    logger.warning("你好，调度器")

job_scheduler.add_job(hello_scheduler, 'interval', seconds=10, misfire_grace_time=None, replace_existing=True)
