"""Basic functions or classes, should be independent of others"""
import argparse
import ctypes
import sys
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
        _parser.add_argument('task', nargs='?', default='battle', choices=['battle', 'lottery', 'fp'],
                             help='specific a task')
        _parser.add_argument('-c', '--config', default='data/config.json',
                             help='config file path or {} part of data/config-{}.json, default "data/config.json".')
        _parser.add_argument('-d', '--disable-supervisor', action='store_true',
                             help='disable supervisor, default enabled.')
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


def check_sys_setting(admin=True, wda=False):
    if sys.platform == 'win32':
        # Android/iOS emulator in Windows
        # check admin permission & set process dpi awareness
        # please run cmd/powershell or Pycharm as administrator.
        from init import initial
        initial()
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            if admin:
                print('Please run cmd/Pycharm as admin to click inside programs with admin permission(e.g. MuMu).')
                # To run a new process as admin, no effect in Pycharm's Python Console mode.
                # print('applying admin permission in a new process, and no effect when in console mode.')
                # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                raise PermissionError('Please run as administrator!')
            else:
                print('Running without admin permission.\n'
                      'Operations (e.g. click) within admin programs will take no effects!')
        else:
            # print('already admin')
            pass
    elif wda is True:
        # WDA+iOS real device, check in config.init_wda()
        pass
    elif sys.platform == 'darwin':
        # Android emulator in macOS
        print('Allow the app(PyCharm/Terminal/...) to control your computer '
              'in "System Preferences/Security & Privacy/Accessibility",\n'
              'or mouse events will take no effects!', file=sys.stderr)
        pass
    else:
        raise EnvironmentError(f'Unsupported system: {sys.platform}. please run in windows/macOS.')


class Timer:
    def __init__(self):
        self.t0 = time.time()

    def lapse(self, save=True):
        t1 = time.time()
        dt = t1 - self.t0
        if save:
            self.t0 = t1
        return dt
