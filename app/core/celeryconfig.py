from celery.schedules import crontab, schedule
from typing import List, Tuple
from kombu import Queue, Exchange
from .settings import settings
# https://docs.celeryq.dev/en/stable/
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
security_key: str = settings.CELERY_SECURITY_KEY
broker_url: str = settings.CELERY_BROKER_URL
result_backend: str = settings.CELERY_RESULT_BACKEND
redbeat_redis_url: str = settings.CELERY_BROKER_URL
redbeat_key_prefix: str = 'celery:redbeat'
redbeat_lock_timeout: int = 300
beat_max_loop_interval: int = 5
result_serializer: str = "json"
accept_content: List[str] = ['json']
timezone: str = "Asia/Shanghai"
result_expires: int = 60 * 60 * 24 # 任务过期时间
worker_max_tasks_per_child: int = 8 # 池工作进程在被新进程替换之前可以执行的最大任务数。默认为无限制。
worker_max_memory_per_child = 100 * 1000  # 100MB
worker_log_format: str = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
broker_transport_options = {
    'visibility_timeout': 6*60*60,
    'max_retries': 3
}
task_queues: Tuple[Queue] = (
    Queue('celery', routing_key='celery'),
    Queue('transient', Exchange('transient', delivery_mode=1), # delivery_mode=1不会写入磁盘
          routing_key='transient', durable=False), # task.apply_async((2,3), queue='transient', ignore_result=True)
)
imports: Tuple[str] = (
    'app.api.tasks',
    'app.api.blog.tasks',
    'app.api.trade.tasks',
    'app.api.goods.tasks',
    'app.api.user.tasks',
) # 导入任务

# 定时任务
beat_schedule = {

    # Executes every Monday morning at 7:30 a.m.

    'add-hello-celery': {

        'task': 'app.api.tasks.hello_celery',

        'schedule': crontab(),

        'args': ('world',),

    },

}