# noinspection PyUnresolvedReferences
from typing import List, Tuple, Union, Dict, Callable, Sequence

from util.my_logger import *


def convert_to_list(items):
    if items is None:
        return []
    elif isinstance(items, Sequence):
        return list(items)
    else:
        return [items]


def terminate_cur_child_thread():
    if threading.current_thread().name != 'MainThread':
        BaseConfig.task_finished = True
        # how to stop?


class Timer:
    t1 = 0
    t2 = 0
    dt = 0

    def __init__(self):
        self.t1 = time.time()

    def lapse(self, save=True):
        dt = time.time() - self.t1
        if save:
            self.t1 = time.time()
        return dt

    def stop(self):
        self.t2 = time.time()
        self.dt = self.t2 - self.t1
        # print('Time lapse: %f sec' % (self.t2 - self.t1))
        return self
