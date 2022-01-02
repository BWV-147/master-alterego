"""Data definition, constants
Coordination: using PIL coordination, (x,y), (left,top,right,bottom), e.g. (0,0,1920-1,1080-1)
"""
import os

from PIL import Image

from .base import *
from .log import logger

THR = 0.80  # default threshold


class _Regions:
    """
    Base class to store region(length 4) or point(length 2) data at default screen size 1920*1080.
    Attributes(except width and height are int value) must be the assembly of point and region.
    Don't use double underline "__" as prefix for attribute name, otherwise it will be ignored.
    """
    width = 1920
    height = 1080
    box = (0, 0, width, height)

    def __init__(self, is_jp=False):
        # can only relocate once
        self.__jp = is_jp
        if is_jp:
            self._override_jp()

    @classmethod
    def _get_region_items(cls):
        for k in dir(cls):  # type:str
            v = getattr(cls, k)
            if k.startswith('__') or callable(v):
                pass
            elif isinstance(v, (list, tuple)):
                yield k, v

    def reset(self, is_jp=None):
        """Reset region values from base class _Regions"""
        if is_jp is None:
            is_jp = self.__jp
        for k, v in _Regions._get_region_items():
            setattr(self, k, v)
        self.width = _Regions.width
        self.height = _Regions.height
        if is_jp:
            self._override_jp()

    def _override_jp(self):
        """different locations of JP, override this function"""
        pass

    @staticmethod
    def relocate_one(region, new: Sequence, old: Sequence = (0, 0, 1919, 1079)):
        assert isinstance(region, Sequence), f'region should be Sequence: {region}'
        if not region:  # empty
            return region
        elif isinstance(region[0], Sequence):
            return tuple([Regions.relocate_one(r, new, old) for r in region])
        elif isinstance(region[0], (int, float)):
            length = len(region)
            assert length % 2 == 0, f'region length must be 2(point) or 4(rect): {region}'
            if length > 4:
                logger.warning(f'warning: more than 4 elements: {region}')
            out = []
            for i in range(length // 2):
                x, y = region[i * 2:i * 2 + 2]
                x2 = (x - old[0]) / (old[2] - old[0]) * (new[2] - new[0]) + new[0]
                y2 = (y - old[1]) / (old[3] - old[1]) * (new[3] - new[1]) + new[1]
                # (x,y) coordinates: in PIL it will be round then int.
                out.append(int(round(x2)))
                out.append(int(round(y2)))
            return tuple(out)
        else:
            raise ValueError(f'elements must be numbers: {region}')

    def relocate(self, box: Sequence = None):
        """
        Recursively resize regions of original class attributes not `self`.

        :param box: new region located in screenshot, (x0,y0,x1,y1): 0 <= x0 < x1 < width, 0 <= y0 < y1 < height.
                     old box always use `self.__class__.box`
        """
        if box is None or tuple(box) == self.box:
            return
        if tuple(self.box) != _Regions.box:
            self.reset()
        width = int(box[2] - box[0])
        height = int(box[3] - box[1])
        assert len(box) == 4 and width > 0 and height > 0, f'Invalid box: {box}'

        self.width = width
        self.height = height
        for k, v in self._get_region_items():
            setattr(self, k, self.relocate_one(v, box, _Regions.box))
        logger.info(f'Relocate Regions from {Regions.box} to {tuple(self.box)}')


# database: regions & saved screenshot
class Regions(_Regions):
    """
    Store region(length 4) or point(length 2) data at screensize 1920*1080.
    """
    # only width and height are standalone int, others are Sequence
    width = 1920
    height = 1080
    box = (0, 0, width, height)  # left top right bottom

    # common, or for supervisor
    net_error = ((599, 814, 720, 872), (1138, 813, 1378, 876))
    login_news_close = (1835, 22, 1900, 86)
    login_popup_clicking = (1382, 64)
    login_terminal_event_banner = (1044, 500, 1377, 586)
    safe_area = (1460, 100)  # for battle
    svt_status_window_close = (1607, 67, 1660, 100)

    # ---------- lottery part ----------
    lottery_point = (600, 650)
    lottery_tab = (1000, 188, 1110, 228)
    lottery_10_initial = (483, 630, 800, 774)
    lottery_reset_action = (1546, 337, 1863, 394)
    lottery_reset_confirm = (1097, 813, 1416, 879)
    lottery_reset_finish = (800, 811, 1113, 878)
    lottery_empty = (285, 631, 524, 780)  # used when no ticket left
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
    bag_full_sell_button = (461, 659, 575, 720)
    # bag_full_sell_button = (471, 689, 565, 740)
    bag_full_enhance_button = (897, 664, 1018, 721)
    # bag_full_enhance_button = (907, 689, 1008, 736)

    # menu
    # menu_button = (1704, 1005, 1852, 1048)
    # menu_button_expand = (1704, 772, 1852, 815)
    # menu_enhance_button = (651, 933, 763, 1011)
    # menu_gacha_button = (900, 933, 1002, 1011)
    # menu_shop_button = (1155, 933, 1260, 1011)
    menu_button = (1704, 955, 1852, 998)
    menu_button_expand = (1704, 682, 1852, 725)
    menu_enhance_button = (660, 850, 760, 930)
    menu_gacha_button = (923, 854, 995, 918)
    menu_shop_button = (1171, 856, 1237, 922)

    # in bag
    bag_back = (49, 34, 242, 100)
    bag_svt_tab = (107, 152, 193, 191)
    bag_select_start = (200, 350)
    bag_select_middle = (1416, 350)
    bag_select_end = (1416, 1050)
    bag_sell_action = (1690, 975, 1780, 1047)
    bag_sell_confirm = (1181, 912, 1340, 968)
    bag_sell_finish = (875, 908, 1045, 966)
    bag_qp_limit_confirm = (1334, 811, 1449, 868)

    # ce enhance
    ce_enhance_button = (1599, 975, 1727, 1038)
    # ce_enhance_button = (1587, 988, 1715, 1051)
    ce_enhance_help = (640, 1014, 705, 1050)
    ce_target_box = (211, 520, 373, 687)
    ce_select_mode = (5, 319, 88, 411)
    ce_targets = [(1307, 362, 1356, 382), (1107, 362, 1156, 382), (908, 362, 957, 382), (708, 362, 757, 382),
                  (509, 362, 558, 382), (309, 362, 358, 382), (110, 362, 159, 382)]

    ce_select_items_box = (600, 300, 700, 400)
    ce_select_button = (1680, 980, 1777, 1040)
    ce_select_start = (210, 800)  # line 3, first item
    ce_select_middle = (1407, 800)  # line 3, last item
    ce_select_end = (1407, 1076)  # line 4, last item
    ce_enhance_lv2 = (1253, 671, 1322, 717)
    ce_enhance_confirm = (1203, 855, 1316, 913)
    # from bag to drawer
    shop_sell = (1352, 465, 1723, 552)
    shop_event_item_exchange = (1352, 239, 1723, 322)
    shop_event_banner_list = [(848, 168, 1525, 445), (848, 468, 1525, 745), (848, 768, 1525, 1045)]
    rewards_action = (1688, 29, 1872, 97)

    # ---------- battle part ----------
    apply_friend = (1692, 521, 1826, 588)
    apply_friend_deny = (464, 913)
    quest = (966, 295, 1149, 350)  # (937, 240, 1848, 360)
    quest_outer = (966, 246, 1149, 360)
    quest_c = (1600, 265)
    quest_master_avatar = (91, 835, 242, 997)
    # rewards = (1680, 33, 1868, 91)

    ap_time = (346, 1041, 366, 1072)
    apple_close = (900, 900, 1016, 952)
    apples = ((471, 177, 645, 359), (471, 397, 645, 579), (474, 621, 645, 803), (471, 840, 645, 861))
    apple_confirm = (1195, 802, 1313, 882)
    # support = ((72,489,1617,560), (72,790,1617,860))
    # 2 supports one time，support[svt][skill]
    loading_line = (10, 1057, 70, 1060)
    support_team_icon = (1637, 320, 1767, 384)
    support_team_column = (1637, 245, 1767, 1000)
    support_class_icons = [(117, 175, 165, 209), (218, 175, 266, 209), (319, 175, 367, 209), (420, 175, 468, 209),
                           (521, 175, 569, 209), (622, 175, 670, 209), (723, 175, 771, 209), (824, 175, 872, 209),
                           (925, 175, 973, 209), (1026, 175, 1074, 209)]  # All, 7 common class, extra, mix
    support_scrollbar_start = (1882, 294)
    support_scrollbar_end = (1882, 1047)
    support_scrollbar_head = (1873, 280, 1895, 296)
    # support_scrollbar_start = (1857, 280)
    # support_scrollbar_end = (1857, 1047)
    # support_scrollbar_head = (1848, 280, 1870, 296)
    support_ce = ((72, 489, 316, 537), (72, 791, 316, 838))  # 礼装位置
    support_ce_max = ((273, 524, 303, 552), (273, 825, 303, 854))  # 礼装满破的星星

    support_skill = (1252, 463, 1577, 548)  # 技能整体外轮廓
    support_skills = [(1260, 468, 1334, 544), (1378, 468, 1448, 544), (1497, 468, 1562, 544)]  # 3个技能外轮廓
    support_skill_lvs = [(1260, 511, 1300, 544), (1380, 511, 1420, 544),
                         (1500, 511, 1540, 544)]  # 3个lv, 强化箭头未比较, not used

    # # jp support: add append skill
    # support_skill = (1255, 494, 1444, 548)  # 技能整体外轮廓
    # support_skills = [(1260, 468, 1334, 544), (1378, 468, 1448, 544), (1497, 468, 1562, 544)]  # 3个技能外轮廓
    # support_skill_lvs = [(1260, 511, 1300, 544), (1380, 511, 1420, 544),
    #                      (1500, 511, 1540, 544)]  # 3个lv, 强化箭头未比较, not used
    # end append skill
    support_friend_icon = (1696, 484, 1741, 529)

    support_confirm_title = (821, 171, 1108, 230)
    support_refresh_confirm = (1110, 890)
    support_refresh = (1238, 160, 1318, 230)
    support_class_affinity = (1119, 160, 1201, 230)

    team_start_action = (1660, 975, 1850, 1034)
    # team_start_action = (1690, 983, 1880, 1042)
    team_cloth = (20, 980, 263, 1054)  # with close icon inside
    team_cloth_button = (148, 986, 263, 1054)  # without cloth

    battle_master_avatar = (1706, 77, 1854, 189)
    wave_num = (1323, 18, 1345, 54)
    enemies_all = (0, 0, 1110, 128)
    enemies = ((754, 10, 874, 130), (387, 10, 497, 130), (20, 10, 120, 130))  # skill_to_enemies
    skills = [[(74 + i * 476 + j * 140, 832, 129 + i * 476 + j * 140, 897) for j in range(3)] for i in
              range(3)]
    # wave_num = (1298, 18, 1320, 54)
    # enemies_all = (0, 0, 1080, 128)
    # enemies = ((720, 10, 840, 130), (370, 10, 480, 130), (20, 10, 120, 130))  # skill_to_enemies
    dying_clicking_point = (1200, 40)
    # skills = [[(63 + i * 476 + j * 140, 825, 120 + i * 476 + j * 140, 893) for j in range(3)] for i in range(3)]
    skill_targets_close = (1614, 195, 1678, 256)
    skill_to_target = ((490, 700), (970, 700), (1429, 700))
    master_skill = (1736, 440, 1841, 507)
    master_skills = ((1319, 427, 1404, 512), (1450, 427, 1535, 512), (1581, 427, 1666, 512))
    loc_wave = [master_skill, wave_num]
    attack = (1599, 957, 1688, 1010)  # 大小可变的attack字样以下部分，且与cards_back不重叠
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
    order_change_close = (1804, 176, 1861, 229)
    order_change_confirm = (739, 907, 1167, 974)  # length 6

    # kizuna = (115, 251, 580, 305)  # 与从者的羁绊text
    # kizuna = (186, 646, 205, 665)  # 羁绊点数第一格
    kizuna = (257, 598, 325, 613)  # 头像框下侧servant字样
    craft_detail_tab1 = (784, 177, 967, 229)

    rewards_qp = (448, 845, 477, 877)
    rewards_show_num = (1593, 62, 1711, 92)
    rewards_items_outer = [[(233 + j * 206, 132 + i * 213, 409 + j * 206, 325 + i * 213) for j in range(0, 7)]
                           for i in range(0, 3)]
    rewards_items = [[(241 + j * 206, 142 + i * 213, 401 + j * 206, 236 + i * 213) for j in range(0, 7)]
                     for i in range(0, 3)]
    rewards_item1 = (447, 142, 607, 236)  # first dropped item rect
    rewards_rainbow = (1452, 16, 1459, 32)
    rewards_next = (1576, 920, 1750, 1001)

    # rewards_qp = (450, 900, 472, 930)
    rewards_clicking = (70, 860)
    # rewards_show_num = (1593, 115, 1711, 149)
    # rewards_items_outer = [[(233 + j * 206, 186 + i * 213, 409 + j * 206, 379 + i * 213) for j in range(0, 7)] for i in
    #                        range(0, 3)]
    # rewards_items = [[(241 + j * 206, 196 + i * 213, 401 + j * 206, 290 + i * 213) for j in range(0, 7)] for i in
    #                  range(0, 3)]
    # rewards_item1 = rewards_items[0][1]  # first dropped item rect
    # rewards_rainbow = (1418, 18, 1442, 50)
    rewards_suochi_character = (445, 274, 495, 301)  # "所"最后一竖
    # rewards_next = (1576, 980, 1750, 1061)
    restart_quest_yes = (1122, 812, 1386, 879)
    # friend_point = (460, 810, 580, 880)

    # ============= fp gacha ================
    gacha_fp_logo = (981, 41, 1028, 86)
    gacha_quartz_logo = (567, 41, 612, 76)
    gacha_help = (111, 899, 198, 944)
    gacha_fp_10_button = (1111, 800, 1374, 886)
    gacha_fp_point = (1240, 864)  # click point
    gacha_fp_confirm = (1205, 819, 1300, 868)
    gacha_fp_result_summon = (987, 983, 1302, 1035)  # gacha10again, origin is(1096, 980, 1200, 1037)

    fp_bag_full_title = (569, 225, 660, 275)
    fp_bag_full_sell_button = (471, 689, 565, 740)
    fp_bag_full_enhance_button = (907, 689, 1008, 736)
    fp_bag_full_archive_button = (1283, 689, 1518, 736)
    fp_bag_full_close_button = (913, 823, 1007, 871)

    gacha_arrow_left = (77, 539)
    gacha_arrow_right = (1850, 539)

    def _override_jp(self):
        self.bag_full_sell_button = (461, 659, 575, 720)
        self.bag_full_enhance_button = (897, 664, 1018, 721)

        self.menu_button = (1704, 955, 1852, 998)
        self.menu_button_expand = (1704, 682, 1852, 725)
        self.menu_enhance_button = (660, 850, 760, 930)
        self.menu_gacha_button = (923, 854, 995, 918)
        self.menu_shop_button = (1171, 856, 1237, 922)

        self.rewards_qp = (448, 845, 477, 877)
        self.rewards_show_num = (1593, 62, 1711, 92)
        self.rewards_items_outer = [[(233 + j * 206, 132 + i * 213, 409 + j * 206, 325 + i * 213) for j in range(0, 7)]
                                    for i in range(0, 3)]
        self.rewards_items = [[(241 + j * 206, 142 + i * 213, 401 + j * 206, 236 + i * 213) for j in range(0, 7)]
                              for i in range(0, 3)]
        self.rewards_item1 = (447, 142, 607, 236)  # first dropped item rect
        self.rewards_rainbow = (1452, 16, 1459, 32)
        self.rewards_next = (1576, 920, 1750, 1001)

        self.support_scrollbar_start = (1882, 294)
        self.support_scrollbar_end = (1882, 1047)
        self.support_scrollbar_head = (1873, 280, 1895, 296)

        self.team_start_action = (1660, 975, 1850, 1034)

        self.wave_num = (1323, 18, 1345, 54)
        self.enemies_all = (0, 0, 1110, 128)
        self.enemies = ((754, 10, 874, 130), (387, 10, 497, 130), (20, 10, 120, 130))  # skill_to_enemies
        self.skills = [[(74 + i * 476 + j * 140, 832, 129 + i * 476 + j * 140, 897) for j in range(3)] for i in
                       range(3)]

        self.ce_enhance_button = (1599, 975, 1727, 1038)

        self.support_skill = (1255, 494, 1444, 548)  # 技能整体外轮廓,只用第一个
        self.support_skills = [(1260, 500, 1302, 541), (1329, 500, 1370, 541), (1396, 500, 1438, 542)]  # 3个技能外轮廓
        self.support_skill_lvs = [(1260, 519, 1302, 541), (1329, 519, 1370, 541),
                                  (1396, 519, 1438, 542)]  # 3个lv, 强化箭头未比较, not used


class ImageTemplates:
    """
    Store loaded template images. Image file(*.png) should be screenshots token by PIL or mss module.
    Otherwise, image comparison may not work.
    @DynamicAttrs
    """

    def __init__(self, directory: str = None, recursive=False):
        self.dirs: str = directory
        self.templates: Dict[str, Image.Image] = {}

        # ============ error part ============
        self.net_error = None
        self.svt_status_window = None
        self.login_news = None
        self.login_popup = None
        self.login_terminal = None

        # ============ battle part ============
        self.apple_confirm = None
        self.apple_page = None
        self.apply_friend = None
        self.cards1 = None
        self.cards2 = None
        self.cards3 = None
        self.cards4 = None
        self.craft_detail = None
        self.rewards_init = None
        self.rewards = None
        self.kizuna = None
        self.order_change = None
        self.quest = None
        self.team = None
        self.restart_quest = None
        self.support = None
        self.support_confirm = None
        self.skill_targets = None
        self.wave1a = None
        self.wave1b = None
        self.wave2a = None
        self.wave2b = None
        self.wave3a = None
        self.wave3b = None
        # ============ lottery part ============
        self.lottery_initial = None
        self.lottery_empty = None
        self.lottery_reset_confirm = None
        self.lottery_reset_finish = None
        self.mailbox_full_alert = None
        self.mailbox_unselected1 = None
        self.mailbox_unselected2 = None
        self.mailbox_selected = None
        self.bag_full_alert = None
        self.bag_unselected = None
        self.bag_selected = None
        self.bag_sell_confirm = None
        self.bag_sell_finish = None
        self.bag_qp_limit = None
        self.shop = None
        self.shop_event_banner_list = None
        # ============ fp gacha part ============
        self.gacha_quartz_page = None
        self.gacha_fp_page = None
        self.gacha_fp_confirm = None
        self.gacha_fp_result = None
        self.gacha_fp_svt_full = None
        self.gacha_fp_ce_full = None
        self.menu = None
        self.ce_enhance_empty = None
        self.ce_select_target = None
        self.ce_items_unselected = None
        self.ce_items_selected = None
        self.ce_enhance_page = None
        self.ce_enhance_confirm = None
        # ============ mystic code part ============
        self.mystic_code_01_chaldea = None  # 初始服
        self.mystic_code_04_battle = None  # 战斗服
        self.mystic_code_02_mages = None  # 魔术协会制服
        self.mystic_code_03_atlas = None  # 阿特拉斯院制服
        self.mystic_code_05_blonde = None  # 金色庆典
        self.mystic_code_06_brand = None  # 王室品牌
        self.mystic_code_07_summer = None  # 明亮夏日
        self.mystic_code_08_extra = None  # 月之海的记忆
        self.mystic_code_09_ccc = None  # 月之背面的记忆
        self.mystic_code_10_fuyuki = None  # 2004年的碎片
        self.mystic_code_11_polar = None  # 极地服
        self.mystic_code_12_tropical = None  # 热带夏日
        self.mystic_code_13_fine = None  # 华美新年
        self.mystic_code_14_captain = None  # 迦勒底船长 太空服
        self.mystic_code_15_true_element = None  # 第五真实元素环境用迦勒底制服
        self.mystic_code_16_pathfinder = None  # 迦勒底开拓者
        # =========== End Props =========== #
        if directory is not None:
            self.read_templates(directory, recursive=recursive)

    def read_templates(self, directory: Union[str, List[str]] = None, append=False, recursive=False):
        """
        Read template .png images from one or more dirs. If duplicated filenames, the last image will be remained
        :param directory:
        :param append: if false, clear the templates first.
        :param recursive:
        :return:
        """
        if directory is None:
            return
        if isinstance(directory, (list, tuple)):
            if not append:
                self.templates = {}
                self.dirs = []
            for _dir in directory:
                self.read_templates(_dir, True)
            return

        if not append:
            self.templates = {}
            self.dirs = []
        all_filepath = []
        if recursive:
            for root, dirs, files in os.walk(directory):
                all_filepath.extend([os.path.join(root, f) for f in files])
            self.dirs.append(directory.upper())
        else:
            for fn in os.listdir(directory):
                fp = os.path.join(directory, fn)
                if os.path.isfile(fp):
                    all_filepath.append(fp)
            self.dirs.append(directory.lower())
        for filepath in all_filepath:
            if not filepath.endswith('.png'):
                continue
            # filepath = os.path.join(directory, filepath)
            key = os.path.basename(filepath)[:-4]
            if self.__dict__.get(key, None) is not None and not isinstance(self.__dict__[key], Image.Image):
                raise ValueError(f'Key "{key}" already exist (not image): {self.__dict__[key]}')
            self.__dict__[key] = self.templates[key] = Image.open(filepath)
        self.dirs.append(directory)

    def __repr__(self):
        return f'{self.__class__.__name__}(dirs="{self.dirs}", templates={self.templates})'

    def __getattr__(self, item):
        """if @property item is not defined, then search item in self.templates"""
        # could be removed?
        if item in self.templates:
            return self.templates[item]
        else:
            return None
            # raise AttributeError(f'{item} for class {self.__class__.__name__}')

    def get(self, item, k=None):
        # type:(Union[str, Sequence[str]],Image.Image)-> Union[Image.Image, Sequence[Image.Image]]
        """get one item or a list of items"""
        if isinstance(item, str) and item in self.templates:
            return self.templates[item]
        elif isinstance(item, (list, tuple)):
            # cannot use Sequence instead (list, tuple), str is also Sequence
            return [self.templates[i] for i in item]
        else:
            return k
