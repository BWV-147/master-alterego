"""Store battle_func for different battles"""

# noinspection PyPackageRequirements
from goto import with_goto

from util.master import *
from util.supervisor import send_mail


# noinspection PyPep8Naming,DuplicatedCode
class Battle:
    def __init__(self):
        self.master = Master()
        pass

    @with_goto
    def start(self, battle_func, folder, battle_num=10, total_battle_num=1000, apple=-1, auto_choose_support=True):
        T = self.master.T
        LOC = self.master.LOC
        timer = Timer()
        T.read_templates(folder)
        CONFIG.img_net = T.net_error
        CONFIG.loc_net = LOC.net_error
        CONFIG.task_finished = False
        finished = 0
        info = StatInfo()
        actual_num = min(battle_num, total_battle_num - info.battle_num)
        while finished < actual_num:
            finished += 1
            logger.info(f'>>>>> Battle "{self.master.quest_name}" No.{finished}/{actual_num} <<<<<')
            if CONFIG.jump_start:
                CONFIG.jump_start = False
                logger.warning('outer: goto label.g')
                # noinspection PyStatementEffect
                goto.g
            if not CONFIG.jump_battle:
                while True:
                    shot = screenshot()
                    res = search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))
                    # print(f'res={res}')
                    if res[0] > THR:
                        click(LOC.quest_c)
                    elif is_match_target(shot, T.apple_page, LOC.apple_page):
                        self.master.eat_apple(apple)
                    elif is_match_target(shot, T.support, LOC.support_refresh):
                        break
                    time.sleep(0.5)
            battle_func(auto_choose_support)
            wait_which_target(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            rewards = screenshot()
            logger.info('battle finished, checking rewards.')
            craft_dropped = is_match_target(rewards, T.rewards, LOC.finish_craft)

            if craft_dropped and CONFIG.check_drop:
                info.add_battle(True)
                logger.warning(f'{info.craft_num}th craft dropped!!!')
                rewards.save(f'img/_drops/drops-{self.master.quest_name}-{time.strftime("%m%d-%H-%M-%S")}'
                             + f'-drop{info.craft_num}.png')
                if info.craft_num in CONFIG.enhance_craft_nums:
                    send_mail(f'NEED Enhancement! {info.craft_num}th craft dropped!!!')
                    logger.warning('need to change party or enhance crafts. Exit.')
                    exit()
                else:
                    send_mail(f'{info.craft_num}th craft dropped!!!')
            else:
                info.add_battle(False)
                rewards.save(f"img/_drops/drops-{self.master.quest_name}-{time.strftime('%m%d-%H-%M-%S')}.png")
            dt = timer.lapse()
            CONFIG.count_battle()
            logger.info(f'--- Battle {finished}/{actual_num} finished, time = {int(dt // 60)} min {int(dt % 60)} sec.'
                        + f' (total {info.battle_num})')
            # ready to restart a battle
            click(LOC.finish_next)
            while True:
                shot = screenshot()
                if search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))[0] > THR:
                    break
                elif is_match_target(shot, T.restart_quest, LOC.restart_quest_yes):
                    click(LOC.restart_quest_yes)
                    logger.debug('restart the same battle')
                    break
                elif is_match_target(shot, T.apply_friend, LOC.apply_friend):
                    click(LOC.apply_friend_deny)
                    logger.debug('not to apply friend')
                time.sleep(0.5)
            # noinspection PyStatementEffect
            label.g
        CONFIG.task_finished = True
        logger.info(f'>>>>> All {finished} battles "{self.master.quest_name}" finished. <<<<<')

    @with_goto
    def jp_bond(self, support=True):
        """
        阵容: 狂兰(醉贞)-CBA-CBA(support)-孔明-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'jp-bond'
        master.svt_names = ['狂兰', 'CBA', '孔明']
        master.set_card_weights([3, 1, 1], color_weight='AQB')
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(4, 6), (4, 2), (5, 5), (4, 1)],
            [(4, 0), (4, 3), (4, 4), (6, 4)],
            [(4, 0), (6, 5), (6, 3), (6, 1)],
        ])
        if CONFIG.jump_battle:
            CONFIG.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        if support:
            master.choose_support(match_svt=True, match_ce=False, match_ce_max=False, switch_classes=(5,))
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[0])
        logger.debug(f'Quest {master.quest_name} start...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 3, 1)
        master.svt_skill(3, 1, 1)
        master.svt_skill(2, 1, 1)
        master.svt_skill(1, 3)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_which_target(T.wave2a, LOC.enemies[0])
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(3, 2)
        master.master_skill(T.wave2a, 3, order_change=(3, 4), order_change_img=T.order_change)
        # noinspection PyStatementEffect
        label.h
        master.set_waves(T.get('wave2c'), T.get('wave2d'))
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(3, 1, 1)
        master.svt_skill(2, 3, 1)
        master.svt_skill(2, 2)
        master.master_skill(T.wave3a, 1)
        # master.attack([6, 1, 2])
        master.auto_attack(nps=6)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    # unused
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
        if CONFIG.jump_battle:
            CONFIG.jump_battle = False
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
        if CONFIG.jump_battle:
            CONFIG.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        if support:
            master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, img=T.get('support2'),
                                  switch_classes=(0, 5))
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
