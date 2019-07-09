"""Place battle_func for different battles"""
from util.master import *
from goto import with_goto
from concurrent.futures import ThreadPoolExecutor
import signal


# noinspection PyPep8Naming
class Battle:
    def __init__(self):
        self.master = Master()
        pass

    def start(self, battle_func, num=10, apple=-1):
        T = self.master.T
        LOC = self.master.LOC
        timer = Timer()
        finished = 0
        while finished < num:
            timer.start()
            finished += 1
            logger.info(f'>>>>> Battle "{self.master.quest_name}" No.{finished}/{num} <<<<<')
            battle_func(apple)
            wait_which_target(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
            # check reward_page has CE dropped or not
            ce = screenshot()
            ce.save(f"img/craft/craft-{time.strftime('%m%d-%H-%M-%S')}.png")
            click(LOC.finish_next)
            logger.info('battle finished, checking rewards.')
            wait_which_target(T.quest, LOC.quest)
            # while True:
            #     page_no = wait_which_target([T.quest, T.apply_friend, T.friend_point],
            #                                 [LOC.quest, LOC.apply_friend, LOC.friend_point])
            #     if page_no == 1:
            #         click(LOC.apply_friend_deny)
            #     elif page_no == 2:
            #         click(LOC.friend_point)
            #     elif page_no == 0:
            #         break
            dt = timer.stop().dt
            logger.info(f'--- Battle {finished} finished, time = {int(dt // 60)} min {int(dt % 60)} sec.')
            with open('log/time.log', 'a') as fd:
                fd.write(str(dt) + '\n')
        logger.info(f'>>>>> All {finished} battles "{self.master.quest_name}" finished. <<<<<')

    @with_goto
    def chaos_android(self, apple):
        """
        阵容: 大英雄70(虚数1)-弓凛(空骑80)-孔明-旧狗(虚数20)-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'chaos-android'
        master.svt_names = ['大英雄', '弓凛', '孔明', '旧狗']
        # T.read_templates('img/chaos-android')
        T.read_templates('img/test')
        # LOC.relocate((88, 45, 1830, 1024))
        # LOC.relocate((106, 60, 1813, 1020))
        master.set_card_weights([1, 3, 2, 3])
        # ---------------------------  NP    Quick    Arts    Buster ----
        master.set_card_templates([[(1, 0), (0, 0), (0, 0), (0, 0)],
                                   [(2, 7), (3, 1), (3, 2), (1, 2)],
                                   [(2, 0), (2, 3), (2, 5), (2, 4)],
                                   [(1, 6), (1, 1), (1, 5), (3, 3)]])
        if G.setdefault('goto', False):
            G['goto'] = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.quest, LOC.quest, at=True)
        page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no == 1:
            master.eat_apple(apple, True)
        master.choose_support(match_ce=True, match_ce_max=False)
        logger.debug('Quest Chaos-android start...')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[2])
        wait_which_target(T.wave1a, LOC.master_skill)
        master.svt_skill(T.wave1a, T.wave1b, 1, 3)
        master.svt_skill(T.wave1a, T.wave1b, 2, 3)
        master.svt_skill(T.wave1a, T.wave1b, 3, 2)

        # noinspection PyStatementEffect
        label.h
        master.attack([6, 1, 2])

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill, lapse=1, clicking=LOC.safe_area)
        master.svt_skill(T.wave2a, T.wave2b, 2, 1)
        master.svt_skill(T.wave2a, T.wave2b, 2, 2)
        master.svt_skill(T.wave2a, T.wave2b, 3, 3)
        master.attack([7, 1, 2])

        # wave 3
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        master.svt_skill(T.wave3a, T.wave3b, 1, 3)
        master.svt_skill(T.wave3a, T.wave3b, 3, 1, 1)
        master.master_skill(T.wave3a, 2, 1)

        master.attack([6, 1, 2])
        master.xjbd(T.kizuna, LOC.kizuna, mode='xjbd')
        return

    @with_goto
    def chaos_ios(self, apple):
        """
        阵容：大英雄(宝石20)-阿周那(宝石20)-孔明()-|-旧狗(醉贞82)-(X)-(X)
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'chaos-ios'
        master.svt_names = ['大英雄', '阿周那', '孔明', '旧狗']
        T.read_templates('img/chaos-ios')
        # LOC.relocate((5, 44, 1830, 1024))
        master.set_card_weights([1, 3, 2, 3])
        # ---------------------------  NP    Quick    Arts    Buster ----
        master.set_card_templates([[(1, 0), (3, 0), (2, 0), (1, 0)],
                                   [(2, 7), (3, 1), (3, 2), (1, 2)],
                                   [(2, 0), (2, 3), (2, 5), (2, 4)],
                                   [(1, 6), (1, 1), (1, 5), (3, 3)]])
        if G.setdefault('goto', False):
            G['goto'] = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.quest, LOC.quest, at=True)
        page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no == 1:
            master.eat_apple(apple, True)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=False)
        logger.debug('Quest Chaos-iOS start...')

        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[2])
        wait_which_target(T.wave1a, LOC.master_skill)
        master.svt_skill(T.wave1a, T.wave1b, 1, 3)
        master.attack([6, 1, 2])

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill, lapse=1, clicking=LOC.safe_area)
        master.svt_skill(T.wave2a, T.wave2b, 3, 2)
        master.svt_skill(T.wave2a, T.wave2b, 3, 3)
        master.svt_skill(T.wave2a, T.wave2b, 1, 3)
        master.attack([6, 1, 2])

        # wave 3
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        master.svt_skill(T.wave3a, T.wave3b, 2, 3)
        master.svt_skill(T.wave3a, T.wave3b, 3, 1, 2)
        master.master_skill(T.wave3a, 2, 2)
        # noinspection PyStatementEffect
        label.h
        master.attack([7, 1, 2])
        master.xjbd(T.kizuna, LOC.kizuna, mode='xjbd')
        return


