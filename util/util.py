"""Utils
Basic, standalone functions
"""
import ctypes
import json
import logging
import os
import random
import smtplib
import threading
import time
import winsound
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging.handlers import RotatingFileHandler
# noinspection PyUnresolvedReferences
from typing import List, Tuple, Union, Dict, Callable, Sequence

import pyautogui


class Config:
    def __init__(self, fp='config.json'):
        self.monitor = 1  # >=1, check sct.monitors to see running at which monitor, 0 is total size
        self.offset_x = 0  # xy offset for mouse click event, relative to MAIN monitor's origin
        self.offset_y = 0
        self.check_drop = True  # check craft dropped or not, if True, make sure rewards.png contains the dropped craft.
        # if crash_num in list, send_mail to remind crafts enhancing, default 5 bonus(self 4 + friend 1)
        # 5 bonus: (7, 8, 11, 12, 15, 16, 19, 20)
        # 6 bonus: (5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25)
        self.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 19, 20)
        self.jump_battle = False  # goto decoration in Battle.battle_func
        self.jump_start = False  # goto decoration in Battle.start
        self.log_time = 0  # record the time of last logging.info/debug..., set NO_LOG_TIME outside battle progress
        self.finished = False  # all battles finished, set to True before child process exist.
        self.img_net = None  # img & loc of network error, especially for jp server.
        self.loc_net = None

        # private data saved in config.json: email account, e.g.
        self.id = None
        self.receiver = None
        self.sender = None
        self.password = None
        self.load_config(fp)

    def load_config(self, fp='config.json'):
        if os.path.exists(fp):
            data: dict = json.load(open(fp, encoding='utf-8'))
            self.id = data.get('id')
            self.receiver = data.get('receiver')
            self.sender = data.get('sender')
            self.password = data.get('password')
        else:
            print(f'config file "{fp}" not exists!')
            json.dump({'id': None, 'receiver': None, 'sender': None, 'password': None},
                      open(fp, encoding='utf8'), ensure_ascii=False, indent=2)
            print(f'Create default config file "{fp}".')


config = Config()


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
        config.log_time = time.time()

    log_filter = LogFilter(func=log_func)
    _logger.addFilter(log_filter)

    formatter = logging.Formatter(
        style='{',
        datefmt="%m-%d %H:%M:%S",
        fmt='{asctime} - {filename:<10.10s}[line:{lineno:>3d}] - {levelname:<5s}: [{threadName}] {message}')

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
            record.args = [x for x in record.args if x is not NO_LOG_TIME]
        else:
            if threading.current_thread().name != 'MainThread':
                self.func()
        return True


logger = get_logger()


# %% child thread
# inspired by https://github.com/mosquito/crew/blob/master/crew/worker/thread.py
def kill_thread(thread: threading.Thread):
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


