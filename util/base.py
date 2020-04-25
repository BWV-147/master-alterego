"""Basic functions or classes, should be independent of others"""
import argparse
import sys
import time
from typing import List, Tuple, Union, Dict, Callable, Sequence, Optional  # noqas


class ArgParser:
    def __init__(self, args: list = None):
        self._parser: Optional[argparse.ArgumentParser] = None
        self._init_parser()
        self.supervise = None
        self.config = None
        self.parse(args)

    def parse(self, args):
        # args without filename
        resolved_args = self._parser.parse_known_intermixed_args(args)[0]
        self.supervise = not resolved_args.disable_supervisor
        self.config = resolved_args.config

    @property
    def parser(self):
        return self._parser

    def _init_parser(self):
        if self._parser is not None:
            return
        self._parser = argparse.ArgumentParser(conflict_handler='resolve')
        self._parser.add_argument('-c', '--config', default='data/config.json',
                                  help='config file path, default "data/config.json".')
        self._parser.add_argument('-d', '--disable-supervisor', action='store_true',
                                  help='disable supervisor, default enabled.')


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


class Timer:
    def __init__(self):
        self.t0 = time.time()

    def lapse(self, save=True):
        t1 = time.time()
        dt = t1 - self.t0
        if save:
            self.t0 = t1
        return dt
