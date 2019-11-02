"""Store battle_func for different battles"""

import winsound

# noinspection PyPackageRequirements
from goto import with_goto

from util.master import *


# noinspection PyPep8Naming,DuplicatedCode
class Battle:
    def __init__(self):
        self.master = Master()
        pass

    @with_goto
    def start(self, battle_func, folder, num=10, apple=-1, auto_choose_support=True):
        T = self.master.T
        LOC = self.master.LOC
        timer = Timer()
        T.read_templates(folder)
        config.img_net = T.net_error
        config.loc_net = LOC.net_error
        finished = 0
        info = StatInfo()
        while finished < num:
            finished += 1
            logger.info(f'>>>>> Battle "{self.master.quest_name}" No.{finished}/{num} <<<<<')
            if config.jump_start:
                config.jump_start = False
                logger.warning('outer: goto label.g')
                # noinspection PyStatementEffect
                goto.g
            while True:
                page_no = wait_which_target([T.quest, T.apple_page, T.support],
                                            [LOC.quest, LOC.apple_page, LOC.support_refresh])
                if page_no == 0:
                    click(LOC.quest_c)
                elif page_no == 1:
                    self.master.eat_apple(apple)
                elif page_no == 2:
                    break
            battle_func(auto_choose_support)
            wait_which_target(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            rewards = screenshot()
            logger.info('battle finished, checking rewards.')
            craft_dropped = is_match_target(rewards, T.rewards, LOC.finish_craft)

            if craft_dropped and config.check_drop:
                info.add_battle(True)
                logger.warning(f'{info.craft_num}th craft dropped!!!')
                rewards.save(f'img/_drops/drops-{self.master.quest_name}-{time.strftime("%m%d-%H-%M-%S")}'
                             + f'-drop{info.craft_num}.png')
                if info.craft_num in config.enhance_craft_nums:
                    send_mail(f'NEED Enhancement! {info.craft_num}th craft dropped!!!')
                    logger.warning('need to change party or enhance crafts. Exit.')
                    exit()
                else:
                    send_mail(f'{info.craft_num}th craft dropped!!!')
            else:
                info.add_battle(False)
                rewards.save(f"img/_drops/drops-{self.master.quest_name}-{time.strftime('%m%d-%H-%M-%S')}.png")
            dt = timer.lapse()
            logger.info(f'--- Battle {finished}/{num} finished, time = {int(dt // 60)} min {int(dt % 60)} sec.'
                        + f' (total {info.battle_no})')
            # ready to restart a battle
            click(LOC.finish_next)
            while True:
                page_no = wait_which_target([T.quest, T.restart_quest, T.apply_friend],
                                            [LOC.quest, LOC.restart_quest_yes, LOC.apply_friend])
                if page_no == 0:
                    # in server cn, restart from quest page
                    break
                elif page_no == 2:
                    click(LOC.apply_friend_deny)
                elif page_no == 1:
                    click(LOC.restart_quest_yes)

            # noinspection PyStatementEffect
            label.g
        logger.info(f'>>>>> All {finished} battles "{self.master.quest_name}" finished. <<<<<')

    @with_goto
    def a_zaxiu_final(self, support=True):
        """
        阵容: 豆爸-弓贞(倍卡)-孔明(T1换下去)-CBA-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'a-zaxiu-final'
        master.svt_names = ['豆爸', '弓贞', 'CBA']
        master.set_card_weights([1, 3, 1.2])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (1, 2), (1, 1), (3, 1)],
            [(2, 7), (3, 3), (2, 1), (2, 2)],
            [(1, 0), [(3, 5), (5, 2), (8, 2)], [(1, 5), (5, 3), (8, 1)], [(1, 4), (6, 1), (7, 2)]]
        ])
        if config.jump_battle:
            config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        if support:
            master.choose_support(match_svt=True, match_ce=True, match_ce_max=True)
        else:
            logger.debug('please choose support manually!')
        # wave 1
        # noinspection PyStatementEffect
        label.h
        wait_which_target(T.wave1a, LOC.enemies[0])
        logger.debug(f'Quest {master.quest_name} start...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 1, 2)
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.svt_skill(1, 1)
        master.master_skill(T.wave1a, 3, order_change=(3, 4), order_change_img=T.order_change)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_which_target(T.wave2a, LOC.enemies[0])
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(1, 2)
        master.svt_skill(1, 3, 2)
        master.svt_skill(3, 3, 2)
        master.svt_skill(2, 1)
        master.svt_skill(2, 3)
        master.attack([7, 1, 2])
        # master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(2, 2)
        master.svt_skill(3, 2)
        master.master_skill(T.wave3a, 1)
        master.attack([7, 1, 2])
        # master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def s_zaxiu_final(self, support=True):
        """
        阵容: 豆爸-弓贞(倍卡)-孔明(T1换下去)-CBA-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 's-zaxiu-final'
        master.svt_names = ['豆爸', '弓贞', 'CBA']
        master.set_card_weights([1, 3, 1.2])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (2, 1), (1, 2), (1, 4)],
            [(2, 7), (3, 5), (1, 3), (1, 1)],
            [(1, 0), [(2, 2), (4, 4), (8, 5)], [(3, 1), (4, 1), (7, 2)], [(3, 4), (6, 4), (9, 5)]]
        ])
        if config.jump_battle:
            config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        if support:
            master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, img=T.get('support2'))
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[0])
        logger.debug(f'Quest {master.quest_name} start...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 1, 2)
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.svt_skill(1, 1)
        # noinspection PyStatementEffect
        label.h
        master.master_skill(T.wave1a, 3, order_change=(3, 4), order_change_img=T.order_change)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_which_target(T.wave2a, LOC.enemies[0])
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(1, 2)
        master.svt_skill(1, 3, 2)
        master.svt_skill(3, 3, 2)
        master.svt_skill(2, 1)
        master.svt_skill(2, 3)
        master.attack([7, 1, 2])
        # master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(2, 2)
        master.svt_skill(3, 2)
        master.master_skill(T.wave3a, 1)
        master.attack([7, 1, 2])
        # master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return


# %% supervisor
def supervise_log_time(thread: threading.Thread, secs: float = 60, mail=False, interval=10, mute=True):
    assert thread is not None, thread

    def _overtime():
        return time.time() - config.log_time > secs

    logger.info(f'start supervising thread {thread.name}...')
    thread.start()
    while not thread.is_alive():
        time.sleep(0.01)
    logger.info(f'Thread-{thread.ident}({thread.name}) started...')
    config.log_time = time.time()
    # from here, every logging should have arg: NO_LOG_TIME, otherwise endless loop.
    while True:
        # every case: stop or continue
        # case 1: all right - continue supervision
        if not _overtime():
            time.sleep(interval)
            continue
        # case 2: thread finished normally - stop supervision
        if not thread.is_alive() and config.finished:
            # thread finished
            logger.debug(f'Thread-{thread.ident}({thread.name}) finished. Stop supervising.')
            break

        # something wrong
        # case 3: network error - click "retry" and continue
        if config.img_net is not None and config.loc_net is not None:
            shot = screenshot()
            if is_match_target(shot, config.img_net, config.loc_net[0]) and \
                    is_match_target(shot, config.img_net, config.loc_net[1]):
                logger.warning('Network error! click "retry" button', NO_LOG_TIME)
                click(config.loc_net[1], lapse=5)
                continue
        # case 4: unrecognized error - waiting user to handle (in 30 secs)
        loops = 15
        logger.warning(f'Something went wrong, please solve it\n', NO_LOG_TIME)
        while loops > 0:
            print(f'Or it will be force stopped...')
            loops -= 1
            if mute:
                time.sleep(2)
            else:
                winsound.Beep(600, 1400)
                time.sleep(0.6)
            if not _overtime():
                # case 4.1: user solved the issue and continue supervision
                break
            else:
                # case 4.2: wrong! kill thread and stop
                err_msg = f'Thread-{thread.ident}({thread.name}):' \
                          f' Time run out! lapse={time.time() - config.log_time:.2f}(>{secs}) secs.'
                print(err_msg)
                if mail:
                    subject = f'[{thread.name}]something went wrong!'
                    send_mail(err_msg, subject=subject)
                kill_thread(thread)
                print('exit supervisor after killing thread.')
                return
