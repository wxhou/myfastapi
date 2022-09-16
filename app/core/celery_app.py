from celery import Celery
from app.core.settings import settings
from app.core import celeryconfig

celery = Celery(settings.PROJECT_NAME)
celery.config_from_object(celeryconfig)

# celery -A  app.core.celery_app.celery worker -l info