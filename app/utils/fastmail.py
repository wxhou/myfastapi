from typing import Optional, Union, List
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from app.core.settings import settings
from app.utils.logger import logger


def _format_addr(s) -> str:
    """格式化邮件地址"""
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_fast_mail(to_addr: Union[str, List], content: Optional[str] = None, html_message: Optional[str] = None):
    """发送最新的测试报告"""
    # https://www.liaoxuefeng.com/wiki/1016959663602400/1017790702398272
    # email地址和口令：
    user = settings.MAIL_USERNAME
    pwd = settings.MAIL_PASSWORD
    # 收件人地址
    # SMTP服务器地址
    smtp_server = settings.MAIL_SERVER
    smtp_port = settings.MAIL_PORT
    try:
        # 初始化邮件对象
        if html_message:
            msg = MIMEText(content, 'html', 'utf-8')
        else:
            msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr("Weblog <%s>" % user)
        msg['To'] = _format_addr('ADMIN <%s>' % ','.join(to_addr))
        msg['Subject'] = Header("注册激活邮件", 'utf-8').encode()

        # 发件人邮箱中的SMTP服务器，端口
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # 括号中对应的是发件人邮箱账号、邮箱密码
            server.login(user, pwd)
            # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.sendmail(user, to_addr, msg.as_string())
        logger.debug("邮件发送成功！")
    except smtplib.SMTPException as e:
        logger.error(u"Error: 无法发送邮件", format(e))


if __name__ == '__main__':
    send_fast_mail()