# noinspection PyUnusedLocal
@with_goto
def __battle_func_example(master: Master, apple=-1):
    pass


# %% bone!
@with_goto
def battle_bone_android(master: Master, apple=-1):
    if not master.quest_name:
        master.quest_name = 'bone-android'
    master.svt_names = ['大英雄', '弓凛', '梅林', '尼托']
    master.T.read_templates('img/saber')
    # master.LOC.relocate((106, 60, 1813, 1020))
    master.set_card_weights([1, 3, 2, 2])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, -1), (3, -1), (2, -1), (1, -1)],
                               [(2, 7), (3, 1), (3, 2), (1, 2)],
                               [(2, -1), (2, 3), (2, 5), (2, 4)],
                               [(1, 6), (1, 1), (1, 5), (3, 3)]])
    T = master.T
    LOC = master.LOC
    if G.setdefault('goto', False):
        G['goto'] = False
        logger.warning('goto label.h')
        # noinspection PyStatementEffect
        goto.h

    wait_which_target(T.quest, LOC.quest, at=True)
    page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
    if page_no == 1:
        master.eat_apple(apple, True)
    master.choose_support(match_ce=False, match_ce_max=False)
    # logger.info('Quest Charlotte-android start...')
    # wave 1
    wait_which_target(T.wave1a, LOC.enemies[2])
    wait_which_target(T.wave1a, LOC.master_skill)
    master.svt_skill(T.wave1a, T.wave1b, 1, 3)
    master.svt_skill(T.wave1a, T.wave1b, 3, 1)
    # master.svt_skill(T.wave1a, T.wave1b, 3, 1, 1)
    # master.auto_attack(6)
    master.attack([6, 1, 2])
    # master.xjbd(T.wave2a, LOC.enemies)

    # wave 2
    wait_which_target(T.wave2a, LOC.master_skill, lapse=1, clicking=LOC.safe_area)
    master.svt_skill(T.wave2a, T.wave2b, 1, 1)
    master.svt_skill(T.wave2a, T.wave2b, 1, 2)
    master.svt_skill(T.wave2a, T.wave2b, 2, 3)
    # master.master_skill(T.wave2a, 2, 1)
    # master.auto_attack(nps=6)
    master.attack([6, 1, 2])
    # master.xjbd(T.wave3a, LOC.enemies)

    # wave 3
    wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
    master.svt_skill(T.wave3a, T.wave3b, 2, 1)
    master.svt_skill(T.wave3a, T.wave3b, 2, 2)
    master.svt_skill(T.wave3a, T.wave3b, 3, 3, 2)
    master.master_skill(T.wave3a, 2, 2)
    # click(LOC.enemies[1])
    # noinspection PyStatementEffect
    label.h
    master.auto_attack(7)
    master.xjbd(T.kizuna, LOC.kizuna, mode='dmg')
    return


