"""Data definition, constants
Coordination: using PIL coordination, (x,y), (left,top,right,bottom), e.g. (0,0,1920-1,1080-1)
"""

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

    # ---------- gacha part ----------
    # in gacha
    gacha_point = (600, 650)
    gacha_tab = (1009, 188, 1213, 228)
    gacha_10_initial = (483, 630, 800, 774)
    gacha_reset_action = (1546, 337, 1863, 394)
    gacha_reset_confirm = (1097, 813, 1416, 879)
    gacha_reset_finish = (800, 811, 1113, 878)
    gacha_empty = (285, 631, 524, 780)  # used when no ticket left
    # move to mailbox
    mailbox_full_confirm = (1112, 822, 1463, 873)

    # in mailbox
    mailbox_back = (49, 34, 242, 100)
    mailbox_get_action = (1509, 535, 1810, 582)
    mailbox_get_all_action = (1524, 302, 1805, 354)  # WARNING: don't click
    # box_items = [(1272, 400), (1272, 600), (1272, 800), (1272, 980)]
    mailbox_items = [(1231, 365, 1314, 447), (1231, 558, 1314, 640), (1231, 751, 1314, 833), (1231, 944, 1314, 1026)]
    mailbox_first_checkbox = (1231, 365, 1314, 447)
    mailbox_first_icon = (162, 350, 300, 435)
    mailbox_first_xn = (507, 295, 574, 329)  # x1
    mailbox_first_xn2 = (564, 295, 584, 329)  # '0' of x10
    mailbox_check_column = (1231, 264, 1314, 1079)
    mailbox_drag_start = (1070, 914)
    mailbox_drag_end = (1070, 250)
    box_history = (365, 30, 522, 102)
    # from mailbox move to bag/enhancement
    bag_full_sell_action = (471, 689, 565, 740)
    bag_full_enhance_action = (907, 689, 1008, 736)

    # in bag
    bag_back = (49, 34, 242, 100)
    bag_select_start = (200, 350)
    bag_select_end = (1416, 1050)
    bag_sell_action = (1600, 975, 1870, 1047)
    bag_sell_confirm = (1181, 847, 1340, 906)
    bag_sell_finish = (900, 845, 1020, 908)
    # jp version:
    # bag_sell_confirm = (1181, 912, 1340, 968)
    # bag_sell_finish = (875, 908, 1045, 966)

    # from bag to drawer
    shop_sell = (1352, 465, 1723, 552)
    shop_event_item_exchange = (1352, 239, 1723, 322)
    shop_event_banner_list = [(848, 168, 1525, 445), (848, 468, 1525, 745), (848, 768, 1525, 1045)]
    rewards_action = (1688, 29, 1872, 97)

    # ---------- battle part ----------
    apply_friend = (1692, 521, 1826, 588)
    apply_friend_deny = (464, 913)
    quest = (966, 256, 1149, 417)  # (937, 240, 1848, 360)
    quest_outer = (966, 246, 1149, 427)
    quest_c = (1600, 265)
    quest_master_avatar = (91, 835, 242, 997)
    # rewards = (1680, 33, 1868, 91)

    ap_time = (346, 1041, 366, 1072)
    apple_page = (471, 177, 645, 359)
    apple_close = (1000, 925)
    apples = ((471, 177, 645, 359), (471, 397, 645, 579), (474, 621, 645, 803), (471, 840, 645, 861))
    apple_confirm = (1195, 802, 1313, 882)
    # support = ((72,489,1617,560), (72,790,1617,860))
    # 2 supports one time，support[svt][skill]
    loading_line = (10, 1057, 70, 1060)
    support_team_icon = (1637, 320, 1767, 384)
    support_team_icon_column = (1637, 245, 1767, 1000)
    support_class_icons = [(117, 175, 165, 209), (218, 175, 266, 209), (319, 175, 367, 209), (420, 175, 468, 209),
                           (521, 175, 569, 209), (622, 175, 670, 209), (723, 175, 771, 209), (824, 175, 872, 209),
                           (925, 175, 973, 209), (1026, 175, 1074, 209)]  # All, 7 common class, extra, mix
    support_scrollbar_start = (1857, 270)
    support_scrollbar_end = (1857, 1047)
    support_scrollbar_head = (1843, 274, 1873, 296)
    support_ce = ((72, 489, 316, 537), (72, 791, 316, 838))  # 礼装位置
    support_ce_max = ((273, 524, 303, 552), (273, 825, 303, 854))  # 礼装满破的星星
    support_skill = ((1252, 463, 1577, 548), (1252, 764, 1577, 847))  # 技能整体外轮廓
    support_skills = [[(1260, 468, 1334, 544), (1378, 468, 1448, 544), (1497, 468, 1562, 544)],
                      [(1260, 768, 1334, 844), (1378, 768, 1448, 844), (1497, 768, 1562, 844)]]  # 3个技能外轮廓
    support_skill_lvs = [[(1260, 511, 1300, 544), (1380, 511, 1420, 544), (1500, 511, 1540, 544)],
                         [(1260, 811, 1334, 844), (1380, 811, 1454, 844),
                          (1500, 811, 1574, 844)]]  # 3个lv, 强化箭头未比较, not used

    support_confirm_title = (821, 171, 1108, 230)
    support_refresh_confirm = (1110, 890)
    support_refresh = (1238, 160, 1318, 230)
    support_scroll = ((1860, 520), (1860, 640), (760, 880))

    team_start_action = (1655, 973, 1902, 1052)
    team_cloth = (20, 980, 263, 1054)
    wave_num = (1293, 18, 1320, 54)
    enemies_all = (0, 0, 1080, 128)
    enemies = ((0, 0, 120, 130), (360, 0, 480, 130), (720, 0, 840, 130))  # skill_to_enemies
    dying_clicking_point = (960, 360)
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

    order_change = (
        (87, 403, 322, 643), (387, 403, 622, 643), (687, 403, 922, 643), (987, 403, 1222, 643), (1287, 403, 1522, 643),
        (1587, 403, 1822, 643))
    order_change_confirm = (739, 907, 1167, 974)  # length 6

    # kizuna = (115, 251, 580, 305)  # 与从者的羁绊text
    kizuna = (186, 646, 205, 665)  # 羁绊点数第一格
    finish_qp = (418, 884, 487, 955)
    rewards_show_num = (1593, 115, 1718, 149)
    finish_next = (1444, 980, 1862, 1061)
    finish_craft = (454, 216, 623, 386)
    restart_quest_yes = (1122, 812, 1386, 829)
    friend_point = (460, 810, 580, 880)

    width = 1920
    height = 1080
    size = (0, 0, width - 1, height - 1)  # left top right bottom

    def relocate(self, region):
        """
        Recursively resize regions. The default size is 1920*1080: region=(0,0,1920-1,1080-1)
        :param region: region located in screen, (x0,y0,x1,y1): 0 <= x0 < x1 < width, 0 <= y0 < y1 < height
        :return:
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

    def gen_empty_img(self, color=(255, 0, 0)):
        return Image.new('RGB', (self.width, self.height), color)


class ImageTemplates:
    directory: str
    templates: Dict[str, Image.Image]

    def __init__(self, directory: str = None):
        self.directory = directory
        self.templates = {}
        if directory is not None:
            self.read_templates(directory)

    def read_templates(self, directory: str, force=False):
        old_templates = self.templates
        self.templates = {}
        flag = False
        for filename in os.listdir(directory):
            if not filename.endswith('.png'):
                continue
            filepath = os.path.join(directory, filename)
            key = filename[0:len(filename) - 4]
            if directory == self.directory and force is False and key in old_templates:
                self.templates[key] = old_templates[key]
            else:
                flag = True
                self.templates[key] = Image.open(filepath)
        if flag:
            logger.debug(f'template images updated: {directory}')
        self.directory = directory

    def get(self, attr, k=None):
        # type:(Union[str, Sequence[str]],Image.Image)-> Union[Image.Image, Sequence[Image.Image], Dict]
        if attr is None:
            return self.templates.copy()
        elif isinstance(attr, (list, tuple)):
            return [self.templates[k] for k in attr]
        elif attr in self.templates:
            return self.templates[attr]
        return k

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

    # ================ gacha ================
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
    def mailbox_full_alert(self):
        return self.get('mailbox_full_alert')

    @property
    def mailbox_unselected1(self):
        return self.get('mailbox_unselected1')

    @property
    def mailbox_unselected2(self):
        return self.get('mailbox_unselected2')

    @property
    def mailbox_selected(self):
        return self.get('mailbox_selected')

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

    @property
    def shop_event_banner_list(self):
        return self.get('shop_event_banner_list')


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
