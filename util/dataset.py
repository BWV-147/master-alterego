"""Data definition, constants
Coordination: using PIL coordination, (x,y), (left,top,right,bottom), e.g. (0,0,1920-1,1080-1)
"""
import json

from PIL import Image

from util.base import *

THR = 0.85  # default threshold


# database: regions & saved screenshot
class Regions:
    """
    Store region(length 4) or point(length 2) data at default screensize 1920*1080.
    Properties could be a region/point or a list(1 or multi dimension) of regions/points
    """
    # common, or for supervisor
    net_error = ((599, 814, 720, 872), (1138, 813, 1378, 876))
    safe_area = (1400, 40)

    # --- gacha part ----
    # in gacha
    gacha_point = (600, 622)
    gacha_logo = (78, 222, 191, 315)
    gacha_tab = (1009, 188, 1213, 228)
    gacha_10_initial = (483, 630, 800, 774)
    gacha_reset_action = (1546, 337, 1863, 394)
    gacha_reset_confirm = (1097, 813, 1416, 879)
    gacha_reset_finish = (800, 811, 1113, 878)
    gacha_empty = (285, 631, 524, 780)  # used when no ticket left
    # move to mailbox
    box_full_confirm = (1112, 822, 1463, 873)

    # in mailbox
    box_back = (49, 34, 242, 100)
    box_get_action = (1509, 535, 1810, 582)
    box_get_all_action = (1524, 302, 1805, 354)  # WARNING: don't click
    # box_items = [(1272, 400), (1272, 600), (1272, 800), (1272, 980)]
    box_items = [(1231, 365, 1314, 447), (1231, 558, 1314, 640), (1231, 751, 1314, 833), (1231, 944, 1314, 1026)]
    box_check_column = (1231, 264, 1314, 1079)
    box_drag_start = (1070, 914)
    box_drag_end = (1070, 84)
    box_history = (365, 30, 522, 102)
    # from mailbox move to bag/enhancement
    bag_full_sell_action = (900, 810, 1020, 870)
    bag_full_enhance_action = (887, 660, 1029, 718)

    # in bag
    bag_back = (49, 34, 242, 100)
    bag_select_start = (200, 350)
    bag_select_end = (1416, 1050)
    bag_sell_action = (1600, 975, 1870, 1047)
    bag_sell_confirm = (1200, 849, 1317, 908)
    bag_sell_finish = (910, 850, 1015, 905)

    # from bag to drawer
    shop_sell = (1352, 465, 1723, 552)
    rewards_action = (1688, 29, 1872, 97)

    # ------- battle part -------
    apply_friend = (1692, 521, 1826, 588)
    apply_friend_deny = (464, 913)
    quest = (966, 256, 1149, 417)  # (937, 240, 1848, 360)
    quest_outer = (966, 246, 1149, 427)
    quest_c = (1600, 265)
    # rewards = (1680, 33, 1868, 91)

    ap_time = (346, 1041, 366, 1072)
    apple_page = (471, 177, 645, 359)
    apple_close = (1000, 925)
    apples = ((471, 177, 645, 359), (471, 397, 645, 579), (474, 621, 645, 803), (471, 840, 645, 861))
    apple_confirm = (1195, 802, 1313, 882)
    # support = ((72,489,1617,560), (72,790,1617,860))
    # 2 supports one time，support[svt][skill]
    support_team_icon = (1637, 320, 1767, 384)
    support_ce = ((72, 489, 316, 537), (72, 791, 316, 838))  # 礼装位置
    support_ce_max = ((273, 524, 303, 552), (273, 825, 303, 854))  # 礼装满破的星星
    support_skill = ((1252, 463, 1577, 548), (1252, 764, 1577, 847))  # 技能整体外轮廓
    support_skills = [[(1260, 468, 1334, 544), (1380, 468, 1454, 544), (1500, 468, 1574, 544), ],
                      [(1260, 768, 1334, 844), (1380, 768, 1454, 844), (1500, 768, 1574, 844)]]  # 3个技能外轮廓
    support_skill_lvs = [[(1260, 511, 1300, 544), (1380, 511, 1420, 544), (1500, 511, 1540, 544)],
                         [(1260, 811, 1334, 844), (1380, 811, 1454, 844), (1500, 811, 1574, 844)]]  # 3个lv, 强化箭头未比较

    support_confirm_title = (821, 171, 1108, 230)
    support_refresh_confirm = (1110, 890)
    support_refresh = (1238, 160, 1318, 230)
    support_scroll = ((1860, 520), (1860, 640), (760, 880))

    team = (1655, 973, 1902, 1052)
    team_cloth = (20, 980, 263, 1054)
    wave = (1261, 78, 1281, 106)
    enemies_all = (0, 0, 1080, 128)
    enemies = ((0, 0, 120, 130), (360, 0, 480, 130), (720, 0, 840, 130))  # skill_to_enemies

    skills = [
        [(61, 823, 121, 908), (202, 823, 262, 908), (343, 823, 403, 908)],
        [(539, 823, 599, 908), (680, 823, 740, 908), (821, 823, 881, 908)],
        [(1017, 823, 1077, 908), (1158, 823, 1218, 908), (1299, 823, 1359, 908)]
    ]
    skill_target_X = (430, 600, 580, 750)  # 第一个人
    skill_to_target = ((490, 700), (970, 700), (1429, 700))
    master_skill = (1736, 440, 1841, 507)
    master_skills = ((1319, 427, 1404, 512), (1450, 427, 1535, 512), (1581, 427, 1666, 512))

    attack = (1554, 950, 1624, 1000)  # attack 字样以下部分，与大小变化的attack独立
    cards_back = (1725, 1007, 1878, 1043)
    cards = (
        (84, 655, 303, 903), (466, 655, 685, 903), (848, 655, 1067, 903), (1235, 655, 1454, 903),
        (1624, 655, 1843, 903),
        (529, 204, 707, 441), (848, 204, 1026, 441), (1167, 204, 1345, 441))
    cards_outer = ((84, 500, 303, 1000), (466, 500, 685, 1000), (848, 500, 1067, 1000), (1235, 500, 1454, 1000),
                   (1624, 500, 1843, 1000),
                   (529, 100, 707, 510), (848, 100, 1026, 510), (1167, 100, 1345, 510))
    # cards_outer = ((0, 500, 386, 1000), (386, 500, 784, 1000), (784, 500, 1170, 1000), (1170, 500, 1552, 1000),
    #                (1552, 500, 1920, 1000),
    #                (428, 100, 812, 510), (812, 100, 1170, 510), (1170, 100, 1554, 510))

    order_change = (
        (87, 403, 322, 643), (387, 403, 622, 643), (687, 403, 922, 643), (987, 403, 1222, 643), (1287, 403, 1522, 643),
        (1587, 403, 1822, 643))
    order_change_confirm = (739, 907, 1167, 974)  # length 6

    kizuna = (115, 251, 580, 305)
    finish_qp = (418, 884, 487, 955)
    rewards_show_num = (1593, 115, 1718, 149)
    finish_next = (1444, 980, 1862, 1061)
    finish_craft = (454, 216, 623, 386)
    restart_quest_yes = (1122, 812, 1386, 829)
    friend_point = (460, 810, 580, 880)

    size = (0, 0, 1920, 1080)

    def relocate(self, region=(0, 0, 1920, 1080)):
        """
        Recursively resize regions. The default size is 1920*1080
        :param region: 4 length tuple - new region for resize, e.g. (100,100,1800,1000).
        :return: None.
        """
        assert len(region) == 4, region
        for key, value in Regions.__dict__.items():
            # at most 3 layers
            if not key.startswith('__') and isinstance(value, (int, list, tuple)):
                # print(key, value)
                self.__dict__[key] = Regions.loop(value, region, Regions.size)

    @staticmethod
    def loop(pt, new, old):
        if isinstance(pt, (tuple, list)):
            if isinstance(pt[0], int):
                assert len(pt) % 2 == 0, pt
                oo = []
                for i, v in enumerate(pt):
                    ii = i % 2
                    oo.append(int(
                        (v - old[ii]) / (old[2 + ii] - old[ii]) * (new[2 + ii] - new[ii]) + new[ii]
                    ))
                    # oo.append(int(region[ii] + (region[ii + 2] - region[ii]) / origin[ii] * o[i]))
                return oo
            else:
                return [Regions.loop(k, new, old) for k in pt]
        else:
            print(f'skip key(type:{type(pt)}) for resize')


