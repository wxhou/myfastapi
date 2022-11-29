from celery import Celery
from app.core.settings import settings

celery = Celery(settings.PROJECT_NAME)
celery.config_from_object("app.core.celeryconfig")
# celery -A  app.core.celery_app.celery worker -l info