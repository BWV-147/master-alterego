__all__ = ['Config', 'config', 'MailLevel']

import ctypes
import json
import os
import sys
import threading
import time
from typing import Optional, List, Tuple, Dict, Set, Mapping

import wda  # noqa


class MailLevel:
    mute = 0
    debug = 1
    info = 2
    warning = 3
    error = 4


class JsonSerializable:
    def __init__(self):
        self._ignored = []

    @staticmethod
    def dump_obj(obj):
        if isinstance(obj, (List, Tuple, Set)):
            return [JsonSerializable.dump_obj(v) for v in obj]
        elif isinstance(obj, Mapping):
            return {k: JsonSerializable.dump_obj(v) for k, v in obj.items()}
        elif isinstance(obj, JsonSerializable):
            return obj.to_json()
        else:
            return obj

    @staticmethod
    def load_obj(data, cls):
        return cls().from_json(data)

    @staticmethod
    def load_obj_list(data: List, cls):
        return [JsonSerializable.load_obj(v, cls) for v in data]

    @staticmethod
    def load_obj_dict(data: dict, cls):
        return {k: JsonSerializable.load_obj(v, cls) for k, v in data.items()}

    def from_json(self, data: dict, drop_unknown=True):
        for k, v in data.items():
            if k in self.__dict__ or drop_unknown is False:
                if isinstance(self.__dict__[k], JsonSerializable):
                    # reset to a fresh instance then update
                    self.__dict__[k] = self.__dict__[k].__class__()
                    self.__dict__[k].from_json(v)
                else:
                    self.__dict__[k] = v
        return self

    def to_json(self, ignore=True):
        out = {}
        for k, v in self.__dict__.items():
            if not ignore or (not k.startswith('_') and k not in self._ignored):
                out[k] = self.dump_obj(v)
        return out


class BaseConfig(JsonSerializable):
    def load(self, fp):
        assert fp is not None, f'please provide filepath of config file.'
        if os.path.exists(fp):
            data: dict = json.load(open(fp, encoding='utf-8'))
            self.from_json(data)
            print(f'loaded config: {fp}')
        else:
            print(f'config file "{fp}" not exists!')
            _dir = os.path.dirname(fp)
            if not os.path.exists(_dir):
                os.makedirs(_dir)
            self.save(fp)
            print(f'Created the default config file "{fp}". Please update it.')

    def save(self, fp):
        assert fp is not None, f'please provide filepath of config file.'
        json.dump(self.to_json(), open(fp, 'w', encoding='utf8'), ensure_ascii=False, indent=2,
                  skipkeys=True)
        return fp


# sub member of Config
class BattleConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.mail = MailLevel.mute
        self.battle_func = None
        self.location = None  # default to (0,0,1920,1080)
        self.num = 1  # max battle num once running, auto decrease
        self.finished = 0  # all finished battles sum, auto increase, don't edit
        self.quartz_eaten = 0  # 突出一个心疼
        # check dropped craft or item.
        # 0-don't check; 1-check 1st drop item; 2-check dropbox(rainbow);
        # 3-check 汉字"所持", rewards.png should not contain craft
        self.check_drop = 1
        self.apples = []  # invalid: stop, 0-rainbow, 1-gold, 2-sliver, 3-cropper, 4-zihuiti, 5-manually(wait ~7min)
        self.end_until_eating_apple = False  # if True, continue battles even finished>=num, be sure the least AP left
        self.jump_battle = False  # goto decoration in Battle.battle_func
        self.login_handler = None  # JP: re-login at 3am(UTC+08)
        self.sell_times = 0  # usually used in hunting event

        self.craft_num = 0
        self.craft_history = {}

        # if craft_num in list, send_mail to remind crafts enhancing, e.g. 5 bonus(self 4 + friend 1).
        # 5 bonus: (7, 8, 11, 12, 15, 16, 20)
        # 6 bonus: (5, 8, 9, 12, 13, 16, 17, 20, 21, 25)
        self.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 20)
        self._ignored = ['login_handler', ]


class LotteryConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.mail = MailLevel.mute
        self.dir = None
        self.location = None  # default to (0,0,1920,1080)
        self.start_func = 'draw'  # draw->clean->sell
        self.num = 10  # lottery num running once, auto decrease
        self.finished = 1  # auto increase， don't edit
        self.clean_num = 100  # < max_num - 10 - retained_num
        self.clean_drag_times = 20  # max drag times during clean mailbox
        self.sell_times = 0  # sell times, if >0, sell. if =0: don't sell. if <0: manual mode
        self.event_banner_no = 0  # values: 0,1,2. Move from shop -> banner list -> event shop


class FpGachaConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.mail = MailLevel.mute
        self.dir = None
        self.location = None
        self.num = 0
        self.finished = 0
        self.sell_times = 10
        self.enhance_times = 100


