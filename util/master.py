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

    def set_battle_data(self, coord=None, names=None, weights=None, cards_loc=None):
        if coord:
            self.LOC.relocate(coord)
        if names:
            self.svt_names = names
        if weights:
            self.set_card_weights(weights)
        if cards_loc:
            self.set_card_templates(cards_loc)

    def __start_battle(self, battle_func, num=10, apple=-1):
        # type:(Callable[[Master,int],None],int,int)->None
        """
        set_battle_data first.
        :param battle_func: start at quest banner screen, end at kizuna screen
        :param num:
        :param apple:
        :return:
        """
        timer = Timer()
        finished = 0
        while finished < num:
            timer.start()
            finished += 1
            logger.info(f'>>>>> Battle "{self.quest_name}" No.{finished}/{num} <<<<<')
            battle_func(self, apple)
            wait_which_target(self.T.rewards, self.LOC.finish_qp, clicking=self.LOC.finish_qp, lapse=0.5)
            # check reward_page has CE dropped or not
            ce = screenshot()
            ce.save(f"img/craft/craft-{time.strftime('%m%d-%H-%M-%S')}.png")
            click(self.LOC.finish_next)
            logger.info('battle finished, checking rewards.')
            while True:
                page_no = wait_which_target([self.T.quest, self.T.apply_friend, self.T.friend_point],
                                            [self.LOC.quest, self.LOC.apply_friend, self.LOC.friend_point])
                if page_no == 1:
                    click(self.LOC.apply_friend_deny)
                elif page_no == 2:
                    click(self.LOC.friend_point)
                elif page_no == 0:
                    break
            dt = timer.stop().dt
            logger.info(f'--- Battle {finished} finished, time = {int(dt // 60)} min {int(dt % 60)} sec.')
        logger.info(f'>>>>> All {finished} battles "{self.quest_name}" finished. <<<<<')
        time.sleep(100)

    # procedures
    def eat_apple(self, apple=-1, check_time=False):
        if apple not in (0, 1, 2, 3):
            logger.debug('invalid apple')
            return
        if apple == 0:  # 不舍得吃彩苹果
            apple = 3
        logger.debug(f"eating {['Colorful', 'Gold', 'Silver', 'Cropper'][apple]} apple...")
        wait_which_target(self.T.apple_page, self.LOC.apple_page)
        if apple == 1 and check_time:
            click(self.LOC.apple_close)
            click(self.LOC.safe_area)  # why?
            ap_time = self.T.quest.crop(self.LOC.ap_time)
            while True:
                sim = cal_sim(screenshot().crop(self.LOC.ap_time), ap_time)
                if sim > THR:
                    click(self.LOC.quest_c, lapse=0.1)
                    click(self.LOC.safe_area, lapse=0.1)  # why: sometimes click once to select, twice to enter
                    click(self.LOC.quest_c, lapse=0.1)
                    break
                time.sleep(2)
        # eating apple page
        shot = screenshot()
        if match_which_target(shot, self.T.apple_page, self.LOC.apples[apple]) >= 0:
            click(self.LOC.apples[apple])
            wait_which_target(self.T.apple_confirm, self.LOC.apple_confirm, at=True)
            wait_which_target(self.T.support, self.LOC.support_team_icon)
            return
        elif match_which_target(shot, self.T.support, self.LOC.support_refresh) >= 0:
            return
        else:
            logger.debug('apple?? where??')

    def choose_support(self, match_svt=True, match_ce=False, match_ce_max=False, match_skills=None):
        # type:(bool,bool,bool,List[int])->None
        """
        choose support servant. default match the region of 3 svt_skills, additional craft-essences
        :param match_svt:
        :param match_ce: whether match CE, please set to False if jp server since CE could be filtered in jp server
        :param match_ce_max: whether match CE max star
        :param match_skills: skills to match, a list of int value (1,2,3)
        """
        logger.debug('choosing support...')
        wait_which_target(self.T.support, self.LOC.support_team_icon)
        if match_svt is False:
            click(self.LOC.support_ce[0])
            wait_which_target(self.T.team, self.LOC.team, at=True)
            return
        while True:
            shot = screenshot()
            for svt in range(2):  # 2 support one time, no scroll
                if match_which_target(shot, self.T.support, self.LOC.support_skill[svt]) >= 0:
                    if match_skills is not None:
                        rs = [match_which_target(shot, self.T.support, self.LOC.support_skills[svt][skill_loc - 1]) >= 0
                              for skill_loc in match_skills]
                        if rs.count(True) != len(match_skills):
                            continue
                    if match_ce:
                        if match_which_target(shot, self.T.support, self.LOC.support_ce[svt]) < 0:
                            continue
                    if match_ce_max:
                        if match_which_target(shot, self.T.support, self.LOC.support_ce_max[svt]) < 0:
                            continue
                    click(self.LOC.support_ce[svt])
                    wait_which_target(self.T.team, self.LOC.team, at=True)
                    return
            # refresh support
            wait_which_target(self.T.support, self.LOC.support_refresh)
            time.sleep(2)
            click(self.LOC.support_refresh)
            wait_which_target(self.T.support_confirm, self.LOC.support_confirm_title)
            click(self.LOC.support_refresh_confirm)
            logger.debug('refresh support')

    def svt_skill(self, before, after, who, skill, friend=None, enemy=None):
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
        valid, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert who in valid and skill in valid and friend in valid2 and enemy in valid2, (who, skill, friend, enemy)
        s = f'to friend {self.svt_names[friend - 1]}' if friend \
            else f'to enemy {self.svt_names[enemy - 1]}' if enemy else ''
        logger.debug('Servant skill %s-%d %s.' % (who, skill, s))

        # start
        if enemy is not None:
            click(self.LOC.enemies[enemy - 1])
        region = self.LOC.skills[who - 1][skill - 1]
        wait_which_target(before, region, at=True)
        if friend is not None:
            # it should also match the saved screenshot, but...
            # TODO: match select target shot, same as master_skill
            time.sleep(0.3)
            click(self.LOC.skill_to_target[friend - 1])
        wait_which_target(after, region)

    def master_skill(self, before, skill, friend=None, enemy=None, order_change=None, order_change_img=None):
        # type:(Image.Image,int,int,int,Tuple[int,int],Image.Image)->None
        """
        Master skill, especially order_change = (svt1:1~3,svt2:4~6) if not None
        """
        valid, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert skill in valid and friend in valid2 and enemy in valid2, (skill, friend, enemy)
        if order_change is not None:
            assert order_change[0] in (1, 2, 3) and order_change[1] in (4, 5, 6)
            assert skill == 3 and order_change_img is not None, ('order_change', skill, order_change_img)
        assert (friend, enemy, order_change).count(None) <= 2, (friend, enemy, order_change)
        s = f'to friend {friend}' if friend else f'to enemy {enemy}' if enemy else ''
        logger.debug(f'Master skill {skill} {s}.')

        region = self.LOC.master_skills[skill - 1]
        if enemy is not None:
            click(self.LOC.enemies[enemy - 1])
        flag = 0
        while True:
            if flag % 3 == 0:
                click(self.LOC.master_skill)
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

    def auto_attack(self, nps: Union[List[int], int] = None, mode='dmg', allow_unknown=False):
        """

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
        while True:
            click(self.LOC.attack, lapse=0.5)  # self.LOC.attack should be not covered by self.LOC.cards_back
            cards, np_cards = self.parse_cards(screenshot(), nps=nps)
            if cards == {}:
                if time.time() - t0 > 5 and allow_unknown:
                    # if lapse>3s, maybe someone has been died
                    chosen_cards = convert_list(nps)
                    chosen_cards.extend([1, 2, 3])
                    self.play_cards(chosen_cards[0:3])
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
        assert len(locs_or_cards) >= 3, locs_or_cards
        logger.debug(f'Attack cards: {self.str_cards(locs_or_cards)}')
        # if isinstance(locs_or_cards[0], Card):
        locs: List[int] = [c.loc if isinstance(c, Card) else c for c in locs_or_cards]
        # else:
        #     locs: List[int] = locs_or_cards
        for loc in locs:
            click(self.LOC.cards[loc - 1])
            time.sleep(0.2)

    def xjbd(self, target, regions, mode='dmg', turns=100):
        # type:(Union[Image.Image,List[Image.Image]],Union[tuple,list],str,int)->int
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
                self.auto_attack(mode=mode)
                # self.attack([1, 2, 3])
            else:
                continue

    # assistant functions
    def parse_cards(self, img: Image.Image, nps: List[int] = None) -> Tuple[Dict[int, Card], Dict[int, Card]]:
        """
        recognize the cards of current screenshot
        :param img:
        :param nps: which servants' np must be found. nps=(1~6,)
        :return: location-card(svt*10+color) pair dictionary
        """
        # TODO: if xjbd, someone is dead, should allow unrecognized cards(card code could be -1).
        assert self.templates != {}, 'Please set cards templates first!!!'
        nps = convert_list(nps)

        # if nps is None:
        #     nps = []
        # elif isinstance(nps, int):
        #     nps = [nps]

        # else:
        #     np_svts = [np_loc for np_loc in np_svts]

        def traverse(outer, mode):
            # mode=0-all,1-common card,2-np card
            threshold = THR if loc < 5 else 0.8
            _matched = -1
            max_th = 0
            for key, templ in self.templates.items():
                _svt, _color = key // 10, key % 10
                if mode == 1 and _color == 0:
                    continue
                elif mode == 2 and _color != 0:
                    continue
                th = search_target(outer, templ)
                if th > threshold and th > max_th:
                    max_th = th
                    _matched = key
            # print(f'max={max_th:.4f}   \r', end='')
            return _matched

        cards, np_cards = {}, {}
        for loc in range(1, 6):  # 5 common card
            matched = traverse(img.crop(self.LOC.cards_outer[loc - 1]), 1)
            if matched == -1:
                return {}, {}  # 5 command card must be matched
            else:
                cards[loc] = Card(loc, matched)
        for loc in range(6, 9):
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
        nps = convert_list(nps)
        chosen_nps = [np_cards[_np] for _np in nps]
        # if isinstance(nps, int):
        #     chosen_nps: List[cards] = [np_cards[nps]]
        # elif nps is None:
        #     chosen_nps = []
        # else:
        #     chosen_nps = [np_cards[_np] for _np in nps]
        s_cards = sorted(cards.values(), key=lambda o: self.weights.get(o.code, 0))

        if mode == 'dmg':
            if not chosen_nps:
                for i in (-3, -2, -1, 1, 0):
                    if s_cards[i].color == Card.BUSTER:
                        s_cards[i], s_cards[-3] = s_cards[-3], s_cards[i]
                        break
                chosen_cards = s_cards[-3:]
                # return s_cards[-3:]
            else:
                chosen_nps.extend(s_cards[2 + len(chosen_nps):5])
                chosen_cards = chosen_nps
                # return chosen_nps
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
                # return s_cards[0:3]
            else:
                chosen_nps.extend(s_cards)
                chosen_cards = chosen_nps[0:3]
                # return chosen_nps[0:3]
        elif mode == 'np':
            # TODO: gain np mode
            chosen_nps.extend(s_cards)
            chosen_cards = chosen_nps
        else:
            # chosen_cards=[]
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
    def set_card_templates(self, locs: list):
        """
        parse card templates from cards[1~3].png file. regions using inner boundary `self.LOC.cards`
        :param locs: locations(tmpl:1~3, card:1~5 6~8) of  [svt1:[np, Q, A, B], svt2:...], loc=-1 if no card
        """
        templs: List[Image.Image] = self.T.cards
        for svt, svt_loc in enumerate(locs):
            for color, loc in enumerate(svt_loc):
                if 0 < loc[1] <= 8:
                    # if loc[1] < 1 or loc[1] > 8:
                    #     continue
                    self.templates[(svt + 1) * 10 + color] = templs[loc[0] - 1].crop(self.LOC.cards[loc[1] - 1])

    def set_card_weights(self, weights: list, color_weight: str = 'QAB'):
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
