import logging
import os
import time
from logging.handlers import RotatingFileHandler

from .config import config

LOG_TIME = {'log_time': True}


class DispatcherFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.cur_logger = None

    def filter(self, record: logging.LogRecord):
        config.temp['record'] = record
        if getattr(record, 'log_time', False) is True:
            # key-value in `extra` are converted to record's attributes
            config.log_time = time.time()
        if self.cur_logger is None:
            return True
        else:
            self.cur_logger.handle(record)
            return False


class LoggerDispatcher(logging.Logger):
    """
    Dispatch every log record to cur_logger which saved in `dispatch_filter`.

    Singleton pattern.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerDispatcher, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__('dispatcher')
        self.dispatch_filter = DispatcherFilter()
        self.addFilter(self.dispatch_filter)
        self.addHandler(logging.StreamHandler())  # default console handler if cur_logger is not None
        self.set_cur_logger()

    def set_cur_logger(self, name='log', level=logging.INFO, save_path='logs/'):
        """
        :param name: logger name in logging's loggerDict
        :param level: if level>DEBUG and save_path, logs will be saved to two files, one only for >=INFO, one for all.
        :param save_path: folder path to save log. If set to None, logs will not be saved.
        :return:
        """
        # noinspection PyUnresolvedReferences
        if name in logging.Logger.manager.loggerDict:
            _logger = logging.getLogger(name)
        else:
            _logger = logging.getLogger(name)
            _logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                style='{',
                datefmt="%m-%d %H:%M:%S",
                fmt='{asctime} - {filename:<11.11s}[line:{lineno:>3d}] - {levelname:<5s}: [{threadName}] {message}')

            console = logging.StreamHandler()
            console.setFormatter(formatter)
            console.setLevel(logging.DEBUG)
            _logger.addHandler(console)

            if save_path is not None:
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                fh = RotatingFileHandler(os.path.join(save_path, f'{name}.log'),
                                         encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
                fh.setFormatter(formatter)
                fh.setLevel(level)
                _logger.addHandler(fh)

                if level > logging.DEBUG:
                    full_fh = RotatingFileHandler(os.path.join(save_path, f'{name}.full.log'),
                                                  encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
                    full_fh.setFormatter(formatter)
                    full_fh.setLevel(logging.DEBUG)
                    _logger.addHandler(full_fh)
        self.dispatch_filter.cur_logger = _logger

    def get_cur_logger(self):
        return self.dispatch_filter.cur_logger


logger = LoggerDispatcher()
