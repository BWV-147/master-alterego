"""Master class

additional, Card class included.
"""
from util.image_process import *


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
    def eat_apple(self, apple=-1):
        if apple == -1:
            config.finished = True
            logger.debug("don't eat apple, all battles finished. Existing...")
            exit()
        if apple not in (0, 1, 2, 3):
            logger.debug('invalid apple')
            return
        if apple == 0:  # 不舍得吃彩苹果
            apple = 3
        # wait_which_target(self.T.apple_page, self.LOC.apple_page)
        while True:
            shot = screenshot()
            page_no = match_which_target(shot, [self.T.apple_page, self.T.apple_confirm, self.T.support],
                                         [self.LOC.apples[apple], self.LOC.apple_confirm, self.LOC.support_refresh])
            if page_no == 0:
                logger.debug(f"eating {['Colorful', 'Gold', 'Silver', 'Cropper'][apple]} apple...")
                click(self.LOC.apples[apple])
            elif page_no == 1:
                click(self.LOC.apple_confirm, lapse=1)
            elif page_no == 2:
                break

    def choose_support(self, match_svt=True, match_ce=False, match_ce_max=False, match_skills=None, img=None):
        # type:(bool,bool,bool,List[int],Image.Image)->None
        """
        choose support servant. default match the region of 3 svt_skills, additional craft-essences
        :param match_svt:
        :param match_ce: whether match CE, please set to False if jp server since CE could be filtered in jp server
        :param match_ce_max: whether match CE max star
        :param match_skills: skills to match, a list of int value (1,2,3)
        :param img: support page img
        """
        logger.debug('choosing support...')
        support_page = self.T.support if img is None else img
        wait_which_target(support_page, self.LOC.support_refresh)
        refresh_time = 10
        while True:
            found = False
            time.sleep(2)
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
            # refresh support
            if found:
                break
            logger.debug('refresh support')
            refresh_time -= 1
            if refresh_time == 0:
                send_mail(body='refresh support more than 10 times.', subject='refresh support more than 10 times')
            wait_which_target(support_page, self.LOC.support_refresh, at=True)
            wait_which_target(self.T.support_confirm, self.LOC.support_confirm_title, clicking=self.LOC.support_refresh)
            click(self.LOC.support_refresh_confirm)
        while True:
            # =1: in server cn and first loop to click START
            page_no = wait_which_target([self.T.team, self.T.wave1a], [self.LOC.team_cloth, self.LOC.master_skill])
            if page_no == 0:
                # print('click start please')
                # time.sleep(5)
                click(self.LOC.team)
            elif page_no == 1:
                break
            else:
                time.sleep(0.2)

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

    def master_skill(self, before, skill, friend=None, enemy=None, order_change=None, order_change_img=None):
        # type:(Image.Image,int,int,int,Tuple[int,int],Image.Image)->Master
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

    def auto_attack(self, nps: Union[List[int], int] = None, mode='dmg', parse_np=False, allow_unknown=False):
        """
        :param parse_np:
        :param nps:
        :param mode: dmg/xjbd/alter
        :param allow_unknown:
        :return:
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
            if cards == {}:
                if time.time() - t0 > 5 and allow_unknown:
                    # if lapse>3s, maybe someone has been died
                    chosen_cards = convert_to_list(nps)
                    chosen_cards.extend([1, 2, 3])
                    logger.debug('unrecognized cards, choose [1,2,3]')
                    self.play_cards(chosen_cards[0:3])
                    break
                else:
                    continue
            else:
                chosen_cards = self.choose_cards(cards, np_cards, nps, mode=mode)
                self.play_cards(chosen_cards)
                break

    def attack(self, locs_or_cards: Union[List[Card], List[int]]):
        assert len(locs_or_cards) >= 3, locs_or_cards
        while True:
            click(self.LOC.attack, lapse=0.2)
            if compare_regions(screenshot(), self.T.cards1, self.LOC.cards_back):
                time.sleep(1)
                self.play_cards(locs_or_cards)
                break

    def play_cards(self, locs_or_cards: Union[List[Card], List[int]]):
        """
        :param locs_or_cards: list of locs or cards
        :return:
        """
        # assert len(locs_or_cards) >= 3, locs_or_cards
        if len(locs_or_cards) < 3:
            print(f'warning! Less then 3 cards to play: {self.str_cards(locs_or_cards)}')
            # time.sleep(1)
        logger.debug(f'Attack cards: {self.str_cards(locs_or_cards)}')
        locs: List[int] = [c.loc if isinstance(c, Card) else c for c in locs_or_cards]
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
        assert self.templates != {}, 'Please set cards templates first!!!'
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

    def str_cards(self, cards: Union[List[Card], Dict[int, Card], List[int]]):
        if isinstance(cards, dict):
            cards: List[Card] = list(cards.values())
            cards.sort(key=lambda c: c.loc)
        elif isinstance(cards[0], int):
            return str(cards)
        s = []
        # print('ready to print cards:', cards)
        for card in cards:
            s.append(self.svt_names[card.svt - 1] + '-' + '宝QAB'[card.color])
        return str(s)

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
        if isinstance(weights[0], int):
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
