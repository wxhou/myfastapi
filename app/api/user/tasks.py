from app.core.celery_app import celery
from app.utils.fastmail import send_fast_mail


@celery.task
def send_register_email_task(register_url, email):
    """发送注册邮件"""
    send_fast_mail([email], content="账户激活地址: {}".format(register_url))
