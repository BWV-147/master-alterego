"""Utils

Basic, standalone functions
"""
import time
import random
import ctypes
import win32api
import win32con
import logging
import ctypes
import threading
import smtplib
import winsound
from email.mime.text import MIMEText
# noinspection PyUnresolvedReferences
from typing import List, Tuple, Union, Dict, Callable
from importlib import reload as reload_module

G = {}  # shared global data


# %% logger
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
    def filter(self, record: logging.LogRecord):
        G[threading.current_thread().name + '.log_time'] = time.time()
        record.msg = f"[{threading.current_thread().name:<10s}] {record.msg}"
        return True


# %% child thread

# inspired by https://github.com/mosquito/crew/blob/master/crew/worker/thread.py
def kill_thread(thread: threading.Thread, exception: BaseException = TimeoutError) -> None:
    if not thread.isAlive():
        return

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), ctypes.py_object(exception)
    )

    if res == 0:
        raise ValueError('nonexistent thread id')
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError('PyThreadState_SetAsyncExc failed')

    while thread.isAlive():
        time.sleep(0.01)
    print(f'Thread-{thread.ident}({thread.name}) have been killed!')


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


def supervise_log_time(threads: Union[List[threading.Thread], threading.Thread],
                       secs: float = 60, mail=False, interval=10):
    if isinstance(threads, threading.Thread):
        threads = [threads]
    print('start supervise_log_time...')
    for thread in threads:
        get_logger().info(f'Thread-{thread.ident}({thread.name}) starting...')
        thread.start()
        G[thread.name + '.log_time'] = time.time()
        time.sleep(0.01)
    while True:
        alive = False
        for thread in threads:
            if not thread.is_alive():
                continue
            alive = True
            now = time.time()
            last = G[thread.name + '.log_time']
            lapse = now - last
            if lapse > secs:
                err_msg = f'Thread-{thread.ident}({thread.name}): Time run out! lapse={lapse:.2f}(>{secs}) secs.'
                print(err_msg)
                if mail:
                    # import winsound
                    # while True:
                    #     winsound.Beep(500, 1000)
                    #     time.sleep(1000)
                    send_mail(err_msg, subject=f'{time.strftime("[%m-%d %H:%M:%S]")} Dell-iOS went wrong!')
                # while True:
                #     winsound.Beep(600, 1000)
                #     time.sleep(0.4)
                kill_thread(thread)
        time.sleep(interval)
        if alive is False:
            break


# %% win32: mouse & screen pixel
def is_second_screen():
    return 'right' in threading.current_thread().name or G.get('right', False)


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
    while G.get('click', False):
        time.sleep(0.1)
    G['click'] = True
    if xy is not None:
        if 2 == len(xy):
            x, y = xy[:]
        elif 4 == len(xy):
            x, y = ((xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2)
        else:
            raise ValueError('len(xy) should be 2 or 4.')
        if is_second_screen():
            x += 1920
        x += random.randint(-r, r)
        y += random.randint(-r, r)
        move_mouse(x, y)
        # m.click(x, y)
        # logger.debug('click (%d, %d)' % (x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    # print(f'{time.asctime()} - click at {xy}')
    G['click'] = False
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
        print('e.g. click somewhere inside a program(Blupapa) with admin, the python thread also need admin.')
        print('require admin, take no effect when in console. ')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        print('already admin')


def convert_list(items):
    if items is None:
        return []
    elif isinstance(items, (list, tuple)):
        return list(items)
    else:
        return [items]


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