class ImageTemplates:
    directory: str
    templates: Dict[str, Image.Image]

    def __init__(self, directory: str = None):
        self.directory = directory
        self.templates = {}
        if directory is not None:
            self.read_templates(directory)

    def read_templates(self, directory: str, force=False):
        old_templs = self.templates
        self.templates = {}
        for filename in os.listdir(directory):
            if not filename.endswith('.png'):
                continue
            filepath = os.path.join(directory, filename)
            key = filename[0:len(filename) - 4]
            if directory == self.directory and force is False and key in old_templs:
                self.templates[key] = old_templs[key]
            else:
                self.templates[key] = Image.open(filepath)
        self.directory = directory

    def get(self, attr):
        # type:(Union[str, Sequence[str]])-> Union[Image.Image, Sequence[Image.Image], Dict[str, Image.Image]]
        if attr is None:
            return self.templates.copy()
        elif isinstance(attr, (list, tuple)):
            return [self.templates[k] for k in attr]
        elif attr in self.templates:
            return self.templates[attr]
        else:
            raise KeyError(f'Templates has no key "{attr}"')

    def __repr__(self):
        return f'{self.__class__.__name__}(dir="{self.directory}", templates={self.templates})'

    @property
    def apple_confirm(self):
        return self.get('apple_confirm')

    @property
    def net_error(self):
        return self.get('net_error')

    @property
    def apple_page(self):
        return self.get('apple_page')

    @property
    def apply_friend(self):
        return self.get('apply_friend')

    @property
    def cards(self):
        templs = []
        for i in range(20):
            key = f'cards{i + 1}'
            if key in self.templates:
                templs.append(self.templates[key])
            else:
                break
        return templs

    @property
    def cards1(self):
        return self.get('cards1')

    @property
    def cards2(self):
        return self.get('cards2')

    @property
    def cards3(self):
        return self.get('cards3')

    @property
    def cards4(self):
        return self.get('cards4')

    @property
    def friend_point(self):
        return self.get('friend_point')

    @property
    def rewards(self):
        return self.get('rewards')

    @property
    def kizuna(self):
        return self.get('kizuna')

    @property
    def order_change(self):
        return self.get('order_change')

    @property
    def quest(self):
        return self.get('quest')

    @property
    def team(self):
        return self.get('team')

    @property
    def restart_quest(self):
        return self.get('restart_quest')

    @property
    def support(self):
        return self.get('support')

    @property
    def support_confirm(self):
        return self.get('support_confirm')

    @property
    def wave1a(self):
        return self.get('wave1a')

    @property
    def wave1b(self):
        return self.get('wave1b')

    @property
    def wave2a(self):
        return self.get('wave2a')

    @property
    def wave2b(self):
        return self.get('wave2b')

    @property
    def wave3a(self):
        return self.get('wave3a')

    @property
    def wave3b(self):
        return self.get('wave3b')

    # gacha
    @property
    def gacha_initial(self):
        return self.get('gacha_initial')

    @property
    def gacha_empty(self):
        return self.get('gacha_empty')

    @property
    def gacha_reset_confirm(self):
        return self.get('gacha_reset_confirm')

    @property
    def gacha_reset_finish(self):
        return self.get('gacha_reset_finish')

    @property
    def box_full_alert(self):
        return self.get('box_full_alert')

    @property
    def box_selected(self):
        return self.get('box_selected')

    @property
    def box_unselected(self):
        return self.get('box_unselected')

    @property
    def bag_full_alert(self):
        return self.get('bag_full_alert')

    @property
    def bag_unselected(self):
        return self.get('bag_unselected')

    @property
    def bag_selected(self):
        return self.get('bag_selected')

    @property
    def bag_sell_confirm(self):
        return self.get('bag_sell_confirm')

    @property
    def bag_sell_finish(self):
        return self.get('bag_sell_finish')

    @property
    def shop(self):
        return self.get('shop')


