"""Place battle_func for different battles"""
from util.master import *
from goto import with_goto
from concurrent.futures import ThreadPoolExecutor
import signal


# noinspection PyUnusedLocal
@with_goto
def __battle_func_example(master: Master, apple=-1):
    pass


# %% serials of battle_func
@with_goto
def battle_charlotte_android(master: Master, apple=-1):
    # LOC.relocate((106, 60, 1813, 1020))
    if not master.quest_name:
        master.quest_name = 'charlotte-android'
    master.svt_names = ['尼托', '旧剑', '孔明']
    T.read_templates('img/charlotte')
    master.set_card_weights([2, 3, 1])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, 6), (3, 4), (2, 3), (1, 1)],
                               [(3, 7), (2, 1), (1, 2), (1, 3)],
                               [(2, -1), (3, 5), (2, 5), (1, 4)]])
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
    LOC.relocate((142, 60, 1777, 980))  # maximize with task bar
    master.quest_name = 'charlotte-ios'
    master.svt_names = ['豆爸', 'lily', '孔明']
    T.read_templates('img/charlotte-ios')
    master.set_card_weights([1, 3, 2])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, 6), (3, 5), (1, 5), (2, 1)],
                               [(2, 7), (2, 4), (1, 2), (1, 1)],
                               [(2, -1), (1, 4), (1, 3), (3, 2)]])
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
