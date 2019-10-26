"""Utils
Basic, standalone functions
"""
import os
import sys
import time
import random
import json
import ctypes
import win32api
import win32con
import logging
from logging.handlers import RotatingFileHandler
import ctypes
import threading
import winsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
# noinspection PyUnresolvedReferences
from typing import List, Tuple, Union, Dict, Callable
from pprint import pprint

# check network_error
G = {}  # shared global data


# %% logger
def get_logger(name='log', level=logging.INFO, save=True):
    # noinspection PyUnresolvedReferences
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    # creat a new logger
    log_path = 'logs/'
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)

    def log_func():
        G['log_time'] = time.time()

    log_filter = LogFilter(func=log_func)
    _logger.addFilter(log_filter)

    formatter = logging.Formatter(
        style='{',
        datefmt="%m-%d %H:%M:%S",
        fmt='{asctime} - {filename:<10.10s}[line:{lineno:>3d}] - {levelname:<5s}: [{threadName:<10s}] {message}')

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)
    _logger.addHandler(console)

    if save:
        fh = RotatingFileHandler(os.path.join(log_path, f'{name}.log'), maxBytes=1024 * 1024, backupCount=3)
        fh.setFormatter(formatter)
        fh.setLevel(level)
        _logger.addHandler(fh)

        if level > logging.DEBUG:
            full_fh = RotatingFileHandler(os.path.join(log_path, f'{name}.full.log'), maxBytes=1024 * 1024,
                                          backupCount=3)
            full_fh.setFormatter(formatter)
            full_fh.setLevel(logging.DEBUG)
            _logger.addHandler(full_fh)
    return _logger


NO_LOG_TIME = 'NO_LOG_TIME'


class LogFilter(logging.Filter):
    def __init__(self, func=None):
        super().__init__()
        assert callable(func)
        self.func = func

    def filter(self, record: logging.LogRecord):
        if NO_LOG_TIME in record.args:
            self.func()
            record.args = [x for x in record.args if x is not NO_LOG_TIME]
        return True


logger = get_logger()


# logger2 = get_logger('craft', logging.WARNING)


# %% child thread

# inspired by https://github.com/mosquito/crew/blob/master/crew/worker/thread.py
def kill_thread(thread: threading.Thread) -> None:
    logger.warning(f'ready to kill thread-{thread.ident}({thread.name})')
    if not thread.isAlive():
        return

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), ctypes.py_object(SystemExit)
    )
    # print(f'kill thread res={res}')
    if res == 0:
        raise ValueError('nonexistent thread id')
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError('PyThreadState_SetAsyncExc failed')

    while thread.isAlive():
        time.sleep(0.01)
    logger.critical(f'Thread-{thread.ident}({thread.name}) have been killed!')


def send_mail(content, subject=None, receiver=None):
    if subject is None:
        subject = f'{content[0:50]}...' if len(content) > 50 else content
    if receiver is None:
        receiver = '984585714@qq.com'
    sender = '1570105257@qq.com'
    password = 'dclkqgbzjdvahhaf'

    msg = MIMEMultipart()
    with open('logs/log.full.log') as fd:
        lines = fd.readlines()
        n = len(lines)
        recent_records = lines[n + 1 - min(10, n):n + 1]
        content = f"""
<b>{content}</b><br>
----------------------------------<br>
<b>Recent log(log.full.log)</b>:<br>
{'<br>'.join(recent_records)}<br>
----------------------------------<br>
<b>Screenshot before shutdown</b>:<br>
<img width="80%" src="cid:image1"></br> 
"""
        body = MIMEText(content, 'html', 'utf-8')
        msg.attach(body)

    from util.image_process import screenshot
    screenshot().save(open('img/crash.png', 'wb'), quality=50)
    with open('img/crash.png', 'rb') as fd:
        m1 = MIMEImage(fd.read())
        m1.add_header('Content-ID', '<image1>')
        msg.attach(m1)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    retry_time = 0
    while retry_time < 5:
        retry_time += 1
        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
            # server.set_debuglevel(1)
            try:
                server.login(sender, password)
                result = server.sendmail(sender, receiver, msg.as_string())
                if result == {}:
                    logger.warning(f'send success, content=\n{content}', NO_LOG_TIME)
                else:
                    logger.warning(f'send failed! Error:\n{result}', NO_LOG_TIME)
                server.quit()
                return
            except Exception as e:
                logger.warning(f'send error,type={type(e)},e={e}', NO_LOG_TIME)
                server.quit()
        except Exception as e:
            logger.warning(f'error send mail, error={e}', NO_LOG_TIME)
            time.sleep(5)
            logger.info(f'retry sending mail...({retry_time}/5 times)', NO_LOG_TIME)