class StatInfo:

    def __init__(self, fp: str = None):
        self.fp = fp if fp is not None else 'record.json'
        self.craft_num = 0
        self.battle_num = 0
        self.history = []
        self.durations = []
        self.load()

    def add_battle(self, craft_dropped: bool = False):
        self.battle_num += 1
        # self.durations.append((self.battle_no, duration))
        if craft_dropped:
            self.craft_num += 1
            self.history.append((self.craft_num, self.battle_num))
        self.save()

    def save(self):
        directory, filename = os.path.split(self.fp)
        if filename == '':
            print(f'invalid filename{self.fp}')
        if directory != '' and not os.path.exists(directory):
            os.makedirs(directory)
        json.dump(self, open(self.fp, 'w'), indent=2, default=lambda x: x.__dict__)

    def load(self):
        if os.path.exists(self.fp):
            data = json.load(open(self.fp, 'r'))
            self.craft_num = data.get('craft_num', 0)
            self.battle_num = data.get('battle_num', 0)
            self.history = data.get('history', [])
            self.durations = data.get('durations', [])
        else:
            print(f'StatInfo file {self.fp}  not exist, skip loading')

    def __repr__(self):
        data = json.dumps(self, ensure_ascii=False, default=lambda x: x.__dict__)
        return f'{self.__class__.__name__}() {data}'


# %% local test functions
def __gen_getter(path='./'):
    """
    generate getters for _ImageTemplates
    """
    methods = []

    for filename in os.listdir(path):
        if filename.endswith('.png'):
            name = filename[0:-4]
            s = f'''
    @property
    def {name}(self):
        return self.get('{name}')
        '''
            methods.append(s)
    print('-------generate _ImageTemplates getters------')
    print('\n'.join(methods))
    print('-------end generation------')
