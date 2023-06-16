from celery import Celery
from redbeat.schedulers import RedBeatSchedulerEntry
from app.settings import settings


celery = Celery(settings.PROJECT_NAME)
celery.config_from_object("app.core.celeryconfig")
# celery -A  app.core.celery_app.celery worker -l info


class RedisSchedulerEntry(object):
    def __init__(self, celery) -> None:
        self.app = celery

    async def from_key(self, name):
        key_name = self.app.redbeat_conf.key_prefix + name
        entry = RedBeatSchedulerEntry.from_key(key_name, app=self.app)
        return entry

    async def update(self, key_name, schedule=None, args=None, kwargs=None, enabled=True):
        entry = await self.from_key(key_name)
        entry.args = args
        entry.kwargs = kwargs
        entry.enabled = enabled
        entry.schedule = schedule
        entry.save()
        return entry

    async def next_run_time(self, key_name):
        """获取下次运行时间"""
        entry = await self.from_key(key_name)
        return entry.due_at

    async def save(self, name=None, task=None, schedule=None, args=None, kwargs=None, enabled=True, **clsargs):
        entry = RedBeatSchedulerEntry(name=name, task=task, schedule=schedule, args=args, kwargs=kwargs,
                                      enabled=enabled, app=self.app, **clsargs)
        entry.save()

    async def delete(self, key_name):
        entry = self.from_key(key_name)
        celery.log.info(entry)
        entry.delete()


redis_scheduler_entry = RedisSchedulerEntry(celery)