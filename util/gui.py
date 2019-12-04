import ctypes
import random
from pprint import pprint

import pyautogui
from mss import mss

from util.base import *
from util.config import *


def check_sys_admin(admin=True):
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
                  'Operations (e.g. click) with admin programs will take no effects!')
    else:
        print('already admin')
    sct = mss()
    print('** Monitors information **')
    pprint(sct.monitors)
    print('WARNING: make sure "config.monitor/offset_x/y" is set properly')


# %% win32: mouse & screen pixel
def move_mouse(x=None, y=None):
    x = int(x)
    y = int(y)
    # logger.debug('mouse move:',x,'-',y)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)


def click(xy: Sequence = None, lapse=0.5, r=2):
    """
    click at point (x,y) or region center (x1,y1,x2,y2) within a random offset in radius 0~r
    :param xy:
    :param lapse:
    :param r:
    :return:
    """
    if xy is not None:
        if 2 == len(xy):
            x, y = xy[:]
        elif 4 == len(xy):
            x, y = ((xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2)
        else:
            raise ValueError(f'xy=${xy}: len(xy) should be 2 or 4.')
        x += random.randint(-r, r) + config.offset_x
        y += random.randint(-r, r) + config.offset_y
        move_mouse(x, y)
        # print('click (%d, %d)' % (x, y))
    pyautogui.click()
    time.sleep(lapse)


def drag(start: Sequence, end: Sequence, duration=1.0, down_time=0.0, up_time=0.0, lapse=0.5):
    """
    drag event
    :param start: (x1,y1)
    :param end: (x2,y2) both absolute coordinate
    :param duration: duration of mouse moving
    :param down_time: (None, double) time between mouse down and move start. If None, no mouse down event.
    :param up_time: (None, double) time between move end and mouse up. If None, no mouse up event.
    :param lapse: lapse after mouse up
    :return:
    """
    move_mouse(start[0], start[1])
    if down_time is not None:
        pyautogui.mouseDown()
        time.sleep(down_time)
    pyautogui.dragRel(end[0] - start[0], end[1] - start[1], duration, mouseDownUp=False)
    if up_time is not None:
        time.sleep(up_time)
        pyautogui.mouseUp()
    time.sleep(lapse)


def get_pixel(xy):
    # RGB
    color = ctypes.windll.gdi32.GetPixel(ctypes.windll.user32.GetDC(None), xy[0], xy[1])
    return color
