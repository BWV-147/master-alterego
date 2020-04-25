"""Log module"""
__all__ = ['LOG_TIME', 'LOG_FORMATTER', 'LoggerDispatcher', 'DispatcherFilter', 'logger']

import logging
import os
from logging.handlers import RotatingFileHandler

from .base import *
from .config import config

LOG_TIME = {'log_time': True}
LOG_FORMATTER = logging.Formatter(
    style='{',
    datefmt="%m-%d %H:%M:%S",
    fmt='{asctime} - {filename:<11.11s}[line:{lineno:>3d}] - {levelname:<5s}: [{threadName}] {message}')


class DispatcherFilter(logging.Filter):
    def __init__(self, dispatch_handler=None):
        super().__init__()
        self.logger = None
        self.dispatch_handler = dispatch_handler

    def filter(self, record: logging.LogRecord):
        """
        Filter jobs are forwarded to LoggerDispatcher.dispatch_record to decide dispatch or not.
        Update config.log_time if needed.
        """
        config.temp['record'] = record
        if getattr(record, 'log_time', False) is True:
            # key-value in `extra` are converted to record's attributes
            config.log_time = time.time()
        if self.dispatch_handler is None:
            return True
        else:
            return self.dispatch_handler(record)


class LoggerDispatcher(logging.Logger):
    """
    Dispatch(forward) every log record to `_logger`.

    _logger: Almost all project related logs are recorded through this logger except server module(flask).
    If _logger is set to None, this LoggerDispatcher will print log to stderr.

    dispatcher_disabled: if disabled, will not forward log to _logger but handle it by self.

    Singleton pattern.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerDispatcher, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__('dispatcher')
        # properties
        self._logger: Optional[logging.Logger] = None
        self.dispatcher_disabled = False
        self._log_filepath = None
        self.dispatcher_filter = DispatcherFilter(self.dispatch_record)
        # init
        self.addFilter(self.dispatcher_filter)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        self.addHandler(console)  # default console handler if cur_logger is not None

    def dispatch_record(self, record: logging.LogRecord):
        """
        Dispatch caught log record by self.filter to _logger if not disabled.
        :return: return False to forward, return True to handle by itself.
        """
        if self.dispatcher_disabled:
            return True
        if self._logger is None:
            # create default _logger
            self.set_cur_logger()
        self._logger.handle(record)
        return False

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

            console = logging.StreamHandler()
            console.setFormatter(LOG_FORMATTER)
            console.setLevel(logging.DEBUG)
            _logger.addHandler(console)

            if save_path is not None:
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                fp = os.path.join(save_path, f'{name}.log')
                fh = RotatingFileHandler(fp, encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
                fh.setFormatter(LOG_FORMATTER)
                fh.setLevel(level)
                _logger.addHandler(fh)
                self._log_filepath = fp

                if level > logging.DEBUG:
                    fp = os.path.join(save_path, f'{name}.full.log')
                    full_fh = RotatingFileHandler(fp, encoding='utf8', maxBytes=1024 * 1024, backupCount=3)
                    full_fh.setFormatter(LOG_FORMATTER)
                    full_fh.setLevel(logging.DEBUG)
                    _logger.addHandler(full_fh)
                    # only store the path of full_log if exist
                    self._log_filepath = fp
        self._logger = _logger

    def get_cur_logger(self):
        return self._logger

    @property
    def log_filepath(self):
        if self.dispatcher_disabled:
            return None
        return self._log_filepath


logger = LoggerDispatcher()
