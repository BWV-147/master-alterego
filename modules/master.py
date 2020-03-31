"""
Master class
additional, Card class included.
"""
from util.autogui import *
from util.supervisor import send_mail


class Card:
    NP = 0
    QUICK = 1
    ARTS = 2
    BUSTER = 3
    UNKNOWN = 'unknown'

    def __init__(self, svt: str, color: int, _loc: int = 0):
        assert svt and -1 <= color <= 3
        self._svt = svt
        self._color = color  # -1: unknown
        # extra data, not included in hash
        self.loc = _loc  # valid if 1~8

    @property
    def svt(self):
        return self._svt

    @property
    def color(self):
        return self._color

    def get_color_string(self):
        return ['NP', 'Quick', 'Arts', 'Buster', '?'][self.color]

    def __repr__(self):
        return f'{self.__class__.__name__}({self._svt}, {self.get_color_string()}, {self.loc})'

    def __hash__(self):
        return hash(f'{self.__class__.__name__}({self._svt}, {self.get_color_string()})')

    def __eq__(self, other):
        if type(other) == type(self):
            return other.svt == self._svt and other.color == self._color
        return False

    @staticmethod
    def find_card(cards: List, svt: str, color: int):
        """all locs of found cards"""
        locs = []
        for i, card in enumerate(cards):
            if card.svt == svt and card.color == color:
                locs.append(i)
        return locs


