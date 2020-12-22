"""
Master class
additional, Card class included.
"""
import contextlib
import enum

from util.addon import *
from util.autogui import *


class Card:
    NP = 0
    QUICK = 1
    ARTS = 2
    BUSTER = 3
    UNKNOWN = 'who'

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

    @property
    def color_string(self):
        return ['NP', 'Quick', 'Arts', 'Buster', '?'][self.color]

    def __repr__(self):
        return f'{self.__class__.__name__}({self._svt}, {self.color_string}, {self.loc})'

    def __hash__(self):
        return hash(f'{self.__class__.__name__}({self._svt}, {self.color_string})')

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


class AttackMode(enum.Enum):
    damage = 1
    alter = 2
    gaining_np = 3
    xjbd = 4


class Master:
    def __init__(self, quest=''):
        self.quest_name = quest
        # realtime member list, auto-update with order-change, but Arash/Chen Gong need to update manually.
        self.members: List[str] = list('ABCDEF')
        self.T = ImageTemplates()
        # initiate inside BattleBase after pre_process
        self.LOC: Optional[Regions] = None
        self.card_templates: Dict[Card, List[Image.Image]] = {}
        self.card_weights: Dict[Card, float] = {}
        self._wave_a = None
        self._wave_b = None

    def set_cards(self, svt, np, quick, arts, buster, images=None):
        # type:(str,Sequence,Sequence,Sequence,Sequence,ImageTemplates)->None
        """
        Set card templates from images.
        np/quick/arts/buster: (img, loc) or list of (img, loc).
                img - could be filename(without ".png") or int (e.g. "1" = "cards1").
                loc - should be 1~8, or it'll be ignored.
        images: ImageTemplates, default is `self.T`. Needed if data loaded from json
        """
        if images is None:
            images = self.T
        for color, locs in enumerate([np, quick, arts, buster]):
            _templates = []
            if locs and isinstance(locs[-1], int):
                # only one loc, not a list of loc
                locs = [locs]
            for img_name, loc in locs:
                if loc > 8 or loc < 1:
                    continue
                if isinstance(img_name, int):
                    img_name = f'cards{img_name}'
                _templates.append(images.get(img_name).crop(self.LOC.cards[loc - 1]))
            self.card_templates[Card(svt, color)] = _templates

    def set_cards_from_json(self, svt: str, fp: str, key: str = None):
        """
        Read card templates from outside folder(within json file and images).

        :param svt: svt name
        :param fp: json file path. Json file and images should be in the same folder.
                default `img/share/{device}/cards/cards.json`.
                two equivalent format (here TYPE=NP/Buster/Arts/Quick):
                - {"svt": {"TYPE":"a1-1,a2-2,a3-3"}}.
                - {"svt": {"prefix":"a","TYPE":"1-1,2-2,3-3"}}.
                in which "a1-1,..." is serials of (img, loc).
        :param key: svt key in json, default is `svt`
        :return:
        """
        import json
        key = key or svt
        fp2 = f'img/share/{fp}/cards/cards.json'
        if not os.path.exists(fp) and os.path.exists(fp2):
            fp = fp2
        _folder = os.path.dirname(os.path.abspath(fp))
        data: Dict[str, str] = json.load(open(fp, encoding='utf8'))[key]
        prefix = data.get('prefix', '')
        params = []
        for card in ('NP', 'Quick', 'Arts', 'Buster'):
            params.append([])
            pairs_str = data[card]
            for pair in pairs_str.split(','):
                img, loc = pair.split('-')
                img = prefix + img
                loc = int(loc)
                params[-1].append([img, loc])
        self.set_cards(svt, *params, images=ImageTemplates(_folder))

    def set_card_weight(self, weights: Union[Sequence, Dict[str, Union[float, List]]], color_weight: str = 'QAB'):
        """
        :param weights: [names,weights] or {name:weights}.
        :param color_weight: used when weight size
        """
        if isinstance(weights, Sequence):
            assert len(weights[0]) == len(weights[1]), weights
            weights = dict([(x, y) for x, y in zip(weights[0], weights[1])])
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

    def svt_die(self, svt: int):
        assert svt in (1, 2, 3)
        svt -= 1
        svt_name = self.members[svt]
        if len(self.members) <= 3:
            self.members[svt] = 'NoBody'
        else:
            self.members.pop(svt)
            self.members.insert(svt, self.members.pop(2))
        logger.debug(f'{svt_name} is dead, current party: {self.members}')

    def str_cards(self, cards):
        # type: (Union[List[Union[int, Card]], Union[int, Card], Dict[int, Card]])->Union[str,List[str]]
        if isinstance(cards, dict):
            # from parsed cards
            cards: List[Card] = list(cards.values())
            cards.sort(key=lambda _c: _c.loc)

        def _str_card(_c):
            if isinstance(_c, Card):
                if _c.svt.startswith(Card.UNKNOWN) and 5 < _c.loc <= 8:
                    return self.members[_c.loc - 6] + '-宝?'
                return _c.svt + '-' + '宝QAB?'[_c.color]
            else:
                if 5 < _c <= 8:
                    return self.members[_c - 6] + '-宝?'
                return str(_c)

        if isinstance(cards, Sequence):
            return [f'({_str_card(c)})?' if i >= 3 else _str_card(c) for i, c in enumerate(cards)]
        else:
            return _str_card(cards)

    # battle procedures
    def eat_apple(self, apples=None):
        T, LOC = self.T, self.LOC
        apples = convert_to_list(apples)
        if not apples:  # empty list
            apples = [-1]
        if config.is_jp is True and not callable(config.battle.login_handler):
            t = time.localtime()
            if t.tm_hour == 2 and t.tm_min > 45:
                logger.info('Around 3am, stop eating apples and battles for jp server.')
                config.mark_task_finish()
                config.kill()
        for apple in apples:
            if apple == 0:  # 不舍得吃彩苹果
                # apple = 3
                pass
            if apple not in (0, 1, 2, 3, 4, 5):
                logger.info(f'apple={apple} ({apples}), don\'t eat apple or no left apples, task finish.')
                click(LOC.apple_close)
                config.mark_task_finish()
                config.kill()
            elif apple == 5:
                logger.debug('Choose apple manually...')
                config.update_time(420)
                wait_targets(T.support, LOC.support_refresh)
            elif apple == 4:
                # zihuiti: sleep 1 hour to check again whether ap enough
                click(LOC.apple_close)
                dt = 3600
                logger.info(f'AP recover: waiting for {dt // 60} min...')
                config.update_time(dt)
                time.sleep(dt)
                break
            elif apple in (0, 1, 2, 3):
                if match_targets(screenshot(), T.apple_page, LOC.apples[apple]):
                    eaten = False
                    while True:
                        page_no = wait_which_target([T.apple_page, T.apple_confirm, T.support],
                                                    [LOC.apples[apple], LOC.apple_confirm, LOC.support_refresh])
                        if page_no == 0:
                            if not eaten:
                                str_apple = ['Colorful', 'Gold', 'Silver', 'Cropper'][apple]
                                logger.info(f"eating {str_apple} apple...", extra=LOG_TIME)
                            eaten = True
                            click(LOC.apples[apple], lapse=1)
                        elif page_no == 1:
                            click(LOC.apple_confirm, lapse=1)
                        elif page_no == 2:
                            if apple == 0:
                                logger.set_cur_logger('quartz', 10)
                                logger.info(f'Account {config.id}: eating saint quartz as apple!')
                                logger.set_cur_logger()
                            return

    def choose_support(self, match_svt=True, match_skills=True, match_ce=False, match_ce_max=False, friend_only=False,
                       switch_classes=None, images=None):
        # type:(bool,bool,bool,bool,bool,Sequence[int],Sequence[Image.Image])->int
        """
        Choose the **first** friend in support templates `images`(default T.support) from the whole support list,
        drag scrollbar to show all friends. Finally return the index of which support template is chosen.

        :param match_svt: match the whole rect of 3 skills
        :param match_skills: match every skill icon
        :param match_ce: whether match CE, please set to False if jp server since CE could be filtered in jp server
        :param match_ce_max: whether match CE max star
        :param friend_only: only choose friends' support
        :param switch_classes: e.g. (0,5,...) means switch between ALL and CASTER.
                        If empty or None, keep current support class.
                        ALL=0, Saber-Berserker=1-7, extra=8, Mixed=9.
        :param images: support page images, default [T.support]
        :return: index of which support template in `images` is chosen
        """
        T, LOC = self.T, self.LOC
        logger.debug('choosing support...', extra=LOG_TIME)
        supports = images if images else [T.support]
        support0 = supports[0]
        if switch_classes is None:
            switch_classes = (-1,)
        wait_targets(support0, LOC.support_refresh)
        while numpy.mean(get_mean_color(screenshot(), LOC.loading_line)) > 200:
            sleep(0.2)
        refresh_times = 0

        def _is_match_offset(_support, _shot, old_loc, _offset, threshold=None):
            return match_targets(_shot.crop(numpy.add(old_loc, [0, _offset, 0, _offset])), _support.crop(old_loc),
                                 threshold=threshold)

        # lambda functions: function(support, screenshot, offset) -> matched or not
        matches = [
            lambda _p, _s, _o: not match_svt or _is_match_offset(_p, _s, LOC.support_skill[0], _o),
            lambda _p, _s, _o: not match_skills or False not in [_is_match_offset(_p, _s, loc, _o) for loc in
                                                                 LOC.support_skills[0]],
            lambda _p, _s, _o: not match_ce or _is_match_offset(_p, _s, LOC.support_ce[0], _o),
            # ce_max rect is to small, may has lower similarity
            lambda _p, _s, _o: not match_ce_max or _is_match_offset(_p, _s, LOC.support_ce_max[0], _o, 0.8),
            lambda _p, _s, _o: not friend_only or _is_match_offset(_p, _s, LOC.support_friend_icon, _o),
        ]

        while True:
            wait_targets(support0, LOC.support_class_affinity)
            for class_icon in switch_classes:
                if class_icon == -1:
                    sleep(0.2)
                else:
                    click(LOC.support_class_icons[class_icon])
                    class_name = ['All', 'Saber', 'Archer', 'Lancer', 'Rider',
                                  'Caster', 'Assassin', 'Berserker', 'Extra', 'Mix'][class_icon]
                    logger.debug(f'switch support class to No.{class_icon}-{class_name}.')
                click(LOC.support_scrollbar_start)
                shot = screenshot()
                drag_x, drag_y1 = LOC.support_scrollbar_start
                drag_y2 = LOC.support_scrollbar_end[1]
                drag_point_num = 6 if min(numpy.mean(shot.crop(LOC.support_scrollbar_head).getdata(), 0)) > 225 else 1
                drag_points = [(drag_x, drag_y1 + (drag_y2 - drag_y1) / 8 * i) for i in range(drag_point_num)]
                for i_point in range(drag_point_num):
                    shot = screenshot()
                    y_peaks = search_peaks(shot.crop(LOC.support_team_column), support0.crop(LOC.support_team_icon))
                    for y_peak in y_peaks:
                        y_offset = y_peak - (LOC.support_team_icon[1] - LOC.support_team_column[1])
                        matched = False
                        matched_support = -1
                        for support_index, support in enumerate(supports):
                            for func in matches:
                                matched = func(support, shot, y_offset)
                                if not matched:  # one condition not match-> false next support image
                                    break
                            if matched:  # one support matched
                                matched_support = support_index
                                if len(supports) > 1:
                                    logger.info(f'matched support {support_index}')
                                break
                        if not matched:  # this friend not match any support, next friend
                            continue
                        click((LOC.width / 2, LOC.support_team_column[1] + y_peak
                               + LOC.support_team_icon[3] - LOC.support_team_icon[1]))
                        logger.debug('found support.', extra=LOG_TIME)
                        while True:
                            page_no = wait_which_target([T.team, T.wave1a],
                                                        [LOC.team_cloth_button, LOC.master_skill])
                            sleep(0.3)
                            if page_no == 0:
                                logger.debug('entering battle', extra=LOG_TIME)
                                click(LOC.team_start_action)
                                click(LOC.team_start_action)
                            elif page_no == 1:
                                return matched_support
                    # no friends matched, drag downward
                    if i_point + 1 < drag_point_num:
                        drag(drag_points[i_point], drag_points[i_point + 1], 0.2)
                        sleep(0.4)
            # refresh support
            refresh_times += 1
            logger.debug(f'refresh support {refresh_times} times...', extra=LOG_TIME)
            if refresh_times % 100 == 0:
                send_mail(body=f'refresh support more than {refresh_times} times.', level=MailLevel.info)
            wait_targets(support0, LOC.support_refresh, at=0)
            wait_targets(T.support_confirm, LOC.support_confirm_title, clicking=LOC.support_refresh)
            click(LOC.support_refresh_confirm)
            wait_targets(support0, LOC.support_class_affinity, lapse=0.2)

    @contextlib.contextmanager
    def set_waves(self, before: Image.Image, after: Image.Image = None):
        """
        Usage: `with self.set_waves(before, after): pass`. Set wave_a and wave_b before every wave or
        after order change/stella.

        Don't jump_battle into with statement.
        """
        self._wave_a = before
        self._wave_b = after
        try:
            yield self
        except:  # noqas
            raise
        finally:
            self._wave_a = None
            self._wave_b = None

    def svt_skill(self, who: int, skill: int, friend: int = None, enemy: int = None, no_wait=False):
        self.svt_skill_full(self._wave_a, self._wave_b, who, skill, friend, enemy, no_wait)
        return self

    def svt_skill_full(self, before, after, who, skill, friend=None, enemy=None, no_wait=False):
        # type: (Image.Image,Image.Image,int,int,int,int,bool)->Master
        """
        Release servant skill to <self/all friends/all enemies>.
        TODO: bug fix, first skill to enemy in this wave may not set enemy correctly.

        :param before: image before the skill released.
        :param after: image after the skill released. if null, not to check.
        :param who: who to release the skill.value in [left=1,mid=2,right=3], the same below.
        :param skill: which skill to release.
        :param friend: which friend
        :param enemy: which enemy
        :param no_wait: if True, not to wait `after`
        :return: master self.
        """
        T, LOC = self.T, self.LOC
        # validation
        assert before is not None, 'provide "before" wave_a template or use inside "with set_waves()"'
        valid1, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert who in valid1 and skill in valid1 and friend in valid2 and enemy in valid2, (who, skill, friend, enemy)
        s = f' to {self.members[friend - 1]}' if friend \
            else f' to enemy {enemy}' if enemy else ''
        logger.info(f'Servant skill: {self.members[who - 1]}-{skill}{s}.', extra=LOG_TIME)

        # start
        if enemy is not None:
            click(LOC.enemies[enemy - 1])
        region = LOC.skills[who - 1][skill - 1]
        wait_targets(before, region, at=0, lapse=1)
        if friend is None:
            while match_targets(screenshot(), before, region, 0.5):
                # some times need to
                click(region, 1)
        else:
            while not match_targets(screenshot(), T.skill_targets, LOC.skill_targets_close, 0.7):
                click(region, 1)
            click(LOC.skill_to_target[friend - 1])
        if after is not None and no_wait is False:
            wait_targets(after, region)
        return self

    def master_skill(self, skill, friend=None, enemy=None, order_change=None, order_change_img=None):
        return self.master_skill_full(self._wave_a, skill, friend, enemy, order_change, order_change_img)

    def master_skill_full(self, before, skill, friend=None, enemy=None, order_change=None, order_change_img=None):
        # type:(Image.Image,int,int,int,Tuple[int,int],Image.Image)->Master
        """
        Release master skill to friend/enemy. Especially, order change if order_change is not None.

        :param before: wave a
        :param skill: 1~3
        :param friend: 1~3, from left to right
        :param enemy: 1~3, from right to left
        :param order_change: None or (svt1:1~3,svt2:4~6)
        :param order_change_img: if None, use `self.T.order_change`
        :return: master self
        """
        T, LOC = self.T, self.LOC
        assert before is not None, 'provide "before" wave_a template or use inside "with set_waves()"'
        valid, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert skill in valid and friend in valid2 and enemy in valid2, (skill, friend, enemy)
        if order_change is not None:
            assert skill == 3, f'order change: skill must be 3: {skill}'
            assert friend is None and enemy is None, f'order change: don\'t need friend/enemy param: {(friend, enemy)}'
            assert order_change[0] in (1, 2, 3) and order_change[1] in (4, 5, 6), \
                f'order change: invalid order_change: {order_change}'
            order_change_img = order_change_img or T.order_change
            assert order_change_img is not None
        s = f' to {self.members[friend - 1]}' if friend else f' to enemy {enemy}' if enemy \
            else f' order change {[self.members[i - 1] for i in order_change]}' if order_change else ''
        logger.info(f'Master skill {skill}{s}.', extra=LOG_TIME)
        if order_change:
            a, b = order_change[0] - 1, order_change[1] - 1
            self.members[a], self.members[b] = self.members[b], self.members[a]
            logger.debug(f'After order change: {self.members}', extra=LOG_TIME)

        region = LOC.master_skills[skill - 1]
        if enemy is not None:
            click(LOC.enemies[enemy - 1])
        flag = 0
        while True:
            if flag % 3 == 0:
                click(LOC.master_skill)
            flag += 1
            sleep(0.6)
            if match_targets(screenshot(), before, region):
                click(region, 0)
                break

        if friend is not None:
            # it should also match the saved screenshot, but...
            sleep(0.3)
            wait_targets(T.skill_targets, LOC.skill_targets_close, 0.7, lapse=0.3)
            click(LOC.skill_to_target[friend - 1])
        elif order_change is not None:
            # TODO: change to order_change_unselect grey button
            wait_targets(order_change_img, LOC.order_change_close)
            click(LOC.order_change[order_change[0] - 1])
            click(LOC.order_change[order_change[1] - 1])
            click(LOC.order_change_confirm)
            wait_targets(before, LOC.master_skill)
        wait_targets(before, LOC.master_skill)
        return self

    def goto_parse_cards(self):
        t0 = time.time()
        while True:
            shot = screenshot()
            if match_targets(shot, self.T.wave1a, self.LOC.attack):
                click(self.LOC.attack)
            elif match_targets(shot, self.T.cards1, self.LOC.cards_back):
                break
        sleep(1)
        while True:
            cards, np_cards = self.parse_cards(screenshot())
            if cards == {} or Card.UNKNOWN in [c.svt for c in cards.values()]:
                if time.time() - t0 > 5 or self.card_templates == {}:
                    break
        return cards, np_cards

    def auto_attack(self, nps: Union[List[int], int] = None, mode=AttackMode.damage, parse_np=False,
                    allow_unknown=False, no_play_card=False, buster_first=False):
        """

        :param parse_np:
        :param nps:
        :param mode: see `AttackMode`
        :param allow_unknown: if parse cards failed(more than 5s), just chose cards[1,2,3]
        :param no_play_card: if True, return chosen_cards but no to play cards automatically.
        :param buster_first:
        :return: chosen_cards
        """
        logger.info(f'Auto attack: nps={nps}, mode={mode}', extra=LOG_TIME)
        t0 = time.time()
        while not match_targets(screenshot(), self.T.cards1, self.LOC.cards_back):
            click(self.LOC.attack, lapse=1)  # self.LOC.attack should be not covered by self.LOC.cards_back
        while True:
            cards, np_cards = self.parse_cards(screenshot(), nps=nps if parse_np else None)
            # print('in auto_attack: ', cards, np_cards)
            chosen_cards = []
            if cards == {} or Card.UNKNOWN in [c.svt for c in cards.values()]:
                # if lapse>5s[can be modified], some card is not recognized, maybe someone has been died
                if time.time() - t0 > 5 and allow_unknown or self.card_templates == {}:
                    chosen_cards = self.choose_cards(cards, np_cards, nps, mode=mode, buster_first=buster_first)
                    logger.info(f'unrecognized: {[f"{self.str_cards(c)}" for c in cards.values()]},'
                                f' nps={self.str_cards(np_cards)}', extra=LOG_TIME)
                    break
                else:
                    continue
            else:
                chosen_cards = self.choose_cards(cards, np_cards, nps, mode=mode, buster_first=buster_first)
                break
        if nps is not None:
            sleep(0.8, 0.5)
        if no_play_card is False:
            self.play_cards(chosen_cards)
        return chosen_cards

    def xjbd(self, target, regions, mode=AttackMode.damage, turns=100, allow_unknown=False, nps=None):
        # type:(Union[Image.Image,Sequence[Image.Image]],Sequence,AttackMode,int,bool,Union[int,Sequence])->List[List]
        cur_turn = 0
        turn_cards = []
        while cur_turn < turns:
            shot = screenshot()
            if match_targets(shot, target, regions):
                # this part must before elif part
                if cur_turn > 0:
                    logger.info(f'xjbd total {cur_turn} turns', extra=LOG_TIME)
                return turn_cards
            elif match_targets(shot, self.T.wave1a, self.LOC.master_skill):
                cur_turn += 1
                logger.info(f'xjbd: turn {cur_turn}/{turns}.', extra=LOG_TIME)
                sleep(1, 0.5)
                chosen_cards = self.auto_attack(mode=mode, nps=nps, allow_unknown=allow_unknown)
                # self.attack([1, 2, 3])
                turn_cards.append(chosen_cards)
            else:
                continue

    # usually assist for methods above
    def attack(self, locs_or_cards: Union[List[Card], List[int]]):
        assert len(locs_or_cards) >= 3, locs_or_cards
        logger.info(f'Attack: cards={locs_or_cards}', extra=LOG_TIME)
        while True:
            click(self.LOC.attack, lapse=1)
            if match_targets(screenshot(), self.T.cards1, self.LOC.cards_back):
                sleep(1, 0.5)
                self.play_cards(locs_or_cards)
                break

    def parse_cards(self, img: Image.Image, nps: List[int] = None) -> Tuple[Dict[int, Card], Dict[int, Card]]:
        """
        Recognize the cards of current screenshot.

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
                if mode == 1 and card.color == Card.NP:
                    continue
                elif mode == 2 and card.color != Card.NP:
                    continue
                for template in templates:
                    # if base_line > 0:
                    #     # enhancement: from 0.95s->0.7s....
                    #     box = (0, max([0, base_line - 10]),
                    #            outer.size[0], min([base_line + template.size[1] + 10, outer.size[1]]))
                    #     cropped_outer = outer.crop(box)
                    # else:
                    #     cropped_outer = outer
                    th, pos = search_target(outer, template)
                    values.append(th)
                    if th > threshold and th > max_th:
                        if base_line < 0:
                            base_line = pos[1]
                        max_th = th
                        _matched = Card(card.svt, card.color)
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
        if cards or np_cards:
            logger.debug(f'Parsed: {[f"{self.str_cards(c)}" for c in cards.values()]},'
                         f' nps={self.str_cards(np_cards)}', extra=LOG_TIME)
        return cards, np_cards

    def choose_cards(self, cards, np_cards, nps=None, mode=AttackMode.damage, buster_first=False):
        # type:(Dict[int,Card],Dict[int,Card],Union[List[int],int],AttackMode,bool)->List[Card]
        """
        :param cards:loc 1~5 {loc+1:svt*10+color}
        :param np_cards:
        :param nps: chosen nps to attack (6~8).
        :param mode:
        :param buster_first:
        :return: locations of chosen cards
        """
        if len(cards) < 5:
            logger.warning(f'in choose_cards: cards count less then 5! {cards}')
        nps = convert_to_list(nps)
        chosen_nps = [np_cards.get(_np, Card(f'{Card.UNKNOWN}{_np}', 0, _np)) for _np in nps]
        if mode == AttackMode.xjbd:
            s_cards = sorted(cards.values(), key=lambda _c: _c.loc)
            chosen_cards = s_cards[0:3]
        else:
            s_cards = sorted(cards.values(), key=lambda _c: self.card_weights.get(_c, 0))
            if mode == AttackMode.damage:
                np_num = len(chosen_nps)
                if np_num > 0:
                    chosen_cards = s_cards[-(3 - np_num):] + list(reversed(s_cards[0:np_num + 2]))
                else:
                    for i in (-3, -2, -1, 1, 0):
                        if s_cards[i].color == Card.BUSTER:
                            s_cards[i], s_cards[-3] = s_cards[-3], s_cards[i]
                            break
                    chosen_cards = s_cards[-3:]
            elif mode == AttackMode.alter:
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
        if buster_first:
            for i, c in enumerate(chosen_cards):
                if i < 3 and isinstance(c, Card) and c.color == Card.BUSTER:
                    chosen_cards.insert(0, chosen_cards.pop(i))
                    break
        logger.debug(f'Chosen: {self.str_cards(chosen_cards)}', extra=LOG_TIME)
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

        logger.info(f'Played: {cards_str_list}', extra=LOG_TIME)
        locs: List[int] = [c.loc if isinstance(c, Card) else c for c in cards]
        for loc in locs:
            # print(f'click card {loc}')
            click(self.LOC.cards[loc - 1], lapse=0.3)
        time.sleep(1)
        if match_targets(screenshot(), self.T.cards1, self.LOC.cards_back):
            # if np card is not clicked, try again
            for loc in locs:
                if loc in (6, 7, 8):
                    click(self.LOC.cards[loc - 1], lapse=0.3)

    def check_rewards(self, img: Image.Image = None, check_type: int = 0):
        if img is None:
            img = screenshot()
        if check_type == 0:
            return False
        elif check_type == 1:
            return match_targets(img, self.T.rewards, self.LOC.rewards_item1)
        elif check_type == 2:
            return match_targets(img, self.T.rewards, self.LOC.rewards_rainbow)
        elif check_type == 3:
            # rewards should not contains craft
            return not match_targets(img, self.T.rewards, self.LOC.rewards_suochi_character, 0.7)
