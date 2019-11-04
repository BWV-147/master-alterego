import logging
import os
import threading
import time
from logging.handlers import RotatingFileHandler

from util.config import CONFIG

NO_LOG_TIME = 'NO_LOG_TIME'


class LogFilter(logging.Filter):
    def __init__(self, func=None):
        super().__init__()
        assert callable(func)
        self.func = func

    def filter(self, record: logging.LogRecord):
        if NO_LOG_TIME in record.args:
            record.args = [x for x in record.args if x is not NO_LOG_TIME]
        else:
            if threading.current_thread().name != 'MainThread':
                self.func()
        return True


def get_logger(name='log', level=logging.INFO, save=True):
    # noinspection PyUnresolvedReferences
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    # creat a new logger
    log_path = 'logs/'
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)

    def log_func():
        CONFIG.log_time = time.time()

    log_filter = LogFilter(func=log_func)
    _logger.addFilter(log_filter)

    formatter = logging.Formatter(
        style='{',
        datefmt="%m-%d %H:%M:%S",
        fmt='{asctime} - {filename:<10.10s}[line:{lineno:>3d}] - {levelname:<5s}: [{threadName}] {message}')

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)
    _logger.addHandler(console)

    if save:
        fh = RotatingFileHandler(os.path.join(log_path, f'{name}.log'),
                                 encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
        fh.setFormatter(formatter)
        fh.setLevel(level)
        _logger.addHandler(fh)

        if level > logging.DEBUG:
            full_fh = RotatingFileHandler(os.path.join(log_path, f'{name}.full.log'),
                                          encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
            full_fh.setFormatter(formatter)
            full_fh.setLevel(logging.DEBUG)
            _logger.addHandler(full_fh)
    return _logger


logger = get_logger()
