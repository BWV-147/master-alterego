import ctypes
import os
import pprint
import sys

import pyautogui

if 'PYGAME_HIDE_SUPPORT_PROMPT' not in os.environ:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from mss import mss

from .base import *
from .config import config


def check_sys_admin(admin=True):
    if sys.platform == 'win32':
        # check admin permission & set process dpi awareness
        # please run cmd/powershell or Pycharm as administrator.
        # SetProcessDpiAwareness: see
        # https://docs.microsoft.com/zh-cn/windows/win32/api/shellscalingapi/ne-shellscalingapi-process_dpi_awareness
        print('set process dpi awareness = PROCESS_PER_MONITOR_DPI_AWARE')
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
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
            print('already admin')
    elif sys.platform == 'darwin':
        print('Allow the app(PyCharm/Terminal/...) to control your computer '
              'in "System Preferences/Security & Privacy/Accessibility",\n'
              'or mouse events will take no effects!')
        pass
    else:
        raise EnvironmentError(f'Unsupported system: {sys.platform}. please run in windows/macOS.')
    sct = mss()
    print('** Monitors information **')
    pprint.pprint(sct.monitors)
    print('WARNING: make sure "config.monitor/offset" is set properly')


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


def click(xy: Sequence = None, lapse=0.5):
    """
    click at point (x,y) or region center (x1,y1,x2,y2) within a random offset in radius 0~r
    """
    if xy is not None:
        move_to(xy)
        # print('click (%d, %d)' % (x, y))
    pyautogui.click()
    time.sleep(lapse)


def move_to(xy: Sequence):
    x, y = apply_offset(get_center_coord(xy), config.offset)
    pyautogui.moveTo(x, y)


def drag(start: Sequence, end: Sequence, duration=1.0, down_time=0.0, up_time=0.0, lapse=0.5):
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
    pyautogui.moveTo(start[0], start[1])
    if down_time is not None:
        pyautogui.mouseDown()
        time.sleep(down_time)
    pyautogui.dragRel(end[0] - start[0], end[1] - start[1], duration, mouseDownUp=False)
    if up_time is not None:
        time.sleep(up_time)
        pyautogui.mouseUp()
    time.sleep(lapse)


# %% sound related.
def beep(duration: float, interval: float = 1, loops=1):
    if loops >= 0:
        # make sure at least play once
        loops += 1
    if sys.platform == 'win32':
        import winsound
        while loops != 0:
            loops -= 1
            winsound.Beep(600, int(duration * 1000))
            time.sleep(interval)
    else:
        while loops != 0:
            loops -= 1
            t0 = time.time()
            while time.time() - t0 < duration:
                sys.stdout.write('\a')
            time.sleep(interval)
        sys.stdout.flush()


def play_music(filename, loops=1, wait=True):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops)
    if wait:
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)


def raise_alert(alert_type=None, loops=5, wait=True):
    """
    :param alert_type: bool: beep, str: ring tone, alert if supervisor found errors or task finish.
    :param loops: if loops == -1, infinite loop
    :param wait: wait music to finish. only for music rather beep.
    """
    if alert_type is None:
        alert_type = config.alert_type
    if alert_type is True:
        logger.info(f'alert: beep for {loops} loops.')
        beep(2, 1, loops)
    elif isinstance(alert_type, str):
        logger.info(f'alert: play music for {loops} loops.')
        play_music(alert_type, loops, wait)