def supervise_log_time(thread: threading.Thread, secs: float = 60, mail=False, interval=10, mute=False):
    from util.image_process import screenshot, cal_sim, match_which_target
    assert thread is not None, thread

    def _overtime():
        return time.time() - G['log_time'] > secs

    logger.info(f'start supervising thread {thread.name}...')
    thread.start()
    while not thread.is_alive():
        time.sleep(0.01)
    logger.info(f'Thread-{thread.ident}({thread.name}) started...')
    G['log_time'] = time.time()
    # from here, every logging should have arg: NO_LOG_TIME, otherwise endless loop.
    while True:
        # every case: stop or continue
        # case 1: all right - continue supervision
        if not _overtime():
            time.sleep(interval)
            continue
        # case 2: thread finished normally - stop supervision
        if not thread.is_alive() and G.get('finish', False):
            # thread finished
            logger.debug(f'Thread-{thread.ident}({thread.name}) finished. Stop supervising.')
            break

        # something wrong
        # case 3: network error - click "retry" and continue
        img_net = G.get('img_net')
        loc_net = G.get('loc_net')
        if img_net is not None and loc_net is not None:
            shot = screenshot()
            if cal_sim(shot, img_net, loc_net[0]) > 0.9 and cal_sim(shot, img_net, loc_net[1]) > 0.9:
                logger.warning('Network error! click "retry" button', NO_LOG_TIME)
                click(loc_net[1])
                continue
        # case 4: unrecognized error - waiting user to handle (in 30 secs)
        loops = 15
        logger.warning(f'Something went wrong, please solve it\n', NO_LOG_TIME)
        while loops > 0:
            print(f'Or it will be force stopped after {loops * 2} seconds...')
            loops -= 1
            if mute:
                time.sleep(2)
            else:
                winsound.Beep(600, 1400)
                time.sleep(0.6)
            if not _overtime():
                # case 4.1: user solved the issue and continue supervision
                break
            else:
                # case 4.2: wrong! kill thread and stop
                err_msg = f'Thread-{thread.ident}({thread.name}):' \
                          f' Time run out! lapse={time.time() - G["log_time"]:.2f}(>{secs}) secs.'
                print(err_msg)
                if mail:
                    subject = f'{time.strftime("[%m-%d %H:%M]")} {thread.name} went wrong!'
                    send_mail(err_msg, subject=subject)
                kill_thread(thread)
                print('exit supervisor after killing thread.')


def check_sys_admin(admin=True):
    # set dpi awareness & check admin permission
    # useless in Python Console of Pycharm
    print('set "G[\'offset_x\'] = -1920" if window in left & vice screen')
    # SetProcessDpiAwareness: see
    # https://docs.microsoft.com/zh-cn/windows/win32/api/shellscalingapi/ne-shellscalingapi-process_dpi_awareness
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    if admin:
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            print('e.g. click somewhere inside admin programs(Blupapa), the python process also need admin permission.')
            print('applying admin permission in a new process, take no effect when in console mode.')
            # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            exit(0)
        else:
            print('already admin')


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
    if xy is not None:
        if 2 == len(xy):
            x, y = xy[:]
        elif 4 == len(xy):
            x, y = ((xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2)
        else:
            raise ValueError(f'xy=${xy}: len(xy) should be 2 or 4.')
        x += random.randint(-r, r) + G.get('offset_x', 0)
        y += random.randint(-r, r) + G.get('offset_y', 0)
        move_mouse(x, y)
        # print('click (%d, %d)' % (x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(lapse)


def drag(start: tuple, end: tuple, duration=1):
    # TODO
    import pyautogui
    time.sleep(0.2)
    pyautogui.dragTo()
    move_mouse(start)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.5)
    pass


def get_pixel(xy):
    # RGB
    color = ctypes.windll.gdi32.GetPixel(ctypes.windll.user32.GetDC(None), xy[0], xy[1])
    return color


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
        self.dt = None
        return self

    def lapse(self):
        return time.time() - self.t1

    def stop(self):
        self.t2 = time.time()
        self.dt = self.t2 - self.t1
        # print('Time lapse: %f sec' % (self.t2 - self.t1))
        return self
