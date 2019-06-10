# Coordination: (x,y), (0,0,1920,1080)
import os
import random
import time
import ctypes
import win32api
import win32con
from PIL import Image
from typing import List, Tuple, Union, Dict
import logging
from PIL.PngImagePlugin import PngImageFile

THR = 0.9  # default threshold


# logger
def get_logger(name='log', level=logging.INFO):
    _logger = logging.getLogger(name)
    fh = logging.FileHandler('log/%s.log' % name)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'))
    fh.setLevel(level)
    _logger.addHandler(fh)
    return _logger


# win32: mouse & screen pixel
def move_mouse(x=None, y=None):
    x = int(x)
    y = int(y)
    # logger.debug('mouse move:',x,'-',y)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)


def click(xy: tuple = None, lapse=0.5, r=2):
    """
    click at point (x,y) or region center (x1,y1,x2,y2) within a random offset between 0~r
    :param xy:
    :param lapse:
    :param r:
    :return:
    """
    if xy is not None:
        if 2 == len(xy):
            x, y = xy[:]
        elif 4 == len(xy):
            x, y = ((xy[0] + xy[2]) / 2, (xy[1] + xy[3]) / 2)
        else:
            raise ValueError('len(xy) should be 2 or 4.')
        x += random.randint(-r, r)
        y += random.randint(-r, r)
        move_mouse(x, y)
        # m.click(x, y)
        # logger.debug('click (%d, %d)' % (x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(lapse)


def get_pixel(xy):
    # RGB
    color = ctypes.windll.gdi32.GetPixel(ctypes.windll.user32.GetDC(None), xy[0], xy[1])
    logger.debug(hex(color))
    logger.debug((color & ((1 << 8) - 1)))
    logger.debug((color >> 8 & ((1 << 8) - 1)))
    logger.debug((color >> 16 & ((1 << 8) - 1)))

    return color


# database: regions & saved screenshot
class _Regions:
    """
    Store region(length 4) or point(length 2) data at default screensize 1920*1080.
    Properties could be a region/point or a list(1 or multi dimension) of regions/points
    """
    safe_area = (1400, 40)
    rewards_action = (1681, 29, 1872, 97)
    bag_back = (49, 34, 242, 100)
    bag_finish = (870, 849, 1044, 908)
    bag_confirm = (1170, 845, 1340, 907)
    bag_select = (1600, 975, 1870, 1047)
    bag_full = (485, 660, 583, 718)
    box_back = (49, 34, 242, 100)
    box_get_action = (1509, 535, 1810, 582)
    box_get_all = (1524, 302, 1805, 354)
    box_items = [(1272, 400), (1272, 600), (1272, 800), (1272, 980)]
    box_history = (365, 30, 522, 102)
    box_full_confirm = (1112, 822, 1463, 873)
    reset_finish = (800, 811, 1113, 878)
    reset_confirm = (1097, 813, 1416, 879)
    reset_action = (1546, 337, 1863, 394)
    drawer = (600, 622)
    # drawer
    apply_friend = (464, 913)
    quest = (937, 240, 1848, 360)
    quest_c = (1277, 351)
    rewards = (1680, 33, 1868, 91)
    ap_time = (346, 1041, 366, 1072)
    apple_page = (471, 177, 645, 359)
    apple_close = (1000, 925)
    apples = ((471, 177, 645, 359), (471, 397, 645, 579), (474, 621, 645, 803), (471, 840, 645, 861))
    apple_confirm = (1061, 802, 1455, 882)
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

    start_quest = (1655, 973, 1902, 1052)

    enemies_all = (0, 0, 1080, 128)
    enemies = ((0, 0, 360, 130), (360, 0, 720, 130), (720, 0, 1080, 130))  # skill_to_enemies

    skills = [
        [(61, 823, 121, 908), (202, 823, 262, 908), (343, 823, 403, 908)],
        [(539, 823, 599, 908), (680, 823, 740, 908), (821, 823, 881, 908)],
        [(1017, 823, 1077, 908), (1158, 823, 1218, 908), (1299, 823, 1359, 908)]
    ]
    skill_target_X = (430, 600, 580, 750)  # 第一个人
    skill_to_target = ((490, 700), (970, 700), (1429, 700))
    master_skill = (1736, 440, 1841, 507)
    master_skills = ((1319, 427, 1404, 512), (1450, 427, 1535, 512), (1581, 427, 1666, 512))

    attack = (1615, 954, 1665, 1005)  # attack 字样以下部分，与大小变化的attack独立
    cards_back = (1725, 1007, 1878, 1043)
    cards = (
        (84, 655, 303, 903), (466, 655, 685, 903), (848, 655, 1067, 903), (1235, 655, 1454, 903),
        (1624, 655, 1843, 903),
        (515, 210, 750, 442), (871, 210, 1106, 442), (1227, 210, 1462, 442))
    cards_outer = ((0, 500, 386, 1000), (386, 500, 784, 1000), (784, 500, 1170, 1000), (1170, 500, 1552, 1000),
                   (1552, 500, 1920, 1000),
                   (428, 100, 812, 510), (812, 100, 1170, 510), (1170, 100, 1554, 510))

    order_change = (
        (87, 403, 322, 643), (387, 403, 622, 643), (687, 403, 922, 643), (987, 403, 1222, 643), (1287, 403, 1522, 643),
        (1587, 403, 1822, 643))
    order_change_confirm = (739, 907, 1167, 974)  # length 6

    kizuna = (115, 251, 580, 305)
    finish_qp = (418, 884, 487, 955)

    finish_next = (1444, 980, 1862, 1061)
    finish_graft = (454, 216, 623, 386)

    size = (1920, 1080)

    def relocate(self, region=(0, 0, 1920, 1080)):
        """
        Recursively resize regions. The default size is 1920*1080
        :param region: 4 length tuple - new region for resize, e.g. (100,100,1800,1000).
        :return: None.
        """
        assert len(region) == 4, region
        for key, value in _Regions.__dict__.items():
            # at most 3 layers
            if not key.startswith('__') and isinstance(value, (int, list, tuple)):
                # print(key, value)
                self.__dict__[key] = _Regions.loop(value, region)

    @staticmethod
    def loop(o, region):
        if isinstance(o, (tuple, list)):
            if isinstance(o[0], int):
                assert len(o) % 2 == 0, o
                oo = []
                for i, v in enumerate(o):
                    ii = i % 2
                    oo.append(int(region[ii] + (region[ii + 2] - region[ii]) / _Regions.size[ii] * o[i]))
                return oo
            else:
                return [_Regions.loop(k, region) for k in o]
        else:
            print(f'skip key(type:{type(o)}) for resize')


