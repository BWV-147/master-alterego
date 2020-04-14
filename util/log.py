import logging
import os
import time
from logging.handlers import RotatingFileHandler

from util.config import config

LOG_TIME = {'log_time': True}


class LogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        config.temp['record'] = record
        if getattr(record, 'log_time', False) is True:
            config.log_time = time.time()
        return True


def get_logger(name='log', level=logging.INFO, save=True):
    # noinspection PyUnresolvedReferences
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    # creat a new logger
    log_dir = 'logs/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    _logger.addFilter(LogFilter())

    formatter = logging.Formatter(
        style='{',
        datefmt="%m-%d %H:%M:%S",
        fmt='{asctime} - {filename:<11.11s}[line:{lineno:>3d}] - {levelname:<5s}: [{threadName}] {message}')

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)
    _logger.addHandler(console)

    if save:
        fh = RotatingFileHandler(os.path.join(log_dir, f'{name}.log'),
                                 encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
        fh.setFormatter(formatter)
        fh.setLevel(level)
        _logger.addHandler(fh)

        if level > logging.DEBUG:
            full_fh = RotatingFileHandler(os.path.join(log_dir, f'{name}.full.log'),
                                          encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
            full_fh.setFormatter(formatter)
            full_fh.setLevel(logging.DEBUG)
            _logger.addHandler(full_fh)
    return _logger


logger = get_logger()
