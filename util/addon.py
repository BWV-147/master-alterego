__all__ = [
    'send_mail',
    'beep',
    'play_music',
    'raise_alert',
    'kill_thread',
    'threading',
    'os',
]

import ctypes
import email.utils
import html
import os
import smtplib
import socket
import sys
import threading
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy
import wda  # noqa

if 'PYGAME_HIDE_SUPPORT_PROMPT' not in os.environ:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from .config import *
from .log import *


# %% email
def send_mail(body, subject=None, receiver=None, attach_shot=True, level=MAIL_DEBUG):
    from .autogui import screenshot
    # check email params
    if not (MAIL_MUTE < config.mail <= level):
        logger.info(f'Don\'t send mail.\nSubject: {subject}\nBody: {body}')
        return
    if receiver is None:
        receiver = config.mail_receiver
    if None in (receiver, config.mail_sender, config.mail_password):
        logger.warning(f'Incomplete email config:\n'
                       f'======== Incomplete Email Settings ========\n'
                       f' - receiver: {receiver}\n'
                       f' - sender  : {config.mail_sender}\n'
                       f' - password:{"*****" if config.mail_password else "None"}\n'
                       f'===========================================\n')
        return

    mail = MIMEMultipart()

    # subject
    if subject is None:
        subject = f'{body[0:50]}...' if len(body) > 50 else body
    if threading.current_thread().name != 'MainThread':
        subject = f'[{threading.current_thread().name}]{subject}'
    subject = f'{time.strftime("[%H:%M]")}{subject}'

    # body
    logger.info('send mail:\n' + html.unescape(body))
    body = f'<b><pre>{html.escape(body)}</pre></b><br>\n' \
           f'<hr><b>Computer name:</b><br>{socket.getfqdn(socket.gethostname())}<br><hr>\n'

    # body.screenshot
    crash_fp = 'img/crash.jpg'
    if attach_shot:
        body += '<b>Screenshot before shutdown</b>:<br>\n' \
                '<img src="cid:screenshot" style="width: 100%; max-width: 720px;"><br><hr>\n'
        shot = screenshot()
        shot.save(crash_fp + '.png')  # save a backup of origin screenshot
        # shrink the image/email size
        shot.resize((numpy.array(shot.size) / 1.5).astype('int')).save(crash_fp, format='jpeg', quality=40)
        with open(crash_fp, 'rb') as fd:
            image = MIMEImage(fd.read())
            image.add_header('Content-ID', '<screenshot>')
            mail.attach(image)

    # body.recent_log
    if logger.log_filepath and os.path.exists(logger.log_filepath):
        with open(logger.log_filepath, encoding='utf8') as fd:
            lines = fd.readlines()
            n = len(lines)
            # "<" should be replaced with escape characters even in <pre/>
            recent_records = ['<code>' + html.escape(x.rstrip()) + '</code>\n' for x in lines[-min(20, n):]]
            body += f'<b>Recent 10 logs ({logger.log_filepath}):</b><br>\n' \
                    '<style>.logs pre { margin: 0.3em auto; font-family: "Consolas"; }</style>\n' \
                    f'<span class="logs">\n<pre>{"".join(recent_records)}</pre></span><hr>'

    print(f'Ready to send email:\n'
          f'=============== Email ===============\n'
          f' - Subject  : {subject}\n'
          f' - Receiver : {receiver}\n'
          f' - Body html:\n{body}\n'
          f'================ End ================\n')

    # make email
    mail['Subject'] = subject
    mail['From'] = email.utils.formataddr((config.mail_sender_name, config.mail_sender))
    mail['To'] = receiver
    mail['Date'] = email.utils.formatdate(localtime=True)
    mail.attach(MIMEText(body, 'html', 'utf-8'))

    # send email, retry 5 times at most if failed.
    retry_time = 0
    while retry_time < 5:
        retry_time += 1
        try:
            server = smtplib.SMTP_SSL(config.mail_server_host, config.mail_server_port)
            # server.set_debuglevel(1)
            try:
                server.login(config.mail_sender, config.mail_password)
                result = server.sendmail(config.mail_sender, receiver, mail.as_string())
                if result == {}:
                    logger.info(f'send email success.')
                else:
                    logger.warning(f'send email failed! Result:\n{result}')
                server.quit()
                break
            except Exception:
                server.quit()
                raise
        except Exception as e:
            logger.warning(f'Error when sending email: {type(e)}\n{e}')
            logger.debug(f'retry sending mail in 5 seconds... ({retry_time}/5 times)')
            time.sleep(5)


