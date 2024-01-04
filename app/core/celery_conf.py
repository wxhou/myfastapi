from celery.schedules import crontab, schedule
from typing import List, Tuple, Dict
from kombu import Queue, Exchange
from app.settings import settings
# https://docs.celeryq.dev/en/stable/
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
security_key: str = settings.CELERY_SECURITY_KEY
broker_url: str = settings.CELERY_BROKER_URL
result_backend: str = settings.CELERY_RESULT_BACKEND
redbeat_redis_url: str = settings.CELERY_REDBEAT_REDIS_URL
redbeat_key_prefix: str = 'celery:redbeat'
redbeat_lock_timeout: int = 300
beat_scheduler: str = 'redbeat.RedBeatScheduler'
beat_max_loop_interval: int = 5
broker_connection_retry_on_startup: bool= True
result_serializer: str = "json"
accept_content: List[str] = ['json']
timezone: str = "Asia/Shanghai"
# enable_utc: bool = False
broker_connection_retry_on_startup: bool = True
result_expires: int = 60 * 60 * 24 # 任务过期时间
worker_max_tasks_per_child: int = 10 # 池工作进程在被新进程替换之前可以执行的最大任务数。默认为无限制。
worker_max_memory_per_child: int = 100 * 1000  # 100MB
worker_proc_alive_timeout: float = 30.0 # 等待新工作进程启动时的超时(秒)
worker_log_format: str = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
broker_transport_options: Dict[str, int] = {
    'visibility_timeout': 6*60*60,
    'max_retries': 3
}

task_default_queue: str = 'celery'
task_default_routing_key: str = task_default_queue
task_queues: Tuple[Queue] = (
    Queue(task_default_queue, routing_key=task_default_routing_key),
    Queue('transient', Exchange('transient', delivery_mode=1), # delivery_mode=1不会写入磁盘
          routing_key='transient', durable=False), # task.apply_async((2,3), queue='transient', ignore_result=True)
)
imports: Tuple[str] = (
    'app.api.tasks',
    'app.api.base.tasks',
    'app.api.user.tasks',
    'app.api.blog.tasks',
    'app.api.trade.tasks',
    'app.api.goods.tasks',
) # 导入任务

# 定时任务
beat_schedule: Dict[str, Dict] = {

    # Executes every Monday morning at 7:30 a.m.

    'add-hello-celery': {

        'task': 'app.api.tasks.hello_celery',

        'schedule': crontab(),

        'args': ('world',),

    },
    "delete-old-text2audio": {
        'task': 'app.api.tasks.text2audio_delete_task',
        'schedule': crontab(hour=9, minute=30, day_of_week=1)
    }
}