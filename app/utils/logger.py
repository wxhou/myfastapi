"""
日志文件配置 参考链接
https://github.com/Delgan/loguru
# 本来是想 像flask那样把日志对象挂载到app对象上，作者建议直接使用全局对象
https://github.com/tiangolo/fastapi/issues/81#issuecomment-473677039
考虑是否应该把logger 改成单例
"""
from loguru import logger

from app.core.settings import settings


# 日志简单配置 文件区分不同级别的日志
logger.add(settings.LOGGER_SERVER_FILE, rotation="500 MB", compression='zip',
           retention="14 days", encoding='utf-8', enqueue=True, level='INFO')
logger.add(settings.LOGGER_ERROR_FILE, rotation="500 MB", compression='zip',
           retention="14 days", encoding='utf-8', enqueue=True, level='ERROR')

# websocket日志
logger.add(settings.WEBSOCKET_LOGGER_FILE, filter=lambda record: record["extra"]["name"]=="websocket")
websocket_logger = logger.bind(name='websocket')