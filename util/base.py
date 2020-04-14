import argparse
import smtplib
import socket
import threading
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
# noinspection PyUnresolvedReferences
from typing import List, Tuple, Union, Dict, Callable, Sequence, Optional

import numpy

from util.log import *


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
    # check email params
    if receiver is None:
        receiver = config.receiver
    if None in (receiver, config.sender, config.password):
        logger.warning(f'Incomplete email config:\n'
                       f'======== Incomplete Email Settings ========\n'
                       f' - receiver: {receiver}\n'
                       f' - sender  : {config.sender}\n'
                       f' - password:{"*****" if config.password else "None"}\n'
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
    body = f'<b>{body}</b><br><br>\n' \
           f'<hr><b>Computer name:</b><br>{socket.getfqdn(socket.gethostname())}<br>\n'

    # body.screenshot
    crash_fp = 'img/crash.jpg'
    if attach_shot:
        body += '<hr><b>Screenshot before shutdown</b>:<br>\n' \
                '<img src="cid:screenshot" style="width: 100%; max-width: 720px;"><br>\n'
        shot = screenshot()
        shot.save(crash_fp + '.png')  # save a backup of origin screenshot
        # shrink the image/email size
        shot.resize((numpy.array(shot.size) / 1.5).astype('int')).save(crash_fp, format='jpeg', quality=40)
        with open(crash_fp, 'rb') as fd:
            image = MIMEImage(fd.read())
            image.add_header('Content-ID', '<screenshot>')
            mail.attach(image)

    # body.recent_log
    if config.log_file and os.path.exists(config.log_file):
        with open(config.log_file, encoding='utf8') as fd:
            lines = fd.readlines()
            n = len(lines)
            recent_records = ['<p>' + x.rstrip() + '</p>\n' for x in lines[-min(10, n):]]
            body += f'<hr><b>Recent 10 logs ({config.log_file}):</b><br>\n' \
                    '<style>.logs { font-family: "Consolas" } .logs p { margin: 0.3em auto; }</style>\n' \
                    f'<span class="logs">\n{"".join(recent_records)}</span>'

    print(f'Ready to send email:\n'
          f'=============== Email ===============\n'
          f' - Subject  : {subject}\n'
          f' - Receiver : {receiver}\n'
          f' - Body html:\n{body}\n'
          f'================ End ================\n')

    # make email
    mail['Subject'] = subject
    mail['From'] = formataddr((config.sender_name, config.sender))
    mail['To'] = receiver
    mail.attach(MIMEText(body, 'html', 'utf-8'))

    # send email, retry 5 times at most if failed.
    retry_time = 0
    while retry_time < 5:
        retry_time += 1
        try:
            server = smtplib.SMTP_SSL(config.server_host, config.server_port)
            # server.set_debuglevel(1)
            try:
                server.login(config.sender, config.password)
                result = server.sendmail(config.sender, receiver, mail.as_string())
                if result == {}:
                    logger.warning(f'send email success.')
                else:
                    logger.warning(f'send email failed! Error:\n{result}')
                server.quit()
                break
            except Exception:
                server.quit()
                raise
        except Exception as e:
            logger.warning(f'Error when sending email: {type(e)}\n{e}')
            logger.info(f'retry sending mail in 5 seconds... ({retry_time}/5 times)')
            time.sleep(5)


class Timer:
    def __init__(self):
        self.t0 = time.time()

    def lapse(self, save=True):
        t1 = time.time()
        dt = t1 - self.t0
        if save:
            self.t0 = t1
        return dt
