from .settings import settings
# https://docs.celeryq.dev/en/stable/
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
security_key = ''
broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND
result_serializer = "json"
accept_content = ['json']
timezone = "Asia/Shanghai"
result_expires = 60 * 60 * 24
worker_max_tasks_per_child = 8
imports = (
    'app.api.blog.tasks',
) # 导入任务
worker_log_format= "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"