@with_goto
def battle_bone_ios(master: Master, apple=-1):
    if not master.quest_name:
        master.quest_name = 'bone-ios'
    master.svt_names = ['大英雄', '闪闪', '梅林', '红A']
    master.T.read_templates('img/bone-ios')
    master.LOC.relocate((142, 60, 1777, 979))
    master.set_card_weights([1, 3, 1, 2])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, 6), (3, -1), (2, -1), (1, -1)],
                               [(3, 7), (2, 1), (1, 2), (1, 3)],
                               [(2, -1), (3, 5), (2, 5), (1, 4)]])
    T = master.T
    LOC = master.LOC
    if G.setdefault('goto', False):
        G['goto'] = False
        logger.warning('goto label.h')
        # noinspection PyStatementEffect
        goto.h

    wait_which_target(T.quest, LOC.quest, at=True)
    page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
    if page_no == 1:
        master.eat_apple(apple, False)
    master.choose_support(match_ce=False, match_ce_max=False)
    # logger.info('Quest Charlotte-android start...')
    # wave 1
    wait_which_target(T.wave1a, LOC.enemies[2])
    wait_which_target(T.wave1a, LOC.master_skill)
    master.svt_skill(T.wave1a, T.wave1b, 1, 3)
    # master.svt_skill(T.wave1a, T.wave1b, 3, 3)
    # master.svt_skill(T.wave1a, T.wave1b, 3, 1, 1)
    # master.auto_attack(6)
    master.attack([6, 1, 2])
    # master.xjbd(T.wave2a, LOC.enemies)

    # wave 2
    wait_which_target(T.wave2a, LOC.master_skill, lapse=1, clicking=LOC.safe_area)
    master.svt_skill(T.wave2a, T.wave2b, 1, 2)
    master.svt_skill(T.wave2a, T.wave2b, 1, 3)
    master.svt_skill(T.wave2a, T.wave2b, 2, 1)
    master.svt_skill(T.wave2a, T.wave2b, 3, 1)
    # master.master_skill(T.wave2a, 2, 1)
    # master.auto_attack(nps=6)
    master.attack([6, 1, 2])
    # master.xjbd(T.wave3a, LOC.enemies)

    # wave 3
    wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
    master.svt_skill(T.wave3a, T.wave3b, 2, 3)
    master.svt_skill(T.wave3a, T.wave3b, 3, 3, 2)
    master.master_skill(T.wave3a, 2, 2)
    # master.svt_skill(T.wave3a, T.wave3b, 2, 3)
    # click(LOC.enemies[1])
    # noinspection PyStatementEffect
    label.h
    master.attack([7, 1, 2])
    master.xjbd(T.kizuna, LOC.kizuna)

    return


