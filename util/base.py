"""Basic functions or classes, should be independent of others"""
import argparse
import sys
import threading
import time
from typing import List, Tuple, Union, Dict, Callable, Sequence, Optional  # noqas

_BUNDLE_ID_CN = 'com.bilibili.fatego'
_BUNDLE_ID_JP = 'com.aniplex.fategrandorder'


class ArgParser:
    def __init__(self, args: list = None):
        self._parser: Optional[argparse.ArgumentParser] = None
        self._init_parser()
        self.task = None
        self.supervise = None
        self.config = None
        self.parse(args)

    def parse(self, args):
        # args without filename
        resolved_args = self._parser.parse_known_intermixed_args(args)[0]
        print(resolved_args)
        if resolved_args.gen_config:
            import os
            from util.config import config
            fp = 'data/config.json'
            if os.path.exists(fp):
                print(f'config file is already at {fp}')
            else:
                config.save(fp)
                print(f'default config file saved at {fp}')
            exit(0)
        self.task = resolved_args.task
        self.supervise = not resolved_args.disable_supervisor
        self.config = resolved_args.config

    @property
    def parser(self):
        return self._parser

    def _init_parser(self):
        if self._parser is not None:
            return
        _parser = argparse.ArgumentParser(conflict_handler='resolve')
        _parser.add_argument('task', nargs='?', default='battle', choices=['battle', 'lottery', 'fp', 'server'],
                             help='specific a task')
        _parser.add_argument('-c', '--config', default='data/config.json',
                             help='config file path or {} part of data/config-{}.json, default "data/config.json".')
        _parser.add_argument('-d', '--disable-supervisor', action='store_true',
                             help='disable supervisor, default enabled.')
        _parser.add_argument('--gen-config', action='store_true', help='generate default config file.')
        self._parser = _parser


def convert_to_list(items):
    if items is None:
        return []
    elif isinstance(items, Sequence):
        return list(items)
    else:
        return [items]


def get_center_coord(xy: Sequence):
    if 2 == len(xy):
        return xy
    elif 4 == len(xy):
        return (xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2
    else:
        raise ValueError(f'xy=${xy}: len(xy) should be 2 or 4.')


def is_interactive_mode():
    if sys.__dict__.get('ps1') or sys.argv[0].endswith('pydevconsole.py'):
        # interactive interpreter: 1-python default, 2-pycharm interactive console,
        return True
    return False


def catch_exception(func):
    """Catch exception then print error and traceback to logger.

    Decorator can be applied to multi-threading but multi-processing
    """
    from .log import logger

    def catch_exception_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            raise
        except:  # noqas
            s = f'=== Error in {threading.current_thread()}, {func} ===\n'
            if args:
                s += f'args={str(args):.200s}\n'
            if kwargs:
                s += f'kwargs={str(kwargs):.200s}\n'
            logger.error(s, exc_info=sys.exc_info())

    return catch_exception_wrapper


def datetime_str():
    return time.strftime("%m%d-%H%M")


class Timer:
    def __init__(self):
        self.t0 = time.time()

    def lapse(self, save=True):
        t1 = time.time()
        dt = t1 - self.t0
        if save:
            self.t0 = t1
        return dt
