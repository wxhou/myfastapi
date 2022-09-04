import os
import sys
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASEDIR)
import logging
from logging.handlers import RotatingFileHandler
from core.settings import settings


logger = logging.getLogger()
logger.setLevel(settings.LOGGER_LEVEL)

# stream_handler = logging.StreamHandler(stream=None)
file_handler = RotatingFileHandler(filename=settings.LOGGER_FILE,
                                   maxBytes=10 * 1024 * 1024,
                                   backupCount=10,
                                   encoding="utf-8")

# stream_handler.setFormatter(logging.Formatter(settings.LOGGER_FORMATTER))
file_handler.setFormatter(logging.Formatter(settings.LOGGER_FORMATTER))
logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


if __name__ == '__main__':
    logger.debug("测试日志")
