from __future__ import absolute_import, unicode_literals

from functools import cached_property
from typing import Callable
from celery import Celery
from redbeat import RedBeatSchedulerEntry
from app.core import celery_conf
from app.settings import settings


celery = Celery(settings.PROJECT_NAME)
celery.config_from_object(celery_conf)

# shell
# celery -A  app.core.celery_app.celery worker -l info | debug

# beat
# celery -A app.core.celery_app.celery beat -S redbeat.RedBeatScheduler -l info | debug

# clear all tasks
# celery -A app.core.celery_app.celery purge


class RedisSchedulerEntry(object):
    """_summary_

    Args:
        object (_type_): _description_
    """

    def __init__(self, name, app=None) -> None:
        self.name = name
        self.app: Celery = app or celery

    @property
    def _entry(self):
        key_name = self.app.redbeat_conf.key_prefix + self.name
        entry = RedBeatSchedulerEntry.from_key(key_name, app=self.app)
        return entry

    @property
    def key(self):
        return self.app.redbeat_conf.key_prefix + self.name

    @property
    def next_run_time(self):
        """下次运行时间

        Returns:
            _type_: _description_
        """
        return self._entry.due_at

    def __str__(self) -> str:
        return self.name

    def __bool__(self):
        return bool(self._entry)


    def save(self, task: Callable, schedule, args=None, kwargs=None, enabled=True, **clsargs):
        """新建

        Args:
            task (Callable): _description_
            schedule (_type_): _description_
            args (_type_): _description_
            kwargs (_type_): _description_
            enabled (bool, optional): _description_. Defaults to True.
        """
        entry = RedBeatSchedulerEntry(name=self.name,
                                      task=task,
                                      schedule=schedule,
                                      args=args,
                                      kwargs=kwargs,
                                      enabled=enabled,
                                      app=self.app,
                                      **clsargs)
        entry.save()


    def update(self, schedule=None, args=None, kwargs=None, enabled=True):
        """更新
        """
        _entry = self._entry
        _entry.args = args
        _entry.kwargs = kwargs
        _entry.enabled = enabled
        _entry.schedule = schedule
        _entry.save()
        return _entry

    def delete(self):
        """删除
        """
        _entry = self._entry
        celery.log.info()
        _entry.delete()