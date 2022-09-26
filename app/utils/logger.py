import logging
from logging.handlers import RotatingFileHandler
from app.core.settings import settings


logger = logging.getLogger()

# stream_handler = logging.StreamHandler(stream=None)
file_handler = RotatingFileHandler(filename=settings.LOGGER_ALL_FILE,
                                   maxBytes=10 * 1024 * 1024,
                                   backupCount=10,
                                   encoding="utf-8")
file_handler.setLevel(settings.LOGGER_LEVEL)
file_handler.setFormatter(logging.Formatter(settings.LOGGER_FORMATTER))

err_handler = RotatingFileHandler(filename=settings.LOGGER_ERROR_FILE,
                                   maxBytes=10 * 1024 * 1024,
                                   backupCount=10,
                                   encoding="utf-8")
err_handler.setLevel(logging.ERROR)
err_handler.setFormatter(logging.Formatter(settings.LOGGER_FORMATTER))
logger.addHandler(file_handler)
logger.addHandler(err_handler)

# websocket
websocket_logger = logging.getLogger('websocket')
websocket_logger.setLevel(settings.LOGGER_LEVEL)
wf_handler = RotatingFileHandler(filename=settings.WEBSOCKET_LOGGER_FILE,
                                   maxBytes=10 * 1024 * 1024,
                                   backupCount=10,
                                   encoding="utf-8")
wf_handler.setFormatter(logging.Formatter(settings.LOGGER_FORMATTER))
websocket_logger.addHandler(wf_handler)

if __name__ == '__main__':
    logger.debug("测试日志")
