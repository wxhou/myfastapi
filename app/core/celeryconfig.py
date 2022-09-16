from kombu import Queue, Exchange
from .settings import settings
# https://docs.celeryq.dev/en/stable/
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
security_key = settings.CELERY_SECURITY_KEY
broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND
result_serializer = "json"
accept_content = ['json']
timezone = "Asia/Shanghai"
result_expires = 60 * 60 * 24 # 任务过期时间
worker_max_tasks_per_child = 8 # 池工作进程在被新进程替换之前可以执行的最大任务数。默认为无限制。
imports = (
    'app.api.blog.tasks',
) # 导入任务
worker_log_format= "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
task_queues = (
    Queue('celery', routing_key='celery'),
    Queue('transient', Exchange('transient', delivery_mode=1), # delivery_mode=1不会写入磁盘
          routing_key='transient', durable=False), # task.apply_async((2,3), queue='transient')
)