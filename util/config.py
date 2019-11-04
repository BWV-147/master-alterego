import json
import os


class Config:
    # TODO: save all config params into json file
    def __init__(self, fp='user.json'):
        self.monitor = 1  # >=1, check sct.monitors to see running at which monitor, 0 is total size
        self.offset_x = 0  # xy offset for mouse click event, relative to MAIN monitor's origin
        self.offset_y = 0
        self.check_drop = True  # check craft dropped or not, if True, make sure rewards.png contains the dropped craft.
        # if crash_num in list, send_mail to remind crafts enhancing, default 5 bonus(self 4 + friend 1)
        # 5 bonus: (7, 8, 11, 12, 15, 16, 19, 20)
        # 6 bonus: (5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25)
        self.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 19, 20)
        self.jump_battle = False  # goto decoration in Battle.battle_func
        self.jump_start = False  # goto decoration in Battle.start
        self.log_time = 0  # record the time of last logging.info/debug..., set NO_LOG_TIME outside battle progress
        self.task_finished = False  # all battles finished, set to True before child process exist.
        self.img_net = None  # img & loc of network error, especially for jp server.
        self.loc_net = None

        # private data saved in user.json: email account, e.g.
        self.user = UserData(fp)


class UserData:
    def __init__(self, fp='user.json'):
        self.id = None
        self.receiver = None
        self.sender = None
        self.sender_name = None
        self.password = None
        self.server_host = None
        self.server_port = None
        self.load_config(fp)

    def load_config(self, fp='user.json'):
        if os.path.exists(fp):
            data: dict = json.load(open(fp, encoding='utf-8'))
            for k, v in data.items():
                self.__dict__[k] = v
        else:
            print(f'config file "{fp}" not exists!')
            json.dump(self.__dict__, open(fp, encoding='utf8'), ensure_ascii=False, indent=2)
            print(f'Created the empty config file "{fp}". Please fill out it.')


CONFIG = Config()