def send_mail(body, subject=None, receiver=None):
    if subject is None:
        subject = f'{body[0:50]}...' if len(body) > 50 else body
        if threading.current_thread().name != 'MainThread':
            subject = f'[{threading.current_thread().name}]' + subject
        subject = f'{time.strftime("[%H:%M]")}{subject}'
    if receiver is None:
        receiver = config.receiver
    sender = config.sender
    password = config.password
    with open('logs/log.full.log') as fd:
        lines = fd.readlines()
        n = len(lines)
        recent_records = lines[n + 1 - min(10, n):n + 1]
        body = f"""
<b>{body}</b><br>
----------------------------------<br>
<b>Recent log(log.full.log)</b>:<br>
{'<br>'.join(recent_records)}<br>
----------------------------------<br>
<b>Screenshot before shutdown</b>:<br>
<img width="80%" src="cid:screenshot"></br> 
"""
    from util.image_process import screenshot
    screenshot(monitor=config.monitor).resize((1920 // 2, 1080 // 2)).save('img/crash.jpg', format='jpeg', quality=40)
    print(f'\n--------- Email --------------\n'
          f'subject: "{subject}"'
          f'body:\n{body}'
          f'----------------------------\n')
    if None in (receiver, sender, password):
        print(f'Email account info needs to implement.\n'
              f'receiver: {receiver}\n'
              f'sender:{sender}\n'
              f'password:{password}')

        return
    # Email object
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    with open('img/crash.png', 'rb') as fd:
        m1 = MIMEImage(fd.read())
        m1.add_header('Content-ID', '<screenshot>')
        msg.attach(m1)
    # send
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
                    logger.warning(f'send success', NO_LOG_TIME)
                else:
                    logger.warning(f'send failed! Error:\n{result}', NO_LOG_TIME)
                server.quit()
                return
            except Exception as e:
                logger.warning(f'send error,type={type(e)},e={e}', NO_LOG_TIME)
                server.quit()
        except Exception as e:
            logger.warning(f'error send mail, error={e}', NO_LOG_TIME)
            logger.info(f'retry sending mail after 5 sec...({retry_time}/5 times)', NO_LOG_TIME)
            time.sleep(5)


def supervise_log_time(thread: threading.Thread, secs: float = 60, mail=False, interval=10, mute=True):
    from util.image_process import screenshot, match_which_target
    assert thread is not None, thread

    def _overtime():
        return time.time() - config.log_time > secs

    logger.info(f'start supervising thread {thread.name}...')
    thread.start()
    while not thread.is_alive():
        time.sleep(0.01)
    logger.info(f'Thread-{thread.ident}({thread.name}) started...')
    config.log_time = time.time()
    # from here, every logging should have arg: NO_LOG_TIME, otherwise endless loop.
    while True:
        # every case: stop or continue
        # case 1: all right - continue supervision
        if not _overtime():
            time.sleep(interval)
            continue
        # case 2: thread finished normally - stop supervision
        if not thread.is_alive() and config.finished:
            # thread finished
            logger.debug(f'Thread-{thread.ident}({thread.name}) finished. Stop supervising.')
            break

        # something wrong
        # case 3: network error - click "retry" and continue
        if config.img_net is not None and config.loc_net is not None:
            shot = screenshot()
            if match_which_target(shot, config.img_net, config.loc_net[0]) and \
                    match_which_target(shot, config.img_net, config.loc_net[1]):
                logger.warning('Network error! click "retry" button', NO_LOG_TIME)
                click(config.loc_net[1])
                continue
        # case 4: unrecognized error - waiting user to handle (in 30 secs)
        loops = 15
        logger.warning(f'Something went wrong, please solve it\n', NO_LOG_TIME)
        while loops > 0:
            print(f'Or it will be force stopped...')
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
                          f' Time run out! lapse={time.time() - config.log_time:.2f}(>{secs}) secs.'
                print(err_msg)
                if mail:
                    subject = f'[{thread.name}]something went wrong!'
                    send_mail(err_msg, subject=subject)
                kill_thread(thread)
                print('exit supervisor after killing thread.')
                return


def check_sys_admin(admin=True):
    # set dpi awareness & check admin permission
    # useless in Python Console of Pycharm
    print('HINT: make sure "Config.offset_x/y" is set properly')
    # SetProcessDpiAwareness: see
    # https://docs.microsoft.com/zh-cn/windows/win32/api/shellscalingapi/ne-shellscalingapi-process_dpi_awareness
    print('set process dpi awareness = PROCESS_PER_MONITOR_DPI_AWARE')
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    if admin:
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            print('Please run cmd/Pycharm as admin to click inside programs with admin permission(e.g. MuMu).')
            # To run a new process as admin, no effect in Pycharm's Python Console mode.
            # print('applying admin permission in a new process, and no effect when in console mode.')
            # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            raise PermissionError('Run as admin')
        else:
            print('already admin')


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
        pyautogui.mouseUp()
        time.sleep(up_time)
    time.sleep(lapse)


def get_pixel(xy):
    # RGB
    color = ctypes.windll.gdi32.GetPixel(ctypes.windll.user32.GetDC(None), xy[0], xy[1])
    return color


def convert_to_list(items):
    if items is None:
        return []
    elif isinstance(items, Sequence):
        return list(items)
    else:
        return [items]


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
