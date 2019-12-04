"""Master class

additional, Card class included.
"""
# noinspection PyPackageRequirements
from goto import with_goto

from util.autogui import *
from util.config import BaseConfig
from util.supervisor import send_mail


class Card:
    NP = 0
    QUICK = 1
    ARTS = 2
    BUSTER = 3

    def __init__(self, loc, code):
        self.loc = loc
        self.code = code
        self.svt = code // 10
        self.color = code % 10

    def __repr__(self):
        return f'{self.__class__.__name__}({self.loc}, {self.code})'


# noinspection PyMethodMayBeStatic
class Master:
    """
    1. crop screen to match card's svt&color
    2. weights to decide the suit to play
    3.
    card: (svt_no, color)
    """

    def __init__(self, quest='', names=None):
        self.quest_name = quest
        self.svt_names = names if names is not None else ['A', 'B', 'C', 'D', 'E', 'F']
        self.T = ImageTemplates()
        self.LOC = Regions()
        self.templates = {}
        self.weights: dict = {}
        self.wave_a = None
        self.wave_b = None

    def set_battle_data(self, coord=None, names=None, weights=None, cards_loc=None):
        if coord:
            self.LOC.relocate(coord)
        if names:
            self.svt_names = names
        if weights:
            self.set_card_weights(weights)
        if cards_loc:
            self.set_card_templates(cards_loc)

    # procedures
    def eat_apple(self, apples=None):
        apples = convert_to_list(apples)
        if config.stop_around_3am:
            t = time.localtime()
            if t.tm_hour == 2 and t.tm_min > 45:
                logger.info('Around 3am, stop eating apples and battles.')
                BaseConfig.task_finished = True
                return False
        if len(apples) > 0:
            for apple in apples:
                if apple not in (0, 1, 2, 3):
                    break
                if apple == 0:  # 不舍得吃彩苹果
                    apple = 3
                if is_match_target(screenshot(), self.T.apple_page, self.LOC.apples[apple]):
                    eaten = False
                    while True:
                        shot = screenshot()
                        page_no = match_which_target(shot, [self.T.apple_page, self.T.apple_confirm, self.T.support],
                                                     [self.LOC.apples[apple], self.LOC.apple_confirm,
                                                      self.LOC.support_refresh])
                        if page_no == 0:
                            if not eaten:
                                logger.debug(f"eating {['Colorful', 'Gold', 'Silver', 'Cropper'][apple]} apple...")
                            eaten = True
                            click(self.LOC.apples[apple], lapse=1)
                        elif page_no == 1:
                            click(self.LOC.apple_confirm, lapse=1)
                        elif page_no == 2:
                            break
                    return True

                    # noinspection DuplicatedCode

        logger.info(f'apples={apples}, don\'t eat apple or no left apples, task finish.')
        BaseConfig.task_finished = True
        return False

    def choose_support(self, match_svt=True, match_ce=False, match_ce_max=False, match_skills=None, img=None,
                       switch_classes=None):
        # type:(bool,bool,bool,List[int],Image.Image,Sequence)->None
        """
        Choose support from the *first two* supports, no dragging scrollbar.
        The two supports in template(T.support) should be the same.
        Args: see self.choose_support_drag
        """
        logger.debug('choosing support...')
        support_page = self.T.support if img is None else img
        if switch_classes is None:
            switch_classes = (-1,)
        wait_which_target(support_page, self.LOC.support_refresh)
        refresh_times = 0
        while True:
            found = False
            time.sleep(0.5)
            for icon in switch_classes:
                if icon == -1:
                    click(self.LOC.safe_area)
                else:
                    click(self.LOC.support_class_icons[icon])
                    logger.debug(f'switch support class to No.{icon}.')
                shot = screenshot()
                if match_svt is False:  # select first one
                    if is_match_target(shot, support_page, self.LOC.support_team_icon) \
                            and is_match_target(shot, support_page, self.LOC.support_ce[0]):
                        # match ce too, temp.
                        click(self.LOC.support_ce[0])
                        found = True
                else:
                    for svt in range(2):  # 2 support one time, no scroll
                        if is_match_target(shot, support_page, self.LOC.support_skill[svt]):
                            if match_skills is not None:
                                rs = [is_match_target(shot, support_page,
                                                      self.LOC.support_skills[svt][skill_loc - 1])
                                      for skill_loc in match_skills]
                                if rs.count(True) != len(match_skills):
                                    continue
                            if match_ce:
                                if not is_match_target(shot, support_page, self.LOC.support_ce[svt]):
                                    continue
                            if match_ce_max:
                                if not is_match_target(shot, support_page, self.LOC.support_ce_max[svt]):
                                    continue
                            click(self.LOC.support_ce[svt])
                            logger.debug(f'choose support No.{svt + 1}')
                            found = True
                            break
                if found:
                    break
            # refresh support
            if found:
                break
            refresh_times += 1
            logger.debug(f'refresh support {refresh_times} times')
            if refresh_times == 40:
                send_mail(body='refresh support more than 40 times.', subject='refresh support more than 40 times')
            wait_which_target(support_page, self.LOC.support_refresh, at=True)
            wait_which_target(self.T.support_confirm, self.LOC.support_confirm_title, clicking=self.LOC.support_refresh)
            click(self.LOC.support_refresh_confirm, lapse=2)
        while True:
            # =1: in server cn and first loop to click START
            page_no = wait_which_target([self.T.team, self.T.wave1a], [self.LOC.team_cloth, self.LOC.master_skill])
            if page_no == 0:
                # print('click start please\r', end='\r')
                # time.sleep(5)
                logger.debug('entering battle')
                click(self.LOC.team_start_action, lapse=2)
            elif page_no == 1:
                break
            else:
                time.sleep(0.2)

    # noinspection DuplicatedCode
    def choose_support_drag(self, match_svt=True, match_ce=False, match_ce_max=False, match_skills=None, img=None,
                            switch_classes=None):
        # type:(bool,bool,bool,bool,Image.Image,Sequence)->None
        """
        Choose the *first* support in T.support from the whole support list, drag scrollbar to show all supports.
        :param match_svt: match the whole rect of 3 skills
        :param match_ce: whether match CE, please set to False if jp server since CE could be filtered in jp server
        :param match_ce_max: whether match CE max star
        :param match_skills: match every skill icon
        :param img: support page img
        :param switch_classes: e.g. (0,5,...) means switch between ALL and CASTER.
                        ALL=0, Saber-Berserker=1-7, extra=8, Mixed=9. if empty, set (-1,), click Regions.safe_area
        """
        T = self.T
        LOC = self.LOC
        import pyautogui
        logger.debug('choosing support (drag mode)...')
        support_page = self.T.support if img is None else img
        if switch_classes is None:
            switch_classes = (-1,)
        wait_which_target(support_page, self.LOC.support_refresh)
        refresh_times = 0

        def _is_match_offset(_shot, old_loc, _offset):
            return is_match_target(_shot.crop(np.add(old_loc, [0, _offset, 0, _offset])), T.support.crop(old_loc))

        while True:
            time.sleep(0.5)
            for icon in switch_classes:
                if icon == -1:
                    # click(self.LOC.safe_area)
                    time.sleep(0.2)
                    pass
                else:
                    click(self.LOC.support_class_icons[icon])
                    logger.debug(f'switch support class to No.{icon}.')
                # drag scrollbar ,start=(1857, 270), dy=111, end=(1857, 1047)
                pyautogui.moveTo(*LOC.support_scrollbar_start)
                drag_num = 5 if is_match_target(screenshot(), T.support, LOC.support_scrollbar_head, 0.8) else 1
                dy_mouse = (LOC.support_scrollbar_end[1] - LOC.support_scrollbar_start[1]) // drag_num
                for drag_no in range(drag_num):
                    shot = screenshot()
                    y_peaks = search_peaks(shot.crop(LOC.support_team_icon_column),
                                           T.support.crop(LOC.support_team_icon))
                    for y_peak in y_peaks:
                        y_offset = y_peak - (LOC.support_team_icon[1] - LOC.support_team_icon_column[1])
                        flag_ce = not match_ce or _is_match_offset(shot, LOC.support_ce[0], y_offset)
                        flag_ce_max = not match_ce_max or _is_match_offset(shot, LOC.support_ce_max[0], y_offset)
                        flag_svt = not match_svt or _is_match_offset(shot, LOC.support_skill[0], y_offset)
                        flag_skills = not match_skills or False not in [_is_match_offset(shot, loc, y_offset) for loc in
                                                                        LOC.support_skills[0]]
                        if flag_ce and flag_ce_max and flag_svt and flag_skills:
                            click((LOC.width / 2, LOC.support_team_icon_column[1] + y_peak))
                            while True:
                                page_no = wait_which_target([self.T.team, self.T.wave1a],
                                                            [self.LOC.team_cloth, self.LOC.master_skill])
                                time.sleep(0.3)
                                if page_no == 0:
                                    # print('click start please\r', end='\r')
                                    logger.debug('entering battle')
                                    click(self.LOC.team_start_action)
                                    click(self.LOC.team_start_action, lapse=2)
                                    time.sleep(2)
                                    return
                                elif page_no == 1:
                                    return
                    time.sleep(0.2)
                    pyautogui.dragRel(0, dy_mouse, 0.2)
            # refresh support
            refresh_times += 1
            logger.debug(f'refresh support {refresh_times} times')
            if refresh_times == 40:
                send_mail(body='refresh support more than 40 times.', subject='refresh support more than 40 times')
            wait_which_target(support_page, self.LOC.support_refresh, at=True)
            wait_which_target(self.T.support_confirm, self.LOC.support_confirm_title, clicking=self.LOC.support_refresh)
            click(self.LOC.support_refresh_confirm, lapse=2)

    def svt_skill_full(self, before, after, who, skill, friend=None, enemy=None):
        # type: (Image.Image,Image.Image,int,int,int,int)->None
        """
        Release servant skill to <self/all friends/all enemies>.
        :param before: image before the skill released.
        :param after: image after the skill released.
        :param who: who to release the skill.value in [left=1,mid=2,right=3], the same below.
        :param skill: which skill to release.
        :param friend: which friend
        :param enemy: which enemy
        :return: None
        """
        # validation
        valid1, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert who in valid1 and skill in valid1 and friend in valid2 and enemy in valid2, (who, skill, friend, enemy)
        s = f'to friend {friend}' if friend \
            else f'to enemy {enemy}' if enemy else ''
        logger.debug('Servant skill %s-%d %s.' % (who, skill, s))

        # start
        if enemy is not None:
            click(self.LOC.enemies[enemy - 1])
        region = self.LOC.skills[who - 1][skill - 1]
        wait_which_target(before, region, at=True)
        if friend is not None:
            # it should also match the saved screenshot, but...
            # TODO: match select target shot, same as master_skill
            time.sleep(0.5)
            click(self.LOC.skill_to_target[friend - 1])
        wait_which_target(after, region)

    def set_waves(self, before: Image.Image, after: Image.Image):
        self.wave_a = before
        self.wave_b = after
        return self

    def svt_skill(self, who: int, skill: int, friend: int = None, enemy: int = None):
        self.svt_skill_full(self.wave_a, self.wave_b, who, skill, friend, enemy)
        return self

    def master_skill(self, skill, friend=None, enemy=None, order_change=None, order_change_img=None):
        # type:(int,int,int,Tuple[int,int],Image.Image)->Master
        """
        Master skill, especially order_change = (svt1:1~3,svt2:4~6) if not None
        """
        valid, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert skill in valid and friend in valid2 and enemy in valid2, (skill, friend, enemy)
        if order_change is not None:
            assert order_change[0] in (1, 2, 3) and order_change[1] in (4, 5, 6)
            assert skill == 3 and (order_change_img is not None or order_change is not None), \
                ('order_change', skill, order_change_img)
        # assert (friend, enemy, order_change).count(None) <= 2, (friend, enemy, order_change)
        s = f' to friend {friend}' if friend else f' to enemy {enemy}' if enemy \
            else f' order change {order_change}' if order_change else ''
        logger.debug(f'Master skill {skill}{s}.')

        before = self.wave_a
        region = self.LOC.master_skills[skill - 1]
        if enemy is not None:
            click(self.LOC.enemies[enemy - 1])
        flag = 0
        while True:
            if flag % 3 == 0:
                click(self.LOC.master_skill)
            flag += 1
            time.sleep(0.6)
            if compare_regions(screenshot(), before, region, at=True):
                break

        if friend is not None:
            # it should also match the saved screenshot, but...
            time.sleep(0.3)
            click(self.LOC.skill_to_target[friend - 1])
        elif order_change is not None:
            wait_which_target(order_change_img, self.LOC.order_change[0])
            click(self.LOC.order_change[order_change[0] - 1])
            click(self.LOC.order_change[order_change[1] - 1])
            click(self.LOC.order_change_confirm)
            wait_which_target(before, self.LOC.master_skill)
            pass
        wait_which_target(before, self.LOC.master_skill)
        return self

    def auto_attack(self, nps: Union[List[int], int] = None, mode='dmg', parse_np=False, allow_unknown=False,
                    no_play_card=False):
        """
        :param parse_np:
        :param nps:
        :param mode: dmg/xjbd/alter
        :param allow_unknown: if parse cards failed(more than 5s), just chose cards[1,2,3]
        :param no_play_card: if True, return chosen_cards but no to play cards automatically.
        :return: Optional, chosen_cards
        """
        t0 = time.time()
        if mode == 'xjbd':
            # xjbd without nps
            self.attack([1, 2, 3])
            return
        while not compare_regions(screenshot(), self.T.cards1, self.LOC.cards_back):
            click(self.LOC.attack, lapse=0.2)  # self.LOC.attack should be not covered by self.LOC.cards_back
            time.sleep(0.2)
        while True:
            time.sleep(1)
            cards, np_cards = self.parse_cards(screenshot(), nps=nps if parse_np else None)
            # print('in auto_attack: ', cards, np_cards)
            chosen_cards = []
            if cards == {}:
                if time.time() - t0 > 5 and allow_unknown or self.templates == {}:
                    # if lapse>3s, maybe someone has been died
                    chosen_cards = convert_to_list(nps)
                    chosen_cards.extend([1, 2, 3])
                    logger.debug('unrecognized cards, choose [1,2,3]')
                    chosen_cards = chosen_cards[0:3]
                    break
                else:
                    continue
            else:
                chosen_cards = self.choose_cards(cards, np_cards, nps, mode=mode)
                break
        if no_play_card is True:
            return chosen_cards
        else:
            self.play_cards(chosen_cards)

    def attack(self, locs_or_cards: Union[List[Card], List[int]]):
        assert len(locs_or_cards) >= 3, locs_or_cards
        while True:
            click(self.LOC.attack, lapse=0.2)
            if compare_regions(screenshot(), self.T.cards1, self.LOC.cards_back):
                time.sleep(1)
                self.play_cards(locs_or_cards)
                break

    def play_cards(self, cards: Union[List[Card], List[int]]):
        """
        :param cards: list of locs or cards
        :return:
        """
        cards_str_list = self.str_cards(cards)
        if len(cards) < 3:
            print(f'warning! Less then 3 cards to play: {cards_str_list}')
        if isinstance(cards[0], Card) and len(cards) >= 3 and cards[0].svt == cards[1].svt == cards[2].svt:
            cards_str_list.append('Extra')

        logger.debug(f'Attack cards: {cards_str_list}')
        locs: List[int] = [c.loc if isinstance(c, Card) else c for c in cards]
        for loc in locs:
            # print(f'click card {loc}')
            click(self.LOC.cards[loc - 1])
            time.sleep(0.2)

    def xjbd(self, target, regions, mode='dmg', turns=100, allow_unknown=False, nps=None):
        # type:(Union[Image.Image,Sequence[Image.Image]],Sequence,str,int,bool,Union[int,Sequence])->int
        if isinstance(regions[0], (int, float)):
            regions = [regions]
        cur_turn = 0
        while cur_turn < turns:
            shot = screenshot()
            if compare_regions(shot, target, regions):
                # this part must before elif part
                return cur_turn
            elif compare_regions(shot, self.T.wave1a, self.LOC.master_skill):
                cur_turn += 1
                logger.debug(f'xjbd: turn {cur_turn}/{turns}.')
                time.sleep(1)
                if nps is not None:
                    nps = convert_to_list(nps)
                    while not compare_regions(screenshot(), self.T.cards1, self.LOC.cards_back):
                        # self.LOC.attack should be not covered by self.LOC.cards_back
                        click(self.LOC.attack, lapse=0.2)
                        time.sleep(0.2)
                    self.play_cards(nps)
                self.auto_attack(mode=mode, allow_unknown=allow_unknown)
                # self.attack([1, 2, 3])
            else:
                continue

    # assistant functions
    def parse_cards(self, img: Image.Image, nps: List[int] = None) -> Tuple[Dict[int, Card], Dict[int, Card]]:
        """
        recognize the cards of current screenshot
        :param img:
        :param nps: which servants' np **MUST** be found. you'd better not set it.
        :return: location-card(svt*10+color) pair dictionary
        """
        # TODO: if xjbd, someone is dead, should allow unrecognized cards(card code could be -1).
        # assert self.templates != {}, 'Please set cards templates first!!!'
        if self.templates == {}:
            return {}, {}
        nps = convert_to_list(nps)
        base_line = -1

        def traverse(outer, mode):
            # mode=0-all,1-common card,2-np card
            nonlocal base_line
            threshold = 0.7
            _matched = -1
            max_th = 0
            values = []
            for key, templ in self.templates.items():
                _svt, _color = key // 10, key % 10
                if mode == 1 and _color == 0:
                    continue
                elif mode == 2 and _color != 0:
                    continue
                for i, templ_child in enumerate(templ):
                    if base_line > 0:
                        # enhancement: from 0.95s->0.7s....
                        box = (0, max([0, base_line - 10]),
                               outer.size[0], min([base_line + templ_child.size[1] + 10, outer.size[1]]))
                        cropped_outer = outer.crop(box)
                    else:
                        cropped_outer = outer
                    th, pos = search_target(cropped_outer, templ_child)
                    values.append(th)
                    if th > threshold and th > max_th:
                        if base_line < 0:
                            base_line = pos[1]
                        max_th = th
                        _matched = key
            # if _matched < 0:
            #     print(f'max matched value: {max(values):.4f}.')
            return _matched

        cards, np_cards = {}, {}
        for loc in range(1, 6):  # 5 common card
            base_line = -1  # reset every card
            matched = traverse(img.crop(self.LOC.cards_outer[loc - 1]), 1)
            # print(f'\n---------end card {loc}')
            if matched == -1:
                return {}, {}  # 5 command card must be matched
            else:
                cards[loc] = Card(loc, matched)
        for loc in range(6, 9):
            base_line = -1  # reset every card
            matched = traverse(img.crop(self.LOC.cards_outer[loc - 1]), 2)
            if matched != -1:
                np_cards[loc] = Card(loc, matched)
        if not set(nps).issubset(set(np_cards.keys())):
            # print(f'nobel phantasm not recognized:{nps} not in {list(np_cards.keys())}\r', end='')
            return {}, {}
        logger.debug(f'Parsed: cards={self.str_cards(cards)}, np_cards={self.str_cards(np_cards)}')
        return cards, np_cards

    def choose_cards(self, cards, np_cards, nps=None, mode='dmg'):
        # type:(Dict[int,Card],Dict[int,Card],Union[List[int],int],str)->List[Card]
        """
        :param cards:loc 1~5 {loc+1:svt*10+color}
        :param np_cards:
        :param nps: chosen nps to attack (6~8).
        :param mode: dmg,np
        :return: locations of chosen cards
        """
        nps = convert_to_list(nps)
        chosen_nps = [np_cards.get(_np, Card(_np, (_np - 5) * 10)) for _np in nps]
        s_cards = sorted(cards.values(), key=lambda o: self.weights.get(o.code, 0))

        if mode == 'dmg':
            if not chosen_nps:
                for i in (-3, -2, -1, 1, 0):
                    if s_cards[i].color == Card.BUSTER:
                        s_cards[i], s_cards[-3] = s_cards[-3], s_cards[i]
                        break
                chosen_cards = s_cards[-3:]
            else:
                chosen_nps.extend(s_cards[2 + len(chosen_nps):5])
                chosen_cards = chosen_nps
        elif mode == 'alter':
            s_cards.reverse()
            for i in (1, 2, 3, 4):
                if s_cards[i].svt != s_cards[0].svt:
                    popped = s_cards.pop(i)
                    s_cards.insert(1, popped)
            for i in (2, 3, 4):
                if s_cards[i].svt != s_cards[1].svt:
                    popped = s_cards.pop(i)
                    s_cards.insert(2, popped)
            if not chosen_nps:
                chosen_cards = s_cards[0:3]
            else:
                chosen_nps.extend(s_cards)
                chosen_cards = chosen_nps[0:3]
        elif mode == 'np':
            # TODO: gain np mode
            chosen_nps.extend(s_cards)
            chosen_cards = chosen_nps
        else:
            raise KeyError(f'Invalid mode "{mode}"')
        logger.debug(f'chosen cards: {self.str_cards(chosen_cards)}')
        return chosen_cards

    def str_cards(self, cards: Union[List[Card], Dict[int, Card], List[int]]) -> List[Union[str, int]]:
        if isinstance(cards, dict):
            cards: List[Card] = list(cards.values())
            cards.sort(key=lambda c: c.loc)
        elif isinstance(cards[0], int):
            return cards
        s = []
        # print('ready to print cards:', cards)
        for card in cards:
            s.append(self.svt_names[card.svt - 1] + '-' + '宝QAB'[card.color])
        return s

    # set battle data in self.set_battle_data()
    def set_card_templates(self, locs: List):
        """
        parse card templates from cards[1~3].png file. regions using inner boundary `self.LOC.cards`
        :param locs: locations(tmpl:1~3, card:1~5 6~8) of  [svt1:[np, Q, A, B], svt2:...], loc=-1 if no card
        """
        self.templates = {}
        templs: List[Image.Image] = self.T.cards
        for svt, svt_loc in enumerate(locs):
            for color, loc in enumerate(svt_loc):
                if isinstance(loc[0], int):
                    loc = [loc, ]
                for loc_i in loc:
                    if 0 < loc_i[1] <= 8:
                        card_id = (svt + 1) * 10 + color
                        if card_id not in self.templates:
                            self.templates[card_id] = []
                        self.templates[card_id].append(
                            templs[loc_i[0] - 1].crop(self.LOC.cards[loc_i[1] - 1]))

    def set_card_weights(self, weights: List, color_weight: str = 'QAB'):
        """
        key:svt*10+color, value:weight
        :param weights: <6*3, M-servants, 3-quick/art/buster; or 6*1.
        :param color_weight: used when weight size is <6*1
        """
        self.weights = {}
        if isinstance(weights[0], (int, float)):
            wq, wa, wb = color_weight.find('Q') + 1, color_weight.find('A') + 1, color_weight.find('B') + 1
            assert wq > 0 and wa > 0 and wb > 0, color_weight
            for i, w in enumerate(weights):
                self.weights[(i + 1) * 10 + 1] = w * 10 + wq
                self.weights[(i + 1) * 10 + 2] = w * 10 + wa
                self.weights[(i + 1) * 10 + 3] = w * 10 + wb
        else:
            for i, ww in enumerate(weights):
                for j, w in enumerate(ww):
                    self.weights[(i + 1) * 10 + 1 + j] = w


