"""Utils

Basic, standalone functions
"""
import time
import random
import ctypes
import win32api
import win32con
import logging
import smtplib
from email.mime.text import MIMEText
# noinspection PyUnresolvedReferences
from typing import List, Tuple, Union, Dict, Callable
from importlib import reload as reload_module

G = {}  # shared global data


# %% logger
def send_mail(content, subject=None, receiver=None):
    if subject is None:
        subject = 'Mail from python script'
    if receiver is None:
        receiver = '984585714@qq.com'  # 收件人邮箱
    sender = '1570105257@qq.com'  # 发送方邮箱
    password = 'dclkqgbzjdvahhaf'  # 填入发送方邮箱的授权码
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
    try:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        print('send success')
    except Exception as e:
        print(f'send error,type={type(e)},e={e}')
    finally:
        server.quit()


def check_log_time(secs: float):
    # last=time.time()
    print('start check_log_time...')
    while not G.get('finished', False):
        now = time.time()
        last2 = G.get('last_log_time', now)
        lapse = now - last2
        if lapse > secs:
            print(f'lapse={lapse:.2f}, maybe something went wrong.\r', end='')
            # send mail
        time.sleep(30)


# logger
def get_logger(name='log', level=logging.INFO, record_time=True):
    # noinspection PyUnresolvedReferences
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    if record_time:
        log_filter = LogFilter()
        _logger.addFilter(log_filter)
    formatter = logging.Formatter('%(asctime)s - %(filename)-10s[line:%(lineno)3d] - %(levelname)-5s: %(message)s',
                                  "%m-%d %H:%M:%S")
    fh = logging.FileHandler('log/%s.log' % name)
    fh.setFormatter(formatter)
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)

    _logger.addHandler(ch)
    _logger.addHandler(fh)
    return _logger


class LogFilter(logging.Filter):
    def filter(self, record):
        G['last_log_time'] = time.time()
        return True


# %% win32: mouse & screen pixel
def move_mouse(x=None, y=None):
    x = int(x)
    y = int(y)
    # logger.debug('mouse move:',x,'-',y)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)


def click(xy: tuple = None, lapse=0.5, r=2):
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
            raise ValueError('len(xy) should be 2 or 4.')
        x += random.randint(-r, r)
        y += random.randint(-r, r)
        move_mouse(x, y)
        # m.click(x, y)
        # logger.debug('click (%d, %d)' % (x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(lapse)


def get_pixel(xy):
    # RGB
    color = ctypes.windll.gdi32.GetPixel(ctypes.windll.user32.GetDC(None), xy[0], xy[1])
    # logger.debug(hex(color))
    # logger.debug((color & ((1 << 8) - 1)))
    # logger.debug((color >> 8 & ((1 << 8) - 1)))
    # logger.debug((color >> 16 & ((1 << 8) - 1)))
    return color


def check_admin():
    import sys
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print('require admin')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        print('already admin')


class Timer:
    t1 = 0
    t2 = 0
    dt = 0

    def start(self):
        self.t1 = time.time()
        return self

    def stop(self):
        self.t2 = time.time()
        self.dt = self.t2 - self.t1
        # print('Time lapse: %f sec' % (self.t2 - self.t1))
        return self
