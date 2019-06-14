from image_process import *


# noinspection PyMethodMayBeStatic
class Master:
    """
    1. crop screen to match card's svt&color
    2. weights to decide the suit to play
    3.
    card: (svt_no, color)
    """

    def __init__(self):
        self.templates = {}
        self.weight: list = []
        self.svt_names = ['1', '2', '3']

    def eat_apple(self, apple=3, check_time=False):
        logger.debug(f"eating {[''][apple]} apple...")
        if apple not in (0, 1, 2, 3):
            return
        if apple == 0:  # 不舍得吃彩苹果
            apple = 3
        wait_regions(T.apple_page, LOC.apple_page)
        if apple == 1 and check_time:
            click(LOC.apple_close)
            click(LOC.safe_area)  # why?
            ap_time = T.quest.crop(LOC.ap_time)
            while True:
                sim = cal_sim(screenshot().crop(LOC.ap_time), ap_time)
                if sim > THR:
                    click(LOC.quest_c, lapse=0.1)
                    click(LOC.safe_area, lapse=0.1)  # why: sometimes click once to select, twice to enter
                    click(LOC.quest_c, lapse=0.1)
                    break
                time.sleep(2)
        # eating apple page
        shot = screenshot()
        if compare_region(shot, T.apple_page, LOC.apples[apple]):
            click(LOC.apples[apple])
            wait_regions(T.apple_confirm, LOC.apple_confirm, at=True)
            wait_regions(T.support, LOC.support_team_icon)
            return
        elif compare_region(shot, T.support, LOC.support_refresh):
            return
        else:
            logger.debug('apple?? where??')

    def choose_support(self, match_ce=False, match_ce_max=False, match_skills=None):
        # type:(bool,bool,List[int])->None
        """
        choose support servant. default match the region of 3 svt_skills, additional craft-essences
        :param match_ce: whether match CE, please set to False if jp server since CE could be filtered in jp server
        :param match_ce_max: whether match CE max star
        :param match_skills: skills to match, a list of int value (1,2,3)
        """
        logger.debug('choosing support...')
        # time.sleep(2)  # it should match support list somewhere(助战编队确认) since support list loads after other UI
        wait_regions(T.support, LOC.support_team_icon)
        while True:
            shot = screenshot()
            for svt in range(2):  # 2 support one time, no scroll
                if compare_region(shot, T.support, LOC.support_skill[svt]):
                    if match_skills is not None:
                        rs = [compare_region(shot, T.support, LOC.support_skills[svt][skill_loc - 1]) for skill_loc in
                              match_skills]
                        if rs.count(True) != len(match_skills):
                            continue
                    if match_ce:
                        if not compare_region(shot, T.support, LOC.support_ce[svt]):
                            continue
                    if match_ce_max:
                        if not compare_region(shot, T.support, LOC.support_ce_max[svt]):
                            continue
                    click(LOC.support_ce[svt])
                    return
            # refresh support
            wait_regions(T.support, LOC.support_refresh)
            time.sleep(1)
            click(LOC.support_refresh)
            wait_regions(T.support_confirm, LOC.support_confirm_title)
            click(LOC.support_refresh_confirm)
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
        logger.info()
        valid, valid2 = (1, 2, 3), (1, 2, 3, None)
        assert who in valid and skill in valid and friend in valid2 and enemy in valid2, (who, skill, friend, enemy)
        assert (friend, enemy).count(None) <= 1, (friend, enemy)
        s = f'to friend {self.svt_names[friend - 1]}' if friend \
            else f'to enemy {self.svt_names[enemy - 1]}' if enemy else ''
        logger.debug('Servant skill %s-%d%s.' % (who, skill, s))
        # start
        if enemy is not None:
            click(LOC.enemies[enemy - 1])
        region = LOC.skills[who - 1][skill - 1]
        wait_regions(before, region, at=True)
        if friend is not None:
            # it should also match the saved screenshot, but...
            time.sleep(0.3)
            click(LOC.skill_to_target[friend - 1])
        wait_regions(after, region)

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
        assert (friend, enemy, order_change).count(None) <= 1, (friend, enemy, order_change)
        s = f'to friend {friend}' if friend else f'to enemy {enemy}' if enemy else ''
        logger.debug(f'Master skill {skill}{s}.')

        region = LOC.master_skills[skill - 1]
        if enemy is not None:
            click(LOC.enemies[enemy - 1])
        no = 3  # max times to click master skill icon, sometime click is invalid
        while no > 0:
            no -= 1
            time.sleep(0.3)
            click(LOC.master_skill)
        wait_regions(before, region, at=True)
        if friend is not None:
            # it should also match the saved screenshot, but...
            time.sleep(0.3)
            click(LOC.skill_to_target[friend - 1])
        elif order_change is not None:
            wait_regions(order_change_img, LOC.order_change[0])
            click(LOC.order_change[order_change[0] - 1])
            click(LOC.order_change[order_change[1] - 1])
            click(LOC.order_change_confirm)
            wait_regions(before, LOC.master_skill)
            pass
        wait_regions(before, LOC.master_skill)

    def attack(self, cards):
        for card in cards:
            click(LOC.cards[card - 1])
            time.sleep(0.2)

    def choose_cards(self, cards: List[int], nps: List[int] = None):
        if isinstance(nps, int):
            nps = [nps + 4]
        elif nps is None:
            nps = []
        else:
            nps = [np + 4 for np in nps]
        cards2 = sorted(cards, key=lambda o: self.weight[o[0] * 10 + o[1]])
        nps.extend(cards2)
        return nps[0:3]

    def load_card_templates(self, locs: list):
        """
        parse card templates from cards_templ[1~3].png file. regions using inner boundary `LOC.cards[0~7]`
        :param locs: locations(tmpl:1~3, card:1~5 6~8) of  [svt1:[np, quick, arts, buster], svt2:..., ...]
        """
        tmpls: List[Image.Image] = T.cards_tmpls
        for svt, svt_loc in enumerate(locs):
            for color, loc in enumerate(svt_loc):
                self.templates[(svt + 1) * 10 + color] = tmpls[loc[0] - 1].crop(LOC.cards[loc[1] - 1])

    def parse_cards(self, np_svts: Tuple[int] = ()):
        """
        recognize the cards of current screenshot
        :param np_svts: which servants' np must be found. nps=(1~6,)
        :return: cards[5], np_cards[len(np_svts)]
        """

        def traverse(outer, mode=0):
            # mode=0-all,1-common card,2-np card
            for key, templ in self.templates.items():
                _svt, _color = key // 10, key % 10
                if mode == 1 and _color == 0:
                    continue
                elif mode == 2 and _color != 0:
                    continue
                if match_target(outer, templ):
                    return _svt, _color
            return -1, -1

        while True:
            shot = screenshot()
            cards = []
            flag = True
            for loc in range(5):  # 5 common card
                svt, color = traverse(shot.crop(LOC.cards_outer[loc]), 1)
                if color <= 0:
                    flag = False
                    break
                else:
                    cards.append((svt, color))
            np_cards = []
            for loc in range(5, 8):
                svt, color = traverse(shot.crop(LOC.cards_outer[loc]), 2)
                if color != 0:
                    flag = False
                    break
                else:
                    np_cards.append((svt, color))
            if flag and set(np_svts).issubset(set(np_cards)):  # np_svts must be found
                return cards, np_cards
            else:
                continue

    def set_card_weight(self, weights: list, color_weight: str = 'QAB'):
        """
        :param weights: M*3, M-servants, 3-quick/art/buster; or M*1, then apply buster>arts>quick
        :return:
        """
        if isinstance(weights[0], int):
            weights = [[w + 1, w + 2, w + 3] for i, w in enumerate(weights)]
        self.weight = weights


def _test():
    pass


if __name__ == '__main__':
    pass
