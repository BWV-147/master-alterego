import json
import os


class BaseConfig:
    img_net = None  # class vars won't be saved
    loc_net = None
    log_time = 0  # record the time of last logging.info/debug..., set NO_LOG_TIME outside battle progress
    task_finished = False  # all battles finished, set to True before child process exist.
    log_file = None  # filename of logger when send_mail review the recent logs
    temp = {}  # save temp vars at runtime

    def __init__(self, fp=None):
        self.fp = fp
        # sys config
        self.id = None
        self.monitor = 1  # >=1, check mss().monitors to see monitor info, 0 is total size
        self.offset_x = 0  # xy offset for mouse click event, relative to MAIN monitor's origin
        self.offset_y = 0
        self.mail = False  # whether to send_mail
        self.alert = False  # bool: beep, str: ring tone, alert if supervisor found errors or task finish.

        # ================= battle part =================
        # battle params
        self.battle_func = None
        self.battle_num = 1  # max battle num once running, auto decrease
        self.finished_battles = 0  # all finished battles sum, auto increase, don't edit
        self.max_finished_battles = 1000  # stop if finished_battles >= max_finished_battles
        self.check_drop = True  # check craft dropped or not, if True, make sure rewards.png contains the dropped craft.
        self.apples = []  # invalid: stop, 0-colorful, 1-gold, 2-sliver, 3-cropper
        self.jump_battle = False  # goto decoration in Battle.battle_func
        self.jump_start = False  # goto decoration in Battle.start
        self.stop_around_3am = True  # JP: re-login at 3am(UTC+08)

        self.craft_num = 0
        self.craft_history = {}

        # if crash_num in list, send_mail to remind crafts enhancing, e.g. 5 bonus(self 4 + friend 1).
        # 5 bonus: (7, 8, 11, 12, 15, 16, 20)
        # 6 bonus: (5, 8, 9, 12, 13, 16, 17, 20, 21, 25)
        self.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 20)

        # ================= gacha part =================
        self.gacha_dir = None
        self.gacha_start_func = 'draw'  # draw->clean->sell
        self.gacha_num = 10  # gacha num running once, auto decrease
        self.total_gacha_num = 1  # auto increase， don't edit
        self.clean_num = 100  # < max_num - 10 - retained_num
        self.clean_drag_times = 20  # max drag times during clean mailbox
        self.sell_times = 0  # sell times, if >0, sell. if =0: don't sell. if <0: manual mode
        self.event_banner_no = 0  # values: 0,1,2. Move from shop -> banner list -> event shop

        # ================= Email part =================
        # make sure the security of password.
        self.receiver = None
        self.sender = None
        self.sender_name = None
        self.password = None
        self.server_host = None
        self.server_port = None

        # load config
        if fp:
            self.load_config()

    def load_config(self, fp=None):
        self.fp = fp = fp or self.fp or 'config.json'
        if os.path.exists(fp):
            data: dict = json.load(open(fp, encoding='utf-8'))
            for k, v in data.items():
                if k in self.__dict__:
                    self.__dict__[k] = v
            print(f'loaded config: {fp}')
        else:
            print(f'config file "{fp}" not exists!')
            self.save(fp)
            print(f'Created the default config file "{fp}". Please check it.')

    def save(self, fp=None):
        fp = fp or self.fp
        if not fp:
            print(f'please provide valid filename: {fp}')
            return
        out = {}
        for k, v in self.__dict__.items():
            if k not in ['fp', ]:
                out[k] = v
        json.dump(out, open(fp or self.fp, 'w', encoding='utf8'), ensure_ascii=False, indent=2,
                  skipkeys=True, default=lambda o: None)

    def count_gacha(self):
        self.total_gacha_num += 1
        self.gacha_num -= 1
        self.save()

    def count_battle(self, craft_dropped=False):
        self.battle_num -= 1
        self.finished_battles += 1
        if craft_dropped:
            self.craft_num += 1
            self.craft_history[str(self.craft_num)] = self.finished_battles
        self.save()


config = BaseConfig()
