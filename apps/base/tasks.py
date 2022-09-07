from celery import shared_task
from utils.fastmail import send_fast_mail


def send_register_email(register_url, email):
    """发送注册邮件"""
    send_fast_mail([email], content="账户激活地址: {}".format(register_url))


@shared_task()
def hello_world():
    return "hello world"