# %% serials of battle_func
@with_goto
def battle_charlotte_android(master: Master, apple=-1):
    if not master.quest_name:
        master.quest_name = 'charlotte-android'
    master.svt_names = ['尼托', '旧剑', '孔明']
    master.T.read_templates('img/charlotte')
    # master.LOC.relocate((106, 60, 1813, 1020))
    master.set_card_weights([2, 3, 2])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, 6), (3, 4), (2, 3), (1, 1)],
                               [(3, 7), (2, 1), (1, 2), (1, 3)],
                               [(2, -1), (3, 5), (2, 5), (1, 4)]])
    T = master.T
    LOC = master.LOC
    if G.setdefault('goto', False):
        G['goto'] = False
        logger.warning('goto label.h')
        # noinspection PyStatementEffect
        goto.h

    wait_which_target(T.quest, LOC.quest, at=True)
    page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
    if page_no == 1:
        master.eat_apple(apple, True)
    master.choose_support(match_ce=True, match_ce_max=True)
    # logger.info('Quest Charlotte-android start...')
    # wave 1
    wait_which_target(T.wave1a, LOC.enemies[2])
    wait_which_target(T.wave1a, LOC.master_skill)
    master.svt_skill(T.wave1a, T.wave1b, 3, 2)
    master.svt_skill(T.wave1a, T.wave1b, 3, 3)
    master.svt_skill(T.wave1a, T.wave1b, 3, 1, 1)
    # master.auto_attack(6)
    master.attack([6, 1, 2])
    master.xjbd(T.wave2a, LOC.enemies)

    # wave 2
    wait_which_target(T.wave2a, LOC.master_skill)
    master.svt_skill(T.wave2a, T.wave2b, 1, 1)
    master.svt_skill(T.wave2a, T.wave2b, 1, 2)
    master.master_skill(T.wave2a, 2, 1)
    # master.auto_attack(nps=6)
    master.attack([6, 1, 2])
    master.xjbd(T.wave3a, LOC.enemies)

    # wave 3
    wait_which_target(T.wave3a, LOC.master_skill)
    master.svt_skill(T.wave3a, T.wave3b, 2, 1)
    master.svt_skill(T.wave3a, T.wave3b, 2, 2)
    master.svt_skill(T.wave3a, T.wave3b, 2, 3)
    # click(LOC.enemies[1])
    # noinspection PyStatementEffect
    label.h
    master.auto_attack(7)
    master.xjbd(T.kizuna, LOC.kizuna)

    return


@with_goto
def battle_charlotte_ios(master: Master, apple=-1):
    # LOC.relocate((133, 75, 1785, 1004))
    master.quest_name = 'charlotte-ios'
    master.svt_names = ['豆爸', 'lily', '孔明']
    master.LOC.relocate((142, 60, 1777, 980))  # maximize with task bar
    master.T.read_templates('img/charlotte-ios')
    master.set_card_weights([1, 3, 2])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, 6), (3, 5), (1, 5), (2, 1)],
                               [(2, 7), (2, 4), (1, 2), (1, 1)],
                               [(2, -1), (1, 4), (1, 3), (3, 2)]])
    T = master.T
    LOC = master.LOC
    if G.setdefault('goto', False):
        G['goto'] = False
        logger.warning('goto label.h')
        # noinspection PyStatementEffect
        goto.h

    wait_which_target(T.quest, LOC.quest, at=True)
    page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
    if page_no == 1:
        master.eat_apple(apple, True)
    master.choose_support(match_ce=True, match_ce_max=True)
    # logger.info('Quest Charlotte-iOS start...')
    # wave 1
    wait_which_target(T.wave1a, LOC.enemies[2])
    wait_which_target(T.wave1a, LOC.master_skill)
    master.svt_skill(T.wave1a, T.wave1b, 3, 2)
    master.svt_skill(T.wave1a, T.wave1b, 3, 3)
    master.svt_skill(T.wave1a, T.wave1b, 3, 1, 1)
    master.svt_skill(T.wave1a, T.wave1b, 1, 2)
    master.auto_attack(6)
    master.xjbd(T.wave2a, LOC.enemies)

    # wave 2
    wait_which_target(T.wave2a, LOC.master_skill)
    master.svt_skill(T.wave2a, T.wave2b, 1, 1)
    # master.svt_skill(T.wave2a, T.wave2b, 1, 2)
    master.master_skill(T.wave2a, 2, 1)
    master.auto_attack(6)
    master.xjbd(T.wave3a, LOC.enemies)

    # wave 3
    wait_which_target(T.wave3a, LOC.master_skill)
    master.svt_skill(T.wave3a, T.wave3b, 2, 1)
    master.svt_skill(T.wave3a, T.wave3b, 2, 2)
    # master.svt_skill(T.wave3a, T.wave3b, 2, 3)
    # click(LOC.enemies[1])
    # noinspection PyStatementEffect
    label.h
    master.auto_attack(7)
    master.xjbd(T.kizuna, LOC.kizuna)
