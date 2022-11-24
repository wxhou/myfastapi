from redis import Redis, ConnectionPool
from celery import Celery
from app.core.settings import settings

celery = Celery(settings.PROJECT_NAME)
celery.config_from_object("app.core.celeryconfig")
celery.redis = Redis(connection_pool=ConnectionPool.from_url(settings.REDIS_URL), decode_responses=True)
# celery -A  app.core.celery_app.celery worker -l info