class Master:
    def __init__(self, quest=''):
        self.quest_name = quest
        # realtime member list, auto-update with order-change, but Arash/Chen Gong need to update manually.
        self.members = list('ABCDEF')
        self.T = ImageTemplates()
        self.LOC = Regions()
        self.card_templates: Dict[Card, List[Image.Image]] = {}
        self.card_weights: Dict[Card, float] = {}
        self.wave_a = None
        self.wave_b = None

    def set_card_template(self, svt_name: str, card_loc: List = None, json_fp: str = None, json_key: str = None):
        """
        use `card_loc` or `json_fp`, not together.
        :param svt_name: svt name
        :param card_loc: list length of 4: NP-Quick-Arts-Buster.
                        For every item: tuple or list of tuple(multiple templates):
                        tuple(0): int or str, if int i, i -> f"cards{i}".
                        tuple(1): int, location of card, 1~5 + 6~8(NP)
        :param json_fp: a json dict which stores serials of {name: card_loc}.
                        Json file and images should be in the same folder.
        :param json_key: key in json, default is `name`
        :return:
        """
        assert card_loc is None or json_fp is None, "don't use 'card_loc' and 'json_fp' together."
        if json_fp is not None:
            import json
            json_key = json_key or svt_name
            _folder = os.path.dirname(os.path.abspath(json_fp))
            card_loc = json.load(open(json_fp, encoding='utf8'))[json_key]
            images = ImageTemplates(_folder)
            # for fn in os.listdir(_folder):
            #     if fn.lower().endswith('.png'):
            #         images[fn[:-4]] = Image.open(os.path.join(_folder, fn))
        else:
            images = self.T
        for color, locs in enumerate(card_loc):
            _templates = []
            if locs and isinstance(locs[-1], int):
                # only one loc, not a list of loc
                locs = [locs]
            for img_name, loc in locs:
                if isinstance(img_name, int):
                    img_name = f'cards{img_name}'
                _templates.append(images.get(img_name).crop(self.LOC.cards[loc - 1]))
            self.card_templates[Card(svt_name, color)] = _templates

        pass

    def set_card_weight(self, weights: Dict[str, Union[float, List[float]]], color_weight: str = 'QAB'):
        """
        key:svt*10+color, value:weight
        :param weights: <6*3, M-servants, 3-quick/art/buster; or 6*1.
        :param color_weight: used when weight size is <6*1
        """
        color_weight = color_weight.upper()
        assert 'ABQ' == ''.join(sorted('QAB')), f'invalid color_weight: {color_weight}'
        self.card_weights.clear()
        for svt, ww in weights.items():
            if isinstance(ww, Sequence):
                for i, w in enumerate(ww):
                    self.card_weights[Card(svt, i + 1)] = w
            else:
                # number, default w*10+0/1/2
                for i in range(3):
                    self.card_weights[Card(svt, i + 1)] = ww * 10 + color_weight.find('QAB'[i])

    @staticmethod
    def str_cards(cards):
        # type: (Union[List[Union[int, Card]], Union[int, Card], Dict[int, Card]])->Union[str,List[str]]
        if isinstance(cards, dict):
            # from parsed cards
            cards: List[Card] = list(cards.values())
            cards.sort(key=lambda _c: _c.loc)

        def _str_card(_c):
            if isinstance(_c, Card):
                return _c.svt + '-' + '宝QAB?'[_c.color]
            else:
                return str(_c)

        if isinstance(cards, Sequence):
            return [f'({_str_card(c)})?' if i >= 3 else _str_card(c) for i, c in enumerate(cards)]
        else:
            return _str_card(cards)

    # battle procedures
    def eat_apple(self, apples=None):
        apples = convert_to_list(apples)
        if config.is_jp is True and config.battle.login_handler is None:
            t = time.localtime()
            if t.tm_hour == 2 and t.tm_min > 45:
                logger.info('Around 3am, stop eating apples and battles.')
                config.mark_task_finish()
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

                    # noinspection DuplicatedCode

        logger.info(f'apples={apples}, don\'t eat apple or no left apples, task finish.')
        config.mark_task_finish()

    # noinspection DuplicatedCode
    def choose_support(self, match_svt=True, match_ce=False, match_ce_max=False, match_skills=None, img=None,
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
        logger.debug('choosing support (drag mode)...')
        support_page = self.T.support if img is None else img
        if switch_classes is None:
            switch_classes = (-1,)
        wait_which_target(support_page, self.LOC.support_refresh)
        while np.mean(get_mean_color(screenshot(), LOC.loading_line)) > 200:
            time.sleep(0.2)
        refresh_times = 0

        def _is_match_offset(_shot, old_loc, _offset):
            return is_match_target(_shot.crop(np.add(old_loc, [0, _offset, 0, _offset])), T.support.crop(old_loc))

        while True:
            wait_which_target(support_page, self.LOC.support_class_affinity, lapse=0.5)
            for icon in switch_classes:
                if icon == -1:
                    time.sleep(0.2)
                else:
                    click(self.LOC.support_class_icons[icon], 0.5)
                    logger.debug(f'switch support class to No.{icon}.')
                pyautogui.moveTo(*LOC.support_scrollbar_start)
                if is_match_target(screenshot(), T.support, LOC.support_scrollbar_head, 0.8) \
                        and np.mean(T.support.getpixel(get_center_coord(LOC.support_scrollbar_head))) > 200:
                    drag_points = 5
                    dy_mouse = (LOC.support_scrollbar_end[1] - LOC.support_scrollbar_start[1]) // (drag_points - 1)
                else:
                    drag_points = 1
                    dy_mouse = 0
                for drag_point in range(drag_points):
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
                            logger.debug('found support.')
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
                    if dy_mouse != 0:
                        time.sleep(0.2)
                        pyautogui.dragRel(0, dy_mouse, 0.2)
            # refresh support
            refresh_times += 1
            logger.debug(f'refresh support {refresh_times} times')
            if refresh_times % 40 == 0:
                send_mail(body=f'refresh support more than {refresh_times} times.')
            wait_which_target(support_page, self.LOC.support_refresh, at=True)
            wait_which_target(self.T.support_confirm, self.LOC.support_confirm_title, clicking=self.LOC.support_refresh)
            click(self.LOC.support_refresh_confirm, lapse=1)

    def svt_skill_full(self, before, after, who, skill, friend=None, enemy=None):
        # type: (Image.Image,Image.Image,int,int,int,int)->None
        """
        Release servant skill to <self/all friends/all enemies>.
        :param before: image before the skill released.
        :param after: image after the skill released. if null, not to check.
        :param who: who to release the skill.value in [left=1,mid=2,right=3], the same below.
        :param skill: which skill to release.
        :param friend: which friend
        :param enemy: which enemy
        :return: None
        """
        # validation
        valid1, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert who in valid1 and skill in valid1 and friend in valid2 and enemy in valid2, (who, skill, friend, enemy)
        s = f' to friend {self.members[friend - 1]}' if friend \
            else f' to enemy {enemy}' if enemy else ''
        logger.debug(f'Servant skill: {self.members[who - 1]}-{skill}{s}.')

        # start
        if enemy is not None:
            click(self.LOC.enemies[enemy - 1])
        region = self.LOC.skills[who - 1][skill - 1]
        # wait_which_target(self.T.wave1a, self.LOC.master_skill)
        wait_which_target(before, region, at=True)
        while is_match_target(screenshot(), before, region):
            # some times need to
            click(region)
        if friend is not None:
            # it should also match the saved screenshot, but...
            # TODO: match select target shot, same as master_skill
            time.sleep(0.5)
            click(self.LOC.skill_to_target[friend - 1])
        if after is not None:
            wait_which_target(after, region)

    def set_waves(self, before: Image.Image, after: Image.Image = None):
        """set wave a/b before every wave start, also for order change/stella/jump_battle """
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
        s = f' to friend {self.members[friend - 1]}' if friend else f' to enemy {enemy}' if enemy \
            else f' order change {[self.members[i - 1] for i in order_change]}' if order_change else ''
        logger.debug(f'Master skill {skill}{s}.')
        if order_change:
            _temp = self.members[order_change[1] - 1]
            self.members[order_change[1] - 1] = self.members[order_change[0] - 1]
            self.members[order_change[0] - 1] = _temp
            logger.debug(f'After order change: {self.members}')

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

    def goto_parse_cards(self):
        t0 = time.time()
        while True:
            shot = screenshot()
            if is_match_target(shot, self.T.wave1a, self.LOC.attack):
                click(self.LOC.attack)
            elif is_match_target(shot, self.T.cards1, self.LOC.cards_back):
                break
        time.sleep(1)
        while True:
            cards, np_cards = self.parse_cards(screenshot())
            if cards == {} or Card.UNKNOWN in [c.svt for c in cards.values()]:
                if time.time() - t0 > 5 or self.card_templates == {}:
                    break
        return cards, np_cards

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
        while not compare_regions(screenshot(), self.T.cards1, self.LOC.cards_back):
            click(self.LOC.attack, lapse=0.3)  # self.LOC.attack should be not covered by self.LOC.cards_back
        while True:
            cards, np_cards = self.parse_cards(screenshot(), nps=nps if parse_np else None)
            # print('in auto_attack: ', cards, np_cards)
            chosen_cards = []
            if cards == {} or Card.UNKNOWN in [c.svt for c in cards.values()]:
                if time.time() - t0 > 5 and allow_unknown or self.card_templates == {}:
                    # if lapse>3s, maybe someone has been died
                    chosen_cards = self.choose_cards(cards, np_cards, nps, mode=mode)
                    logger.debug(f'unrecognized: {[f"{self.str_cards(c)}" for c in cards.values()]},'
                                 f' np_cards={self.str_cards(np_cards)}')
                    break
                else:
                    continue
            else:
                chosen_cards = self.choose_cards(cards, np_cards, nps, mode=mode)
                break
        if no_play_card is False:
            if nps is not None:
                time.sleep(0.8)
            self.play_cards(chosen_cards)
        return chosen_cards

    def xjbd(self, target, regions, mode='dmg', turns=100, allow_unknown=False, nps=None):
        # type:(Union[Image.Image,Sequence[Image.Image]],Sequence,str,int,bool,Union[int,Sequence])->List[List]
        if not isinstance(regions[0], Sequence):
            regions = [regions]
        cur_turn = 0
        turn_cards = []
        while cur_turn < turns:
            shot = screenshot()
            if compare_regions(shot, target, regions):
                # this part must before elif part
                if cur_turn > 0:
                    logger.debug(f'xjbd total {cur_turn} turns')
                return turn_cards
            elif compare_regions(shot, self.T.wave1a, self.LOC.master_skill):
                cur_turn += 1
                logger.debug(f'xjbd: turn {cur_turn}/{turns}.')
                time.sleep(1)
                chosen_cards = self.auto_attack(mode=mode, nps=nps, allow_unknown=allow_unknown)
                # self.attack([1, 2, 3])
                turn_cards.append(chosen_cards)
            else:
                continue

    # usually assist for methods above
    def attack(self, locs_or_cards: Union[List[Card], List[int]]):
        assert len(locs_or_cards) >= 3, locs_or_cards
        while True:
            click(self.LOC.attack, lapse=0.2)
            if compare_regions(screenshot(), self.T.cards1, self.LOC.cards_back):
                time.sleep(1)
                self.play_cards(locs_or_cards)
                break

    def parse_cards(self, img: Image.Image, nps: List[int] = None) -> Tuple[Dict[int, Card], Dict[int, Card]]:
        """
        recognize the cards of current screenshot
        :param img:
        :param nps: which servants' np **MUST** be found. you'd better not set it.
        :returns cards and np_cards, location-card(svt*10+color) pair dictionary, np_cards may less then actual
        """
        if self.card_templates == {}:
            return {}, {}
        nps = convert_to_list(nps)
        base_line = -1

        def _traverse(outer, mode):
            # mode=0-all,1-common card,2-np card
            nonlocal base_line  # to decrease time of `search_target()`
            threshold = 0.7
            _matched = None
            max_th = 0
            values = []
            for card, templates in self.card_templates.items():
                # _svt, _color = key // 10, key % 10
                if mode == 1 and card.color == Card.NP:
                    continue
                elif mode == 2 and card.color != Card.NP:
                    continue
                for template in templates:
                    if base_line > 0:
                        # enhancement: from 0.95s->0.7s....
                        box = (0, max([0, base_line - 10]),
                               outer.size[0], min([base_line + template.size[1] + 10, outer.size[1]]))
                        cropped_outer = outer.crop(box)
                    else:
                        cropped_outer = outer
                    th, pos = search_target(cropped_outer, template)
                    values.append(th)
                    if th > threshold and th > max_th:
                        if base_line < 0:
                            base_line = pos[1]
                        max_th = th
                        _matched = Card(card.svt, card.color)
            # if _matched < 0:
            #     print(f'max matched value: {max(values):.4f}.')
            return _matched

        cards, np_cards = {}, {}
        for loc in range(1, 9):
            base_line = -1  # reset every card
            matched = _traverse(img.crop(self.LOC.cards_outer[loc - 1]), 1 if loc <= 5 else 2)
            if matched is None:
                matched = Card(Card.UNKNOWN, -1, loc)
            else:
                matched.loc = loc
            if loc <= 5:
                cards[loc] = matched
            else:
                np_cards[loc] = matched
        for x in [cards, np_cards]:
            if False not in [card.svt == Card.UNKNOWN for card in x.values()]:
                # all cards are not recognized.
                x.clear()
        if not set(nps).issubset(set(np_cards.keys())):
            # print(f'nobel phantasm not recognized:{nps} not in {list(np_cards.keys())}\r', end='')
            np_cards.clear()
            # return {}, {}
        logger.debug(f'Parsed: {[f"{self.str_cards(c)}" for c in cards.values()]},'
                     f' np_cards={self.str_cards(np_cards)}')
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
        if len(cards) < 5:
            logger.warning(f'in choose_cards: cards count less then 5! {cards}')
        mode = mode.lower()
        nps = convert_to_list(nps)
        chosen_nps = [np_cards.get(_np, Card(f'UNKNOWN{_np}', 0, _np)) for _np in nps]
        if mode == 'xjbd':
            s_cards = sorted(cards.values(), key=lambda _c: _c.loc)
            chosen_cards = s_cards[0:3]
        else:
            s_cards = sorted(cards.values(), key=lambda _c: self.card_weights.get(_c, 0))
            if mode == 'dmg':
                if len(chosen_nps) > 0:
                    chosen_cards = [s_cards[i] for i in (-2, -1, -3)]
                else:
                    for i in (-3, -2, -1, 1, 0):
                        if s_cards[i].color == Card.BUSTER:
                            s_cards[i], s_cards[-3] = s_cards[-3], s_cards[i]
                            break
                    chosen_cards = s_cards[-3:]
            elif mode == 'alter':
                s_cards.reverse()
                chosen_cards = [s_cards.pop(0)]
                for i in range(2):
                    for j, c in enumerate(s_cards):
                        if c.svt != chosen_cards[-1].svt:
                            chosen_cards.append(s_cards.pop(j))
                            break
                chosen_cards = (chosen_cards + s_cards)[0:3]
            else:
                raise KeyError(f'Invalid mode "{mode}"')
        chosen_cards = chosen_nps + chosen_cards[0:3]
        logger.debug(f'chosen cards: {self.str_cards(chosen_cards)}')
        return chosen_cards

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
            click(self.LOC.cards[loc - 1], lapse=0.3)
