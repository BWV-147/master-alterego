import json
import os


class Config:
    def __init__(self):
        # base config
        self.id = None
        self.monitor = 1  # >=1, check sct.monitors to see running at which monitor, 0 is total size
        self.offset_x = 0  # xy offset for mouse click event, relative to MAIN monitor's origin
        self.offset_y = 0
        self.log_time = 0  # record the time of last logging.info/debug..., set NO_LOG_TIME outside battle progress
        self.task_finished = False  # all battles finished, set to True before child process exist.
        self.check_drop = True  # check craft dropped or not, if True, make sure rewards.png contains the dropped craft.
        self.log_file = None

        # battle specific
        self.battle_num = 1  # auto decrease
        self.apple = -1
        # if crash_num in list, send_mail to remind crafts enhancing, default 5 bonus(self 4 + friend 1)
        # 5 bonus: (7, 8, 11, 12, 15, 16, 20)
        # 6 bonus: (5, 8, 9, 12, 13, 16, 17, 20, 21, 25)
        self.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 20)
        self.jump_battle = False  # goto decoration in Battle.battle_func
        self.jump_start = False  # goto decoration in Battle.start
        self.img_net = None  # img & loc of network error, especially for jp server.
        self.loc_net = None  # TODO: this two params should not be stored

        # gacha specific
        self.gacha_num = 1  # auto decrease
        self.mailbox_clean_num = 100  # < max_num - 10 - retained_num
        self.event_banner_no = 0  # values: 0,1,2

        # private data.
        self.receiver = None
        self.sender = None
        self.sender_name = None
        self.password = None
        self.server_host = None
        self.server_port = None

    def load_config(self, fp='config.json'):
        if os.path.exists(fp):
            data: dict = json.load(open(fp, encoding='utf-8'))
            for k, v in data.items():
                self.__dict__[k] = v
        else:
            print(f'config file "{fp}" not exists!')
            self.save(fp)
            print(f'Created the empty config file "{fp}". Please fill out it.')

    def save(self, fp='config.json'):
        json.dump(self.__dict__, open(fp, 'w', encoding='utf8'), ensure_ascii=False, indent=2, skipkeys=True,
                  default=lambda o: None)

    def count_gacha(self):
        self.gacha_num -= 1
        self.save()

    def count_battle(self):
        self.battle_num -= 1
        self.save()


CONFIG = Config()