class _ImageTemplates:
    directory: str
    templates: Dict[str, PngImageFile]

    def __init__(self, directory=None):
        self.directory = directory
        self.templates = {}
        if directory is not None:
            self.read_templates(directory)

    def read_templates(self, directory, force=False):
        old_tmpls = self.templates
        self.templates = {}
        for filename in os.listdir(directory):
            if not filename.endswith('.png'):
                continue
            filepath = os.path.join(directory, filename)
            key = filename[0:len(filename) - 4]
            if (filepath not in old_tmpls or force is True) and directory == self.directory:
                self.templates[key] = Image.open(filepath)
            else:
                self.templates[key] = old_tmpls[key]
        self.directory = directory

    def get(self, attr):
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
    def apple_page(self):
        return self.get('apple_page')

    @property
    def cards(self):
        return self.get('cards')

    @property
    def cards_tmpls(self):
        tmpls = []
        for i in range(4):
            key = f'cards_tmpl{i + 1}'
            if key in self.templates:
                tmpls.append(self.templates[key])
            else:
                break
        return tmpls

    @property
    def cards_tmpl1(self):
        return self.get('cards_tmpl1')

    @property
    def cards_tmpl2(self):
        return self.get('cards_tmpl2')

    @property
    def cards_tmpl3(self):
        return self.get('cards_tmpl3')

    @property
    def cards_tmpl4(self):
        return self.get('cards_tmpl0')

    @property
    def finish_rewards(self):
        return self.get('finish_rewards')

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
    def start_quest(self):
        return self.get('start_quest')

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
    def wave2c(self):
        return self.get('wave2c')

    @property
    def wave2d(self):
        return self.get('wave2d')

    @property
    def wave3a(self):
        return self.get('wave3a')

    @property
    def wave3b(self):
        return self.get('wave3b')


class Timer:
    t1 = 0
    t2 = 0
    dt = 0

    def start(self):
        self.t1 = time.time()
        return self

    def stop(self):
        self.t2 = time.time()
        self.dt = self.t2 - self.t1
        print('Time lapse: %f sec' % (self.t2 - self.t1))
        # logger.debug('Time lapse: %f sec' % (self.t2 - self.t1))
        return self


# export constants
logger = get_logger()
logger2 = get_logger('craft', logging.WARNING)

LOC = _Regions()
T = _ImageTemplates()


def __gen_getter(path='./'):
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


def _test():
    pass


if __name__ == "__main__":
    _test()
    pass