# noinspection PyPep8Naming,DuplicatedCode
class BattleBase:
    def __init__(self):
        self.master = Master()

    @with_goto
    def start(self, battle_func, battle_num, apples=None):
        T = self.master.T
        LOC = self.master.LOC
        timer = Timer()
        battle_func(True)
        BaseConfig.img_net = T.net_error
        BaseConfig.loc_net = LOC.net_error
        BaseConfig.task_finished = False
        finished_num = 0
        actual_max_num = min(battle_num, config.max_finished_battles - config.finished_battles)
        while finished_num < actual_max_num:
            finished_num += 1
            logger.info(f'>>>>> Battle "{self.master.quest_name}" No.{finished_num}/{actual_max_num} <<<<<')
            if config.jump_start:
                config.jump_start = False
                logger.warning('in start: goto label.g')
                # noinspection PyStatementEffect
                goto.g
            if not config.jump_battle:
                while True:
                    shot = screenshot()
                    res = search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))
                    if res[0] > THR:
                        click(LOC.quest_c)
                    elif is_match_target(shot, T.apple_page, LOC.apple_page):
                        if self.master.eat_apple(apples) is False:
                            return
                    elif is_match_target(shot, T.bag_full_alert, LOC.bag_full_sell_action):
                        # usually used in hunting events.
                        logger.info('bag full, to sell...')
                        click(LOC.bag_full_sell_action)
                        self.sell(1)
                        break
                    elif is_match_target(shot, T.support, LOC.support_refresh):
                        break
                    time.sleep(0.5)
            battle_func()
            wait_which_target(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            dt = timer.lapse()
            logger.info(f'--- Battle {finished_num}/{actual_max_num} finished,'
                        f' time = {int(dt // 60)} min {int(dt % 60)} sec.'
                        f' (total {config.finished_battles})')
            rewards = screenshot()
            craft_dropped = is_match_target(rewards, T.rewards, LOC.finish_craft)
            png_fn = f'img/_drops/rewards-{self.master.quest_name}-{time.strftime("%m%d-%H%M")}'
            if craft_dropped and config.check_drop:
                config.count_battle(True)
                logger.warning(f'{config.craft_num}th craft dropped!!!')
                rewards.save(f'{png_fn}-drop{config.craft_num}.png')
                if config.craft_num in config.enhance_craft_nums:
                    send_mail(f'NEED Enhancement! {config.craft_num}th craft dropped!!!')
                    logger.warning('need to change party or enhance crafts. Exit.')
                    BaseConfig.task_finished = True
                    return
                else:
                    send_mail(f'{config.craft_num}th craft dropped!!!')
            else:
                config.count_battle(False)
                rewards.save(f"{png_fn}.png")
            # ready to restart a battle
            click(LOC.finish_next)
            while True:
                shot = screenshot()
                if search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))[0] > THR:
                    break
                elif is_match_target(shot, T.restart_quest, LOC.restart_quest_yes):
                    click(LOC.restart_quest_yes)
                    logger.debug('restart the same battle')
                    break
                elif is_match_target(shot, T.apply_friend, LOC.apply_friend):
                    click(LOC.apply_friend_deny)
                    logger.debug('not to apply friend')
                time.sleep(0.5)
            # noinspection PyStatementEffect
            label.g
        BaseConfig.task_finished = True
        logger.info(f'>>>>> All {finished_num} battles "{self.master.quest_name}" finished. <<<<<')
        if config.mail:
            send_mail(f'All {finished_num} battles "{self.master.quest_name}" finished')

    @with_goto
    def battle_template(self, pre_process=False):
        """
        template procedure of a battle.
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'template'
        T.read_templates('img/template-jp')
        master.svt_names = ['X', 'Y', 'Z']
        if pre_process:
            return

        # battle part
        master.set_card_weights([2, 3, 1])
        # ----  NP     Quick    Arts   Buster ----
        # master.set_card_templates([
        #     [(1, 6), (3, 3), (2, 3), (1, 2)],
        #     [(3, 7), (1, 4), (1, 1), (2, 4)],
        #     [(1, 0), (2, 1), (2, 2), (1, 3)],
        # ])
        if config.jump_battle:
            config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        # noinspection PyStatementEffect
        label.h
        wait_which_target(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support_drag(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                                       switch_classes=(-1,))
        else:
            logger.debug('please choose support manually!')
        time.sleep(2)
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[0])
        logger.debug(f'Quest {master.quest_name} started...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(1, 1)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_which_target(T.wave2a, LOC.enemies[0])
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(1, 3)
        # master.attack([6, 1, 2])
        click(LOC.enemies[1])
        chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        # master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        # master.attack([6, 1, 2])
        master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    def sell(self, num=100):
        """
        Called when bag full before entering quest, usually hunting events. Back to supporting finally.
        :param num: selling times. 100~=ALL
        """
        T = self.master.T
        LOC = self.master.LOC
        logger.info('shop: selling...')
        print('Make sure the bag **FILTER** only shows "Experience Cards"/"Zhong Huo"!')
        no = 0
        while True:
            wait_which_target(T.bag_unselected, LOC.bag_sell_action)
            drag(LOC.bag_select_start, LOC.bag_select_end, duration=1, down_time=1, up_time=4)
            page_no = wait_which_target([T.bag_selected, T.bag_unselected], [LOC.bag_sell_action, LOC.bag_sell_action])
            if page_no == 0:
                no += 1
                logger.debug(f'sell {no} times.')
                click(LOC.bag_sell_action)
                wait_which_target(T.bag_sell_confirm, LOC.bag_sell_confirm, at=True)
                wait_which_target(T.bag_sell_finish, LOC.bag_sell_finish, at=True)
                if no >= num:
                    break
            elif page_no == 1:
                logger.debug('all items are sold.')
                break
        wait_which_target(T.bag_unselected, LOC.bag_sell_action)
        click(LOC.bag_back)
        wait_which_target(T.shop, LOC.shop_event_item_exchange)
        click(LOC.bag_back)
        wait_which_target(T.quest, LOC.quest_master_avatar)
        click(LOC.quest_c)
        logger.debug('from shop back to supporting')
        return
