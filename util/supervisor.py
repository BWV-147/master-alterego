"""Utils
Basic, standalone functions
"""
import smtplib
import winsound
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from util.autogui import *


def supervise_log_time(thread: threading.Thread, secs: float = 60, mail=False, interval=10, mute=True):
    assert thread is not None, thread

    def _overtime():
        return time.time() - CONFIG.log_time > secs

    logger.info(f'start supervising thread {thread.name}...')
    thread.start()
    while not thread.is_alive():
        time.sleep(0.01)
    logger.info(f'Thread-{thread.ident}({thread.name}) started...')
    CONFIG.log_time = time.time()
    # from here, every logging should have arg: NO_LOG_TIME, otherwise endless loop.
    while True:
        # every case: stop or continue
        # case 1: all right - continue supervision
        if not _overtime():
            time.sleep(interval)
            continue
        # case 2: thread finished normally - stop supervision
        if not thread.is_alive() and CONFIG.task_finished:
            # thread finished
            logger.debug(f'Thread-{thread.ident}({thread.name}) finished. Stop supervising.')
            break

        # something wrong
        # case 3: network error - click "retry" and continue
        if CONFIG.img_net is not None and CONFIG.loc_net is not None:
            shot = screenshot()
            if is_match_target(shot, CONFIG.img_net, CONFIG.loc_net[0]) and \
                    is_match_target(shot, CONFIG.img_net, CONFIG.loc_net[1]):
                logger.warning('Network error! click "retry" button', NO_LOG_TIME)
                click(CONFIG.loc_net[1], lapse=5)
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
                          f' Time run out! lapse={time.time() - CONFIG.log_time:.2f}(>{secs}) secs.'
                print(err_msg)
                if mail:
                    subject = f'[{thread.name}]something went wrong!'
                    send_mail(err_msg, subject=subject)
                kill_thread(thread)
                print('exit supervisor after killing thread.')
                return


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
        subject = f'[{threading.current_thread().name}]{subject}'
    subject = f'{time.strftime("[%H:%M]")}{subject}'
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
    from util.autogui import screenshot
    crash_fp = 'img/crash.jpg'
    screenshot(monitor=CONFIG.monitor).resize((1920 // 2, 1080 // 2)).save(crash_fp, format='jpeg', quality=40)
    print(f'\n--------- Email --------------\n'
          f'subject: "{subject}"'
          f'body:\n{body}'
          f'----------------------------\n')
    if receiver is None:
        receiver = CONFIG.receiver
    if None in (receiver, CONFIG.sender, CONFIG.password):
        print(f'----Email account info needs to update.-----\n'
              f'receiver: {receiver}\n'
              f'sender:{CONFIG.sender}\n'
              f'password:{"*" * len(CONFIG.password)}'
              f'----------------------------\n')
        return

    # Email object
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr([CONFIG.sender_name, CONFIG.sender])
    msg['To'] = receiver
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    with open(crash_fp, 'rb') as fd:
        m1 = MIMEImage(fd.read())
        m1.add_header('Content-ID', '<screenshot>')
        msg.attach(m1)
    # send
    retry_time = 0
    while retry_time < 5:
        retry_time += 1
        try:
            server = smtplib.SMTP_SSL(CONFIG.server_host, CONFIG.server_port)  # 邮件服务器及端口号
            # server.set_debuglevel(1)
            try:
                server.login(CONFIG.sender, CONFIG.password)
                result = server.sendmail(CONFIG.sender, receiver, msg.as_string())
                if result == {}:
                    logger.warning(f'send success', NO_LOG_TIME)
                else:
                    logger.warning(f'send failed! Error:\n{result}', NO_LOG_TIME)
                server.quit()
                return
            except Exception as e:
                logger.warning(f'send error, error_type={type(e)},\ne={e}', NO_LOG_TIME)
                server.quit()
        except Exception as e:
            logger.warning(f'connect server "{(CONFIG.server_host, CONFIG.server_port)}" failed,'
                           f' error_type={type(e)},\ne={e}', NO_LOG_TIME)
            logger.info(f'retry sending mail after 5 sec...({retry_time}/5 times)', NO_LOG_TIME)
        time.sleep(5)
