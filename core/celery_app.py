from celery import Celery
from core.settings import settings

celery = Celery('weblog',
                broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULT_BACKEND)
