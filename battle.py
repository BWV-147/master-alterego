"""Store battle_func for different battles"""
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
            craft_dropped = match_which_target(rewards, T.rewards, LOC.finish_craft) >= 0

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
