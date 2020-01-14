"""Utils
Basic, standalone functions
"""
import smtplib
import socket
import winsound
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from util.autogui import *


def supervise_log_time(thread: threading.Thread, secs: float = 60, mail=False, interval=10, mute=True):
    assert thread is not None, thread

    def _overtime():
        return time.time() - BaseConfig.log_time > secs

    logger.info(f'start supervising thread {thread.name}...')
    thread.start()
    while not thread.is_alive():
        time.sleep(0.01)
    logger.info(f'Thread-{thread.ident}({thread.name}) started...')
    BaseConfig.log_time = time.time()
    # from here, every logging should have arg: NO_LOG_TIME, otherwise endless loop.
    loops = 15
    while True:
        # every case: stop or continue
        # case 1: all right - continue supervision
        if not _overtime():
            loops = 15  # reset loops
            time.sleep(interval)
            continue
        # case 2: thread finished normally - stop supervision
        if not thread.is_alive() and BaseConfig.task_finished:
            # thread finished
            logger.debug(f'Thread-{thread.ident}({thread.name}) finished. Stop supervising.')
            if mail:
                send_mail('Task finished.')
            break

        # something wrong
        # case 3: network error - click "retry" and continue
        if config.img_net is not None and config.loc_net is not None:
            shot = screenshot()
            if is_match_target(shot, config.img_net, config.loc_net[0]) and \
                    is_match_target(shot, config.img_net, config.loc_net[1]):
                logger.warning('Network error! click "retry" button', NO_LOG_TIME)
                click(config.loc_net[1], lapse=3)
                BaseConfig.log_time += 30
                continue
        # case 4: unrecognized error - waiting user to handle (in 2*loops seconds)
        logger.warning(f'Something wrong, please solve it, or it will be force stopped... {loops}', NO_LOG_TIME)
        loops -= 1
        if mute:
            time.sleep(2)
        else:
            winsound.Beep(600, 1400)
            time.sleep(0.6)
        if loops < 0:
            # not solved! kill thread and stop.
            err_msg = f'Thread-{thread.ident}({thread.name}):' \
                      f' Time run out! lapse={time.time() - BaseConfig.log_time:.2f}(>{secs}) secs.'
            print(err_msg)
            if mail:
                send_mail(err_msg, subject=f'[{thread.name}]something went wrong!')
            kill_thread(thread)
            print('exit supervisor after killing thread.')
            return


# inspired by https://github.com/mosquito/crew/blob/master/crew/worker/thread.py
def kill_thread(thread: threading.Thread):
    logger.warning(f'ready to kill thread-{thread.ident}({thread.name})')
    if not thread.is_alive():
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

    while thread.is_alive():
        time.sleep(0.01)
    logger.critical(f'Thread-{thread.ident}({thread.name}) have been killed!')


def send_mail(body, subject=None, receiver=None, attach_shot=True):
    if subject is None:
        subject = f'{body[0:50]}...' if len(body) > 50 else body
    if threading.current_thread().name != 'MainThread':
        subject = f'[{threading.current_thread().name}]{subject}'
    subject = f'{time.strftime("[%H:%M]")}{subject}'
    if BaseConfig.log_file is not None and os.path.exists(config.log_file):
        with open(BaseConfig.log_file, encoding='utf8') as fd:
            lines = fd.readlines()
            n = len(lines)
            recent_records = lines[n + 1 - min(10, n):n + 1]
            body = f"""
<b>{body}</b><br>
Computer name: <b>{socket.getfqdn(socket.gethostname())}</b><br>
----------------------------------<br>
<b>Recent log({BaseConfig.log_file})</b>:<br>
{'<br>'.join(recent_records)}<br>
----------------------------------<br>
{'<b>Screenshot before shutdown</b>:<br>' +
 '<img width="80%" src="cid:screenshot"></br>' if attach_shot else ''}
"""
    from util.autogui import screenshot
    crash_fp = 'img/crash.jpg'
    screenshot(monitor=config.monitor).resize((1920 // 2, 1080 // 2)).save(crash_fp, format='jpeg', quality=40)
    logger.info(f'\n--------- Email --------------\n'
                f'subject: "{subject}"\n'
                f'receiver: {receiver}\n'
                f'body:\n{body}\n'
                f'------------------------------\n')
    if receiver is None:
        receiver = config.receiver
    if None in (receiver, config.sender, config.password):
        print(f'----Email account info needs to be updated.-----\n'
              f'receiver: {receiver}\n'
              f'sender:{config.sender}\n'
              f'password:{"*****"}'
              f'----------------------------\n')
        return

    # Email object
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr((config.sender_name, config.sender))
    msg['To'] = receiver
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    if attach_shot:
        with open(crash_fp, 'rb') as fd:
            m1 = MIMEImage(fd.read())
            m1.add_header('Content-ID', '<screenshot>')
            msg.attach(m1)
    # send
    retry_time = 0
    while retry_time < 5:
        retry_time += 1
        try:
            server = smtplib.SMTP_SSL(config.server_host, config.server_port)  # 邮件服务器及端口号
            # server.set_debuglevel(1)
            try:
                server.login(config.sender, config.password)
                result = server.sendmail(config.sender, receiver, msg.as_string())
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
            logger.warning(f'connect server "{(config.server_host, config.server_port)}" failed,'
                           f' error_type={type(e)},\ne={e}', NO_LOG_TIME)
            logger.info(f'retry sending mail after 5 sec...({retry_time}/5 times)', NO_LOG_TIME)
        time.sleep(5)
