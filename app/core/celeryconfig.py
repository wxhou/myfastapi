from typing import List, Tuple
from kombu import Queue, Exchange
from .settings import settings
# https://docs.celeryq.dev/en/stable/
# https://docs.celeryq.dev/en/stable/userguide/configuration.html
security_key: str = settings.CELERY_SECURITY_KEY
broker_url: str = settings.CELERY_BROKER_URL
result_backend: str = settings.CELERY_RESULT_BACKEND
result_serializer: str = "json"
accept_content: List[str] = ['json']
timezone: str = "Asia/Shanghai"
result_expires: int = 60 * 60 * 24 # 任务过期时间
worker_max_tasks_per_child: int = 8 # 池工作进程在被新进程替换之前可以执行的最大任务数。默认为无限制。
imports: Tuple[str] = (
    'app.api.base.tasks',
    'app.api.blog.tasks',
    'app.api.trade.tasks',
    'app.api.goods.tasks',
) # 导入任务
worker_log_format: str = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
task_queues: Tuple[Queue] = (
    Queue('celery', routing_key='celery'),
    Queue('transient', Exchange('transient', delivery_mode=1), # delivery_mode=1不会写入磁盘
          routing_key='transient', durable=False), # task.apply_async((2,3), queue='transient', ignore_result=True)
)