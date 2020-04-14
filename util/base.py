import argparse
import smtplib
import socket
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
# noinspection PyUnresolvedReferences
from typing import List, Tuple, Union, Dict, Callable, Sequence, Optional

from util.my_logger import *


class ArgParser:
    _parser: argparse.ArgumentParser = None

    def __init__(self, args: list = None):
        self._init_parser()
        self.supervise = None
        self.config = None
        self.parse(args)

    def parse(self, args):
        # args without filename
        resolved_args = self._parser.parse_known_intermixed_args(args)[0]
        self.supervise = not resolved_args.disable_supervisor
        self.config = resolved_args.config

    @property
    def parser(self):
        return self._parser

    @classmethod
    def _init_parser(cls):
        if cls._parser is not None:
            return
        cls._parser = argparse.ArgumentParser(conflict_handler='resolve')
        cls._parser.add_argument('-c', '--config', default='data/config.json', help='config file path.')
        cls._parser.add_argument('-d', '--disable-supervisor', action='store_true',
                                 help='disable supervisor (default enabled).')


def convert_to_list(items):
    if items is None:
        return []
    elif isinstance(items, Sequence):
        return list(items)
    else:
        return [items]


def get_center_coord(xy: Sequence):
    if 2 == len(xy):
        return xy
    elif 4 == len(xy):
        return (xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2
    else:
        raise ValueError(f'xy=${xy}: len(xy) should be 2 or 4.')


def send_mail(body, subject=None, receiver=None, attach_shot=True):
    from util.autogui import screenshot
    if subject is None:
        subject = f'{body[0:50]}...' if len(body) > 50 else body
    if threading.current_thread().name != 'MainThread':
        subject = f'[{threading.current_thread().name}]{subject}'
    subject = f'{time.strftime("[%H:%M]")}{subject}'
    if config.log_file is not None and os.path.exists(config.log_file):
        with open(config.log_file, encoding='utf8') as fd:
            lines = fd.readlines()
            n = len(lines)
            recent_records = lines[n + 1 - min(10, n):n + 1]
            body = f"""
<b>{body}</b><br>
----------------------------------<br>
Computer name: <b>{socket.getfqdn(socket.gethostname())}</b><br>
----------------------------------<br>
<b>Recent log({config.log_file})</b>:<br>
{'<br>'.join(recent_records)}<br>
----------------------------------<br>
{'<b>Screenshot before shutdown</b>:<br>' +
 '<img width="80%" src="cid:screenshot"></br>' if attach_shot else ''}
"""

    logger.info(f'ready to send email:\n'
                f'--------- Email --------------\n'
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
        crash_fp = 'img/crash.jpg'
        shot = screenshot()
        shot.save(crash_fp + '.png')
        shot.resize((1920 // 2, 1080 // 2)).save(crash_fp, format='jpeg', quality=40)
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
                break
            except Exception as e:
                logger.warning(f'send error, error_type={type(e)},\ne={e}', NO_LOG_TIME)
                server.quit()
        except Exception as e:
            logger.warning(f'connect server "{(config.server_host, config.server_port)}" failed,'
                           f' error_type={type(e)},\ne={e}', NO_LOG_TIME)
            logger.info(f'retry sending mail after 5 sec...({retry_time}/5 times)', NO_LOG_TIME)
        time.sleep(5)


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
