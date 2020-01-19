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


def get_center_coord(xy: Sequence):
    if 2 == len(xy):
        return xy
    elif 4 == len(xy):
        return (xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2
    else:
        raise ValueError(f'xy=${xy}: len(xy) should be 2 or 4.')


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
