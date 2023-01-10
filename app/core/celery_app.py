from celery import Celery
from celery.schedules import crontab
from app.core.settings import settings

celery = Celery(settings.PROJECT_NAME)
celery.config_from_object("app.core.celeryconfig")
# celery -A  app.core.celery_app.celery worker -l info
celery.conf.beat_schedule = {

    # Executes every Monday morning at 7:30 a.m.

    'add-every-monday-morning': {

        'task': 'app.core.celery_app.hello_celery',

        'schedule': crontab(),

        'args': ('world',),

    },

}


@celery.task
def hello_celery(name):
    return 'ok'