class Config(BaseConfig):
    def __init__(self, fp=None):
        super().__init__()
        # ================= base config =================
        self.id = None
        self.is_jp = False  # difference between jp and cn server
        self.is_wda = False  # app run in real iOS device and served in macOS
        # Attention: MAIN monitor is not always monitor 1.
        self.monitor = 1  # >=1, check sct.monitors to see monitor info, 0 is all monitors in one screenshot
        self.offset = (0, 0)  # xy offset relative to MAIN monitor's origin for mouse click
        # ================= battle part =================
        self.battle_name = 'default'
        self.battles: Dict[str, BattleConfig] = {'default': BattleConfig()}
        self.lottery = LotteryConfig()
        self.fp_gacha = FpGachaConfig()
        # ================= Other part ==================
        self.wda_settings = {'url': None}  # default url http://localhost:8100 and other options for appium_settings
        self.alert_type = False  # bool: beep, str: ring tone, alert if supervisor found errors or task finish.
        self.manual_operation_time = 60 * 10  # seconds.
        self.www_host_port = None  # default [host='0.0.0.0', port=8080] to run www server. If None, not to run server
        self.need_admin = True
        self.hide_hotkey = ['alt', 'z']  # for MuMu Windows, "alt+z" to hide window. or "alt+x" for new MuMu
        self.switch_tab_hotkey = ['ctrl', 'tab']  # for MuMu Windows
        # ================= Email part ==================
        # make sure the security of password.
        self.mail_receiver = None
        self.mail_sender = None
        self.mail_sender_name = None
        self.mail_password = None
        self.mail_server_host = None
        self.mail_server_port = None

        # ================= ignored =================
        self.mail = MailLevel.mute  # decided by sub-config
        self.fp = fp
        self.T = None
        self.LOC = None
        self.log_time = 0  # record the time of last logging.info/debug..., set NO_LOG_TIME outside battle progress
        self.wda_client: Optional[wda.Client] = None
        # signal = (reason, mail_level), set to default None every time start task/load config
        # the reason will be send in mail after mark_task_finish.
        # if signal is None when thread died: unexpected error
        self.task_finish_signal = None
        self.task_thread: Optional[threading.Thread] = None
        self.new_task_signal = False

        self.temp = {'click_xy': (0, 0)}  # save temp vars at runtime

        self._ignored = ['mail', 'fp', 'T', 'LOC', 'log_time', 'wda_client', 'task_finish_signal',
                         'task_thread', 'new_task_signal', 'temp']
        # load config
        if fp:
            self.load()

    def from_json(self, data: dict, drop_unknown=True):
        self.battles = self.load_obj_dict(data.pop('battles', {}), BattleConfig)
        return super().from_json(data)

    def load(self, fp=None):
        # should only load config at the start of thread,
        # runtime properties are set to default (mainly for interactive console, may load more than once).
        fp = fp or self.fp or 'data/config.json'
        if not os.path.exists(fp) and os.path.exists(f'data/config-{fp}.json'):
            fp = f'data/config-{fp}.json'
        self.fp = fp
        super().load(self.fp)
        # init values after super called
        self.task_finish_signal = None
        self.T = self.LOC = self.task_thread = None
        self.temp.clear()

    def save(self, fp=None):
        fp = fp or self.fp
        return super().save(fp)

    @property
    def battle(self):
        return self.battles[self.battle_name]

    def initialize(self, check_permission=None):
        from init import initialize
        initialize()

        if self.is_wda:
            self.wda_client = wda.Client(self.wda_settings.get('url', None))
            try:
                # quality:
                # 0-max(time is wasted to transfer large image),
                # 1-middle,
                # 2-lowest, may not clear enough
                # once changed the quality value, image templates should be updated
                print(f"window size = {self.wda_client.window_size()}")
                print(f"screenshot size = {self.wda_client.screenshot().size}")
                print(f"scale = {self.wda_client.scale}")
                print(f'WDA connected, current app: {config.wda_client.app_current()["bundleId"]}')
                default_settings = self.wda_client.appium_settings()
                settings = {k: v for k, v in self.wda_settings.items() if k in default_settings}
                if settings:
                    print(f'set WDA: {settings}')
                    print(self.wda_client.appium_settings(settings))
            except Exception as e:
                print(f'Error:\n {e}')
                raise EnvironmentError(f'WebDriverAgent is not configured properly!')
        elif sys.platform == 'win32':
            # Android/iOS emulator in Windows
            # check admin permission & set process dpi awareness
            # please run cmd/powershell or Pycharm as administrator.
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                if check_permission:
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
                  'confirm these two permissions are granted:\n'
                  '   "Accessibility" and "Screen Recording" inside "System Preferences/Security & Privacy/"\n',
                  file=sys.stderr)

    def count_lottery(self):
        self.lottery.finished += 1
        self.lottery.num -= 1
        self.save()

    def count_fp_gacha(self):
        self.fp_gacha.finished += 1
        self.fp_gacha.num -= 1
        self.save()

    def count_battle(self):
        self.battle.finished += 1
        self.battle.num -= 1
        self.save()

    def record_craft_drop(self):
        self.battle.craft_num += 1
        self.battle.craft_history[str(self.battle.craft_num)] = self.battle.finished
        self.save()

    def update_time(self, dt: float = 0):
        self.log_time = time.time() + dt

    def get_dt(self):
        return time.time() - self.log_time

    def mark_task_finish(self, msg=None, level=MailLevel.info):
        from .log import logger
        if msg is None:
            import traceback
            stack = ''.join(traceback.format_stack(limit=4))
            logger.info('Mark finished without message, traceback stack:\n' + stack)
            msg = 'Finished: unknown reason.'

        if level >= MailLevel.warning:
            logger.warning(msg)
        else:
            logger.info(msg)
        self.task_finish_signal = (msg, level)
        self.save()
        self.kill()

    def kill(self):
        """
        If program run in multi-threading, supervisor or child thread call this to kill child thread.\n
        But if run in single-threading(no supervisor thus running_thread is None), just kill MainThread self.

        Ke
        """
        from .addon import kill_thread
        thread = self.task_thread or threading.current_thread()
        if thread is not threading.main_thread():
            kill_thread(thread)


config = Config()
