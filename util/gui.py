import pyautogui

from .base import *
from .config import config


# %% mouse events
# Attention: outside of this module, pyautogui.dragRel and moveRel is allowed.
# Otherwise, apply_offset() before action

def apply_offset(xy: Sequence, offset: Sequence = None):
    """
    :param xy: list length = 2*n
    :param offset: (dx, dy)
    :return:
    """
    offset = offset or config.offset or (0, 0)
    return [p + offset[i % 2] for i, p in enumerate(xy)]


def apply_wda_scale(xy, scale):
    if isinstance(xy, (list, tuple)):
        return [apply_wda_scale(p, scale) for p in xy]
    else:
        # x, y must be integer, if float(0~1 valid), means width or height factor
        return int(xy // scale)


def click(xy: Sequence = None, lapse=0.5):
    """
    click at point (x,y) or region center (x1,y1,x2,y2) within a random offset in radius 0~r

    disable pyautogui.FAILSAFE to ignore FailSafeException/Check
    """
    # in desktop, xy=None means the current pos of mouse,
    # but mobile device cannot remember the last position, so store it in `temp` dict
    # from .log import logger
    # logger.debug(f'click {xy}')
    if xy is None:
        xy = config.temp.get('click_xy', (0, 0))
    else:
        config.temp['click_xy'] = xy
    if config.is_wda:
        assert xy is not None
        x, y = apply_wda_scale(apply_offset(get_center_coord(xy), config.offset), config.wda_client.scale)
        # print(f'click at {(x, y)}')
        config.wda_client.click(x, y)
        pass
    else:
        if xy is not None:
            move_to(xy)
            # print(f'click {tuple(xy)}')
        pyautogui.click()
    time.sleep(lapse)


def move_to(xy: Sequence):
    # only for desktop, or maybe android?
    x, y = apply_offset(get_center_coord(xy), config.offset)
    pyautogui.moveTo(x, y)


def drag(start: Sequence, end: Sequence, duration=1.0, down_time=1.0, up_time=0.0, lapse=0.5):
    """
    :param start: (x1,y1)
    :param end: (x2,y2) both absolute coordinate
    :param duration: duration of mouse moving
    :param down_time: (None, double) time between mouse down and move start. If None, no mouse down event.
    :param up_time: (None, double) time between move end and mouse up. If None, no mouse up event.
    :param lapse: lapse after mouse up
    :return:
    """
    start = apply_offset(get_center_coord(start), config.offset)
    end = apply_offset(get_center_coord(end), config.offset)
    if config.is_wda:
        # yet, wda cannot swipe at a complex path, and only down_time(=duration in .swipe()) can be set
        start = apply_wda_scale(start, config.wda_client.scale)
        end = apply_wda_scale(end, config.wda_client.scale)
        config.wda_client.swipe(*start, *end, duration=down_time)
    else:
        pyautogui.moveTo(start[0], start[1])
        if down_time is not None:
            pyautogui.mouseDown()
            time.sleep(down_time)
        pyautogui.dragRel(end[0] - start[0], end[1] - start[1], duration, mouseDownUp=False)
        if up_time is not None:
            time.sleep(up_time)
            pyautogui.mouseUp()
    time.sleep(lapse)


def sleep(secs: float, secs_wda: float = 0):
    """
    In WDA situation, screenshot take a long time (about 0.3~1 sec), **SHORT** lapse for sleep is not necessary.
    """
    time.sleep(secs_wda if config.is_wda else secs)
