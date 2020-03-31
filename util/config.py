import json
import os


class _BaseConfig:
    def __init__(self):
        self._ignored = []

    def from_json(self, data):
        for k, v in data.items():
            if k in self.__dict__:
                if isinstance(self.__dict__[k], _BaseConfig):
                    self.__dict__[k].from_json(v)
                else:
                    self.__dict__[k] = v

    def to_json(self):
        out = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_') and k not in self._ignored:
                if isinstance(v, _BaseConfig):
                    out[k] = v.to_json()
                else:
                    out[k] = v
        return out

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
                  skipkeys=True, default=lambda o: o.__dict__)


class Config(_BaseConfig):

    def __init__(self, fp=None):
        super().__init__()
        # ================= sys config =================
        self.id = None
        self.is_jp = False  # difference between jp and cn server
        self.monitor = 1  # >=1, check mss().monitors to see monitor info, 0 is total size
        self.offset = (0, 0)  # xy offset for mouse click event, relative to MAIN monitor's origin
        self.mail = False  # whether to send_mail
        self.alert_type = False  # bool: beep, str: ring tone, alert if supervisor found errors or task finish.
        self.manual_operation_time = 60 * 10  # seconds.

        # ================= battle part =================
        self.battle = BattleConfig()
        self.gacha = GachaConfig()
        self.fp_gacha = FpGachaConfig()
        # ================= Email part ==================
        # make sure the security of password.
        self.receiver = None
        self.sender = None
        self.sender_name = None
        self.password = None
        self.server_host = None
        self.server_port = None

        # ================= ignored =================
        self.fp = fp
        self.T = None
        self.LOC = None
        self.log_time = 0  # record the time of last logging.info/debug..., set NO_LOG_TIME outside battle progress
        self.task_finished = False  # all battles finished, set to True before child process exist.
        self.log_file = None  # filename of logger when send_mail review the recent logs
        self.running_thread = None
        self.temp = {}  # save temp vars at runtime

        self._ignored = ['fp', 'T', 'LOC', 'log_time', 'task_finished', 'log_file', 'running_thread', 'temp']
        # load config
        if fp:
            self.load()

    def load(self, fp=None):
        self.fp = fp or self.fp or 'data/config.json'
        return super().load(self.fp)

    def save(self, fp=None):
        fp = fp or self.fp
        return super().save(fp)

    def count_gacha(self):
        self.gacha.finished += 1
        self.gacha.num -= 1
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

    def mark_task_finish(self, kill=True):
        import time
        from util.supervisor import kill_thread
        import threading
        self.task_finished = True
        self.save()
        time.sleep(5)
        if kill:
            kill_thread(threading.current_thread())


# sub member of Config
class BattleConfig(_BaseConfig):
    def __init__(self):
        super().__init__()
        self.battle_func = None
        self.num = 1  # max battle num once running, auto decrease
        self.finished = 0  # all finished battles sum, auto increase, don't edit
        self.check_drop = True  # check craft dropped or not, if True, make sure rewards.png contains the dropped craft.
        self.apples = []  # invalid: stop, 0-colorful, 1-gold, 2-sliver, 3-cropper
        self.jump_battle = False  # goto decoration in Battle.battle_func
        self.jump_start = False  # goto decoration in Battle.start
        self.login_handler = None  # JP: re-login at 3am(UTC+08)
        self.sell_when_battle = 0  # usually used in hunting event

        self.craft_num = 0
        self.craft_history = {}

        # if crash_num in list, send_mail to remind crafts enhancing, e.g. 5 bonus(self 4 + friend 1).
        # 5 bonus: (7, 8, 11, 12, 15, 16, 20)
        # 6 bonus: (5, 8, 9, 12, 13, 16, 17, 20, 21, 25)
        self.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 20)


class GachaConfig(_BaseConfig):
    def __init__(self):
        super().__init__()
        self.dir = None
        self.start_func = 'draw'  # draw->clean->sell
        self.num = 10  # gacha num running once, auto decrease
        self.finished = 1  # auto increase， don't edit
        self.clean_num = 100  # < max_num - 10 - retained_num
        self.clean_drag_times = 20  # max drag times during clean mailbox
        self.sell_times = 0  # sell times, if >0, sell. if =0: don't sell. if <0: manual mode
        self.event_banner_no = 0  # values: 0,1,2. Move from shop -> banner list -> event shop


class FpGachaConfig(_BaseConfig):
    def __init__(self):
        super().__init__()
        self.dir = None
        self.num = 0
        self.finished = 0


config = Config()
