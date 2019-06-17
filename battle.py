"""Place battle_func for different battles"""
from master import *
from goto import with_goto
from concurrent.futures import ThreadPoolExecutor


# noinspection PyUnusedLocal
@with_goto
def __battle_func_example(master: Master, apple=-1):
    pass


# main entrance
def battle_with_check(battle_func, templ_dir, num=10, apple=-1, check=True):
    # type:(Callable[[Master,int],None],str,int,int,bool)->None
    master = Master()
    check_admin()
    if check:
        executor = ThreadPoolExecutor()
        executor.submit(master.start_battle, battle_func, templ_dir, num, apple)
        executor.submit(check_log_time, 120)
        executor.shutdown(wait=True)
        print('executor shutdown.')
    else:
        master.start_battle(battle_func, templ_dir, num, apple)


# %% serials of battle_func
@with_goto
def battle_charlotte_android(master: Master, apple=-1):
    # LOC.relocate((106, 60, 1813, 1020))
    master.svt_names = ['尼托', '旧剑', '孔明']
    master.set_card_weights([2, 3, 1])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, 6), (3, 4), (2, 3), (1, 1)],
                               [(3, 7), (2, 1), (1, 2), (1, 3)],
                               [(2, -1), (3, 5), (2, 5), (1, 4)]])
    if G.setdefault('goto', False):
        # noinspection PyStatementEffect
        goto.h

    wait_regions(T.quest, LOC.quest, at=True)
    page_no = wait_regions([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
    if page_no == 1:
        master.eat_apple(apple, True)
    master.choose_support(match_ce=True, match_ce_max=True)
    logger.info('Quest Charlotte-android start...')
    # wave 1
    wait_regions(T.wave1a, LOC.enemies[2])
    wait_regions(T.wave1a, LOC.master_skill)
    master.svt_skill(T.wave1a, T.wave1b, 3, 2)
    master.svt_skill(T.wave1a, T.wave1b, 3, 3)
    master.svt_skill(T.wave1a, T.wave1b, 3, 1, 1)
    # noinspection PyStatementEffect
    label.h
    master.auto_attack(6)
    # master.xjbd(T.wave2a, LOC.enemies[2])

    # wave 2
    wait_regions(T.wave2a, LOC.master_skill)
    master.svt_skill(T.wave2a, T.wave2b, 1, 1)
    master.svt_skill(T.wave2a, T.wave2b, 1, 2)
    master.master_skill(T.wave2a, 2, 1)
    master.auto_attack(nps=6)
    # master.xjbd(T.wave3a, LOC.enemies[2])

    # wave 3
    wait_regions(T.wave3a, LOC.master_skill)
    master.svt_skill(T.wave3a, T.wave3b, 2, 1)
    master.svt_skill(T.wave3a, T.wave3b, 2, 2)
    master.svt_skill(T.wave3a, T.wave3b, 2, 3)
    # click(LOC.enemies[1])
    master.auto_attack(7)
    master.xjbd(T.kizuna, LOC.kizuna)

    return


@with_goto
def battle_charlotte_ios(master: Master, apple=-1):
    # LOC.relocate((133, 75, 1785, 1004))
    LOC.relocate((142, 60, 1777, 980))  # maximize with task bar
    master.svt_names = ['豆爸', 'lily', '孔明']
    master.set_card_weights([1, 3, 2])
    # ---------------------------  NP    Quick    Arts    Buster ----
    master.set_card_templates([[(1, 6), (3, 5), (1, 5), (2, 1)],
                               [(2, 7), (2, 4), (1, 2), (1, 1)],
                               [(2, -1), (1, 4), (1, 3), (3, 2)]])
    if G.setdefault('goto', False):
        # noinspection PyStatementEffect
        goto.h

    wait_regions(T.quest, LOC.quest, at=True)
    page_no = wait_regions([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
    if page_no == 1:
        master.eat_apple(apple, True)
    master.choose_support(match_ce=True, match_ce_max=True)
    logger.info('Quest Charlotte-iOS start...')
    # wave 1
    wait_regions(T.wave1a, LOC.enemies[2])
    wait_regions(T.wave1a, LOC.master_skill)
    master.svt_skill(T.wave1a, T.wave1b, 3, 2)
    master.svt_skill(T.wave1a, T.wave1b, 3, 3)
    master.svt_skill(T.wave1a, T.wave1b, 3, 1, 1)
    master.svt_skill(T.wave1a, T.wave1b, 1, 2)
    master.auto_attack(6)
    # master.xjbd(T.wave2a, LOC.enemies[2])

    # noinspection PyStatementEffect
    label.h
    # wave 2
    wait_regions(T.wave2a, LOC.master_skill)
    master.svt_skill(T.wave2a, T.wave2b, 1, 1)
    # master.svt_skill(T.wave2a, T.wave2b, 1, 2)
    master.master_skill(T.wave2a, 2, 1)
    master.auto_attack(6)
    # master.xjbd(T.wave3a, LOC.enemies[2])

    # wave 3
    wait_regions(T.wave3a, LOC.master_skill)
    master.svt_skill(T.wave3a, T.wave3b, 2, 1)
    master.svt_skill(T.wave3a, T.wave3b, 2, 2)
    # master.svt_skill(T.wave3a, T.wave3b, 2, 3)
    # click(LOC.enemies[1])
    master.auto_attack(7)
    master.xjbd(T.kizuna, LOC.kizuna)


@with_goto
def loop_test(master: Master, apple=-1):
    # LOC.relocate((133, 75, 1785, 1004))
    LOC.relocate((106, 60, 1813, 1020))
    master.svt_names = ['特斯拉', '黑狗', '梅林']
    master.set_card_weights([2, 3, 1])
    master.set_card_templates([[(2, 6), (3, 5), (2, 3), (1, 1)],
                               [(2, 7), (2, 5), (1, 3), (1, 4)],
                               [(2, 8), (2, 1), (2, 2), (3, 1)]])
    if G.get('first_run', True):
        # noinspection PyStatementEffect
        goto.h
        G['first_run'] = False
        pass

    wait_regions(T.quest, LOC.quest)
    while True:
        page_no = compare_regions(screenshot(), [T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no < 0:
            click(LOC.quest, lapse=0.5)
        else:
            break
    if page_no == 1:
        master.eat_apple(apple, True)
    master.choose_support(match_ce=True, match_ce_max=True)
    logger.info('Quest Test start...')
    # wave 1
    wait_regions(T.wave1a, LOC.wave)
    wait_regions(T.wave1a, LOC.master_skill)
    master.svt_skill(T.wave1a, T.wave1b, 2, 2)
    master.xjbd(T.wave2a, LOC.enemies[0])

    # wave 2
    wait_regions(T.wave2a, LOC.master_skill)
    master.svt_skill(T.wave2a, T.wave2b, 1, 2)
    master.svt_skill(T.wave2a, T.wave2b, 3, 1)
    # noinspection PyStatementEffect
    label.h
    master.auto_attack(nps=6)
    master.xjbd(T.wave3a, LOC.wave)

    # wave 3
    wait_regions(T.wave3a, LOC.master_skill)
    master.svt_skill(T.wave3a, T.wave3b, 3, 3, 2)
    master.master_skill(T.wave3a, T.wave3a, 2)
    master.auto_attack(7)
    master.xjbd(T.kizuna, LOC.kizuna)
    wait_regions(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp)
    ce = screenshot()
    # check apply_support/friendship_point(after 4:00am)/quest_page
    while True:
        page_no = wait_regions([T.quest, T.apply_friend, T.friend_point],
                               [LOC.quest, LOC.apply_friend, LOC.friend_point])
        if page_no == 1:
            click(LOC.apply_friend_deny)
        elif page_no == 2:
            click(LOC.friend_point_close)
        elif page_no == 0:
            break
    # return rewards page screenshot
    return ce
