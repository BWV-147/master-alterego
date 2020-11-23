__all__ = ['Config', 'config']

import json
import os
import threading
import time
from queue import Queue
from typing import Optional, List, Tuple, Dict, Set, Mapping

import wda  # noqa


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


class Config(BaseConfig):
    def __init__(self, fp=None):
        super().__init__()
        # ================= sys config =================
        self.id = None
        self.is_jp = False  # difference between jp and cn server
        self.is_wda = False  # app run in real iOS device and served in macOS
        self.wda_settings = {'url': None}  # default url http://localhost:8100 and other options for appium_settings
        # Attention: MAIN monitor is not always monitor 1.
        self.monitor = 1  # >=1, check sct.monitors to see monitor info, 0 is all monitors in one screenshot
        self.offset = (0, 0)  # xy offset relative to MAIN monitor's origin for mouse click
        self.alert_type = False  # bool: beep, str: ring tone, alert if supervisor found errors or task finish.
        self.manual_operation_time = 60 * 10  # seconds.
        self.www_host_port = None  # default [host='0.0.0.0', port=8080] to run www server. If None, not to run server
        self.need_admin = True
        self.hide_hotkey = ['alt', 'z']  # for MuMu Windows, "alt+z" to hide window. or "alt+x" for new MuMu
        self.switch_tab_hotkey = ['ctrl', 'tab']  # for MuMu Windows
        # ================= battle part =================
        self.battle_name = 'default'
        self.battles: Dict[str, BattleConfig] = {'default': BattleConfig()}
        self.lottery = LotteryConfig()
        self.fp_gacha = FpGachaConfig()
        # ================= Email part ==================
        # make sure the security of password.
        self.mail_receiver = None
        self.mail_sender = None
        self.mail_sender_name = None
        self.mail_password = None
        self.mail_server_host = None
        self.mail_server_port = None

        # ================= ignored =================
        self.mail = False  # decided by sub-config
        self.fp = fp
        self.T = None
        self.LOC = None
        self.log_time = 0  # record the time of last logging.info/debug..., set NO_LOG_TIME outside battle progress
        self.wda_client: Optional[wda.Client] = None
        self.task_finished = False  # all battles finished, set to True before child process exist.
        self.task_thread: Optional[threading.Thread] = None
        self.task_queue = Queue(1)
        self.temp = {}  # save temp vars at runtime

        self._ignored = ['mail', 'fp', 'T', 'LOC', 'log_time', 'wda_client', 'task_finished', 'task_thread',
                         'task_queue', 'temp']
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
        self.task_finished = False
        self.T = self.LOC = self.task_thread = None
        self.temp.clear()
        return super().load(self.fp)

    def save(self, fp=None):
        fp = fp or self.fp
        return super().save(fp)

    @property
    def battle(self):
        return self.battles[self.battle_name]

    def init_wda(self):
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

    def count_lottery(self):
        self.lottery.finished += 1
        self.lottery.num -= 1
        self.save()

    def count_fp_gacha(self):
        self.fp_gacha.finished += 1
        self.fp_gacha.num -= 1
        self.save()

    def count_battle(self, craft_dropped=False):
        self.battle.finished += 1
        self.battle.num -= 1
        if craft_dropped:
            self.battle.craft_num += 1
            self.battle.craft_history[str(self.battle.craft_num)] = self.battle.finished
        self.save()

    def update_time(self, dt: float = 0):
        self.log_time = time.time() + dt

    def get_dt(self):
        return time.time() - self.log_time

    def mark_task_finish(self):
        self.save()
        self.task_finished = True

    def kill(self):
        """
        If program run in multi-threading, supervisor or child thread call this to kill child thread.\n
        But if run in single-threading(no supervisor thus running_thread is None), just kill MainThread self.

        Ke
        """
        from .addon import kill_thread
        kill_thread(self.task_thread or threading.current_thread())


# sub member of Config
class BattleConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.mail = False
        self.battle_func = None
        self.num = 1  # max battle num once running, auto decrease
        self.finished = 0  # all finished battles sum, auto increase, don't edit
        self.check_drop = 1  # check dropped craft or item. 0-not check; 1-check 1st drop item; 2-check dropbox(rainbow)
        self.apples = []  # invalid: stop, 0-rainbow, 1-gold, 2-sliver, 3-cropper, 4-zihuiti, 5-manually(wait ~7min)
        self.end_until_eating_apple = False  # if True, continue battles even finished>=num, be sure the least AP left
        self.jump_battle = False  # goto decoration in Battle.battle_func
        self.login_handler = None  # JP: re-login at 3am(UTC+08)
        self.sell_num = 0  # usually used in hunting event

        self.craft_num = 0
        self.craft_history = {}

        # if crash_num in list, send_mail to remind crafts enhancing, e.g. 5 bonus(self 4 + friend 1).
        # 5 bonus: (7, 8, 11, 12, 15, 16, 20)
        # 6 bonus: (5, 8, 9, 12, 13, 16, 17, 20, 21, 25)
        self.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 20)
        self._ignored = ['login_handler', ]


class LotteryConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.mail = False
        self.dir = None
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
        self.mail = False
        self.dir = None
        self.num = 0
        self.finished = 0
        self.sell_num = 10
        self.enhance_num = 100


config = Config()