# %% sound related.
def beep(duration: float, interval: float = 1, loops: int = 1):
    """Beep `duration` seconds then mute `interval` seconds for loops."""
    if loops == 0:
        loops = 1
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
    if os.path.exists(filename):
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
    :param loops: if loops <0, infinite loop, else loop at least once.
    :param wait: wait music to finish. only for music rather beep.
    """
    if alert_type is None:
        alert_type = config.alert_type
    if alert_type is True:
        logger.debug(f'alert: beep for {loops} loops.')
        beep(2, 1, loops)
    elif isinstance(alert_type, str) and alert_type:
        logger.debug(f'alert: play music for {loops} loops.')
        play_music(alert_type, loops, wait)


# %% system
def kill_thread(thread: threading.Thread):
    """
    Support killing thread both in terminal and interactive console.

    In terminal:
        - sys.exit() only raise error to exit child **THREAD** (exit process if only main thread),
          while os._exit() exit **PROCESS** without cleaning (not recommended).
        - multiprocessing: can use process.terminate() or sys.exit()
    In interactive console:
        - both sys.exit() and os._exit() will exit console, so it's not the better choice.
        - multiprocessing is not supported in console.
    """
    friendly_name = f'Thread-{thread.ident}({thread.name})'
    logger.info(f'Ready to kill {"*self* " if thread == threading.current_thread() else ""}{friendly_name}')
    if not thread.is_alive():
        logger.info(f'{friendly_name} is already not alive!')
        return

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
    if res == 0:
        raise ValueError('nonexistent thread id')
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError('PyThreadState_SetAsyncExc failed')

    while thread.is_alive():
        time.sleep(0.01)
    logger.info(f'{friendly_name} have been killed!')


def check_sys_setting(check_admin=True, check_wda=False):
    if check_wda is True:
        # WDA+iOS real device, check in config.init_wda()
        if config.is_wda:
            client = config.wda_client = wda.Client(config.wda_settings.get('url', None))
            try:
                # quality:
                # 0-max(time is wasted to transfer large image),
                # 1-middle,
                # 2-lowest, may not clear enough
                # once changed the quality value, image templates should be updated
                print(f"window size = {client.window_size()}")
                print(f"screenshot size = {client.screenshot().size}")
                print(f"scale = {client.scale}")
                print(f'WDA connected, current app: {client.app_current()["bundleId"]}')
                default_settings = client.appium_settings()
                settings = {k: v for k, v in config.wda_settings.items() if k in default_settings}
                if settings:
                    print(f'set WDA: {settings}')
                    print(client.appium_settings(settings))
            except Exception as e:
                print(f'Error:\n {e}')
                raise EnvironmentError(f'WebDriverAgent is not configured properly!')

    if sys.platform == 'win32':
        # Android/iOS emulator in Windows
        # check admin permission & set process dpi awareness
        # please run cmd/powershell or Pycharm as administrator.
        from init import initialize
        initialize()
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            if check_admin:
                print('[Emulator] Please run cmd/Pycharm as admin to click inside emulators with admin permission.')
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
    elif sys.platform == 'darwin':
        # Android emulator in macOS
        print('[Android Emulators] For the app who is running the script(PyCharm/Terminal/...), '
              'two permissions are required:\n'
              '   "Accessibility" and "Screen Recording" inside "System Preferences/Security & Privacy/"\n',
              file=sys.stderr)
