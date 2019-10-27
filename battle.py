"""Store battle_func for different battles"""
# noinspection PyPackageRequirements
from goto import with_goto
from concurrent.futures import ThreadPoolExecutor
from util.master import *


# noinspection PyPep8Naming,DuplicatedCode
class Battle:
    def __init__(self):
        self.master = Master()
        pass

    @with_goto
    def start(self, battle_func, num=10, apple=-1, support=True):
        T = self.master.T
        LOC = self.master.LOC
        timer = Timer()
        finished = 0
        info = StatInfo()
        while finished < num:
            timer.start()
            finished += 1
            logger.info(f'>>>>> Battle "{self.master.quest_name}" No.{finished}/{num} <<<<<')
            if Config.jump_start:
                Config.jump_start = False
                logger.warning('outer: goto label.g')
                # noinspection PyStatementEffect
                goto.g
            battle_func(support)
            wait_which_target(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            # noinspection PyStatementEffect
            label.g
            rewards = screenshot()
            logger.info('battle finished, checking rewards.')
            craft_dropped = match_which_target(rewards, T.rewards, LOC.finish_craft) >= 0
            if craft_dropped and Config.check_drop:
                logger.warning(f'{info.craft_num}th craft dropped!!!')
                rewards.save(f'img/_drops/craft-{self.master.quest_name}-{time.strftime("%m%d-%H-%M-%S")}'
                             + f'-drop{info.craft_num}.png')
                if info.craft_num in (5, 8, 9, 12, 13, 16, 17, 20, 21, 25):
                    send_mail(f'NEED Enhancement! {info.craft_num}th craft dropped!!!')
                    logger.warning('need to change party or enhance crafts. Exit.')
                    exit()
                else:
                    send_mail(f'{info.craft_num}th craft dropped!!!')
            else:
                rewards.save(f"img/_drops/craft-{self.master.quest_name}-{time.strftime('%m%d-%H-%M-%S')}.png")
            dt = timer.stop().dt
            info.add_battle(craft_dropped, int(dt))
            info.save()
            logger.info(f'--- Battle {finished}/{num} finished, time = {int(dt // 60)} min {int(dt % 60)} sec.'
                        + f' (total {info.battle_no})')
            # ready to restart a battle
            click(LOC.finish_next)
            while True:
                page_no = wait_which_target([T.quest, T.restart_quest, T.apply_friend],
                                            [LOC.quest, LOC.restart_quest_yes, LOC.apply_friend])
                if page_no == 0:
                    # in server cn, restart from quest page
                    click(LOC.quest_c)
                    break
                elif page_no == 2:
                    click(LOC.apply_friend_deny)
                elif page_no == 1:
                    click(LOC.restart_quest_yes)
                    break

            page_no = wait_which_target([T.apple_page, T.support], [LOC.apple_page, LOC.support_refresh])
            if page_no == 0:
                self.master.eat_apple(apple)
        logger.info(f'>>>>> All {finished} battles "{self.master.quest_name}" finished. <<<<<')

    @with_goto
    def a_zaxiu(self, support=True):
        """
        阵容: CBA-狂兰(醉贞)-CBA2-孔明-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'a-zaxiu-1'
        master.svt_names = ['CBA', '狂兰', '孔明']
        T.read_templates('img/a-zaxiu-1')
        master.set_card_weights([1, 3, 1, 1])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates(
            [[(1, 0), [(3, 1), (4, 4), (7, 5)], [(1, 5), (5, 4), (7, 1)], [(2, 4), (5, 3), (8, 4)]],
             [(1, 7), (2, 3), (3, 2), (1, 1)],
             [(1, 0), (6, 1), (2, 5), (7, 4)]
             ])
        Config.img_net = T.net_error
        Config.loc_net = LOC.net_error
        if Config.jump_battle:
            Config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        print('at support choosing page.')
        if support:
            master.choose_support(match_svt=False, match_ce=False, match_ce_max=False)
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[1])
        logger.debug('Quest zaxiu-caster start...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b) \
            .svt_skill(3, 1, 2) \
            .svt_skill(3, 3, 2) \
            .svt_skill(1, 1, 2) \
            .svt_skill(2, 3)
        # master.attack([7, 1, 2])
        master.auto_attack(nps=7)

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.svt_skill(T.wave2a, T.wave2b, 3, 2)
        master.master_skill(T.wave2a, 3, order_change=(3, 4), order_change_img=T.order_change)
        master.svt_skill_full(T.get('wave2c'), T.get('wave2d'), 3, 1, 2)
        master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b) \
            .svt_skill(1, 3, 2) \
            .svt_skill(1, 2) \
            .svt_skill(3, 2) \
            .svt_sll(3, 3) \
            .master_skill(T.wave3a, 1)
        # noinspection PyStatementEffect
        label.h
        master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def a_zaxiu_ass(self, support=True):
        """
        阵容: 豆爸-齐格(倍卡)-孔明(T1换下去)-CBA-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'a-zaxiu-ass'
        master.svt_names = ['豆爸', '齐格', 'CBA']
        T.read_templates('img/a-zaxiu-ass')
        master.set_card_weights([1, 3, 1.2])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (2, 4), (2, 5), (2, 3)],
            [(1, 7), (1, 1), (1, 2), (1, 5)],
            [(1, 0), (2, 1), (3, 3), (1, 3)]
        ])
        Config.img_net = T.net_error
        Config.loc_net = LOC.net_error
        if Config.jump_battle:
            Config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        if support:
            master.choose_support(match_svt=True, match_ce=True, match_ce_max=True)
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[0])
        logger.debug(f'Quest {master.quest_name} start...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b) \
            .svt_skill(3, 1, 2) \
            .svt_skill(3, 2) \
            .svt_skill(3, 3) \
            .svt_skill(1, 1) \
            .svt_skill(1, 2)
        master.master_skill(T.wave1a, 3, order_change=(3, 4), order_change_img=T.order_change)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_which_target(T.wave2a, LOC.enemies[0])
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b) \
            .svt_skill(3, 3, 2) \
            .svt_skill(1, 3, 2) \
            .svt_skill(2, 1) \
            .svt_skill(2, 2)
        # noinspection PyStatementEffect
        label.h
        master.attack([7, 1, 2])
        # master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b) \
            .svt_skill(2, 3) \
            .svt_skill(3, 2)
        # master.master_skill(T.wave3a, 1)
        master.attack([7, 1, 2])
        # master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return


# %% backup, old version
# noinspection DuplicatedCode
class BattleBackup:
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
            ce.save(f"img/craft/craft-{self.master.quest_name}-{time.strftime('%m%d-%H-%M-%S')}.png")
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
    def steel_android(self, apple=-1):
        """
        阵容：杀师匠（醉贞）-茶茶（满破虚数）-孔明-X-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'charlotte-android'
        master.svt_names = ['bba', '茶茶', '孔明']
        T.read_templates('img/steel-android')
        master.LOC.relocate((88, 44, 88 + 1742, 44 + 982))
        master.set_card_weights([3, 2, 1])
        # ---------------------------  NP    Quick    Arts    Buster ----
        master.set_card_templates([[(4, 6), (2, 1), (3, 5), (1, 4)],
                                   [(4, 7), (3, 2), (2, 4), (2, 3)],
                                   [(0, 0), (1, 3), (1, 2), (1, 1)]])
        if Config.jump_battle:
            Config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.quest, LOC.quest, at=True)
        page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no == 1:
            master.eat_apple(-1, False)
        master.choose_support(match_ce=True, match_ce_max=True)
        # wait_which_target(T.team, LOC.team, at=True, clicking=(1387, 114), interval=5)
        logger.debug('start battle!')
        # logger.info('Quest Charlotte-android start...')
        # wave 1
        # noinspection PyStatementEffect
        label.h
        wait_which_target(T.wave1a, LOC.enemies[2])
        wait_which_target(T.wave1a, LOC.master_skill)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 2)
        master.svt_skill_full(T.wave1a, T.wave1b, 2, 1)
        # master.svt_skill2(T.wave1a, T.wave1b, 3, 1, 1)
        # master.svt_skill2(T.wave1a, T.wave1b, 1, 2)
        # master.auto_attack(6)
        # master.attack([6, 1, 2])

        master.xjbd(T.wave2a, ([274, 103, 391, 132], [634, 103, 751, 132], [994, 103, 1111, 132]))

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill)
        master.svt_skill_full(T.wave2a, T.wave2b, 3, 3)
        # master.master_skill(T.wave2a, 2, 1)

        master.auto_attack(nps=7)
        # master.attack([6, 1, 2])
        # master.xjbd(T.wave3a, LOC.enemies)

        # wave 3
        wait_which_target(T.wave3a, LOC.master_skill)
        click(LOC.enemies[0])
        master.svt_skill_full(T.wave3a, T.wave3b, 3, 1, 1)
        master.svt_skill_full(T.wave3a, T.wave3b, 2, 3)
        master.svt_skill_full(T.wave3a, T.wave3b, 1, 1)
        master.svt_skill_full(T.wave3a, T.wave3b, 1, 3)

        master.master_skill(T.wave3a, 2, 1)
        master.auto_attack(6)

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)

        return

    # Free
    @with_goto
    def charlotte_android(self, apple=-1):
        """
        阵容：豆爸（醉贞）-旧剑（虚数）-孔明-X-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'charlotte-android'
        master.svt_names = ['豆爸', '旧剑', '孔明']
        T.read_templates('img/charlotte')
        # master.LOC.relocate((106, 60, 1813, 1020))
        master.set_card_weights([2, 3, 2])
        # ---------------------------  NP    Quick    Arts    Buster ----
        master.set_card_templates([[(1, 6), (3, 4), (2, 2), (1, 4)],
                                   [(3, 7), (3, 5), (3, 2), (1, 1)],
                                   [(0, 0), (1, 3), (2, 3), (1, 5)]])
        if Config.jump_battle:
            Config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.quest, LOC.quest, at=True)
        page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no == 1:
            master.eat_apple(-1, False)
        # master.choose_support(match_ce=True, match_ce_max=True)
        wait_which_target(T.team, LOC.team, at=True, clicking=(1387, 114), interval=5)
        # logger.info('Quest Charlotte-android start...')
        # wave 1
        # wait_which_target(T.wave1a, LOC.enemies[2])
        wait_which_target(T.wave1a, LOC.master_skill)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 2)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 1, 1)
        master.svt_skill_full(T.wave1a, T.wave1b, 1, 2)
        # master.auto_attack(6)
        master.attack([6, 1, 2])
        # master.xjbd(T.wave2a, LOC.enemies)

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill)
        master.svt_skill_full(T.wave2a, T.wave2b, 1, 1)
        master.master_skill(T.wave2a, 2, 1)
        # noinspection PyStatementEffect
        label.h
        master.auto_attack(nps=6)
        # master.attack([6, 1, 2])
        # master.xjbd(T.wave3a, LOC.enemies)

        # wave 3
        wait_which_target(T.wave3a, LOC.master_skill)
        master.svt_skill_full(T.wave3a, T.wave3b, 1, 3, 1)
        master.svt_skill_full(T.wave3a, T.wave3b, 2, 1)
        master.svt_skill_full(T.wave3a, T.wave3b, 2, 2)
        master.svt_skill_full(T.wave3a, T.wave3b, 2, 3)
        # click(LOC.enemies[1])

        master.auto_attack(7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg')

        return

    @with_goto
    def charlotte_ios(self, apple=-1):
        """
        阵容：豆爸（醉贞）-lily（宝石）-孔明-X-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        master.quest_name = 'charlotte-ios'
        master.svt_names = ['豆爸', 'lily', '孔明']
        LOC.relocate((177, 74, 1741, 954))  # maximize with task bar
        T.read_templates('img/charlotte-ios')
        master.set_card_weights([2, 3, 2])
        # ---------------------------  NP    Quick    Arts    Buster ----
        master.set_card_templates([[(1, 0), (3, 1), (1, 1), (2, 2)],
                                   [(1, 0), (1, 4), (1, 5), (1, 4)],
                                   [(0, 0), (3, 2), (3, 4), (3, 3)]])
        if Config.jump_battle:
            Config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.quest, LOC.quest, at=True)
        page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no == 1:
            master.eat_apple(-1, False)
        master.choose_support(match_ce=True, match_ce_max=True)
        # logger.info('Quest Charlotte-iOS start...')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[2])
        wait_which_target(T.wave1a, LOC.master_skill)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 2)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 1, 1)
        master.svt_skill_full(T.wave1a, T.wave1b, 1, 2)
        master.attack([6, 1, 2])
        # master.xjbd(T.wave2a, LOC.enemies)

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill)
        master.svt_skill_full(T.wave2a, T.wave2b, 1, 1)
        # master.svt_skill2(T.wave2a, T.wave2b, 1, 2)
        master.master_skill(T.wave2a, 2, 1)
        master.attack([6, 1, 2])
        # master.xjbd(T.wave3a, LOC.enemies)

        # noinspection PyStatementEffect
        label.h
        # wave 3
        wait_which_target(T.wave3a, LOC.master_skill)
        # master.svt_skill2(T.wave3a, T.wave3b, 2, 1)
        master.svt_skill_full(T.wave3a, T.wave3b, 2, 2)
        # master.svt_skill2(T.wave3a, T.wave3b, 2, 3)
        # click(LOC.enemies[1])

        master.attack([7, 1, 2])
        master.xjbd(T.kizuna, LOC.kizuna, 'xjbd')

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
        # master.set_card_templates([[(1, 0), (0, 0), (0, 0), (0, 0)],
        #                            [(2, 7), (3, 1), (3, 2), (1, 2)],
        #                            [(2, 0), (2, 3), (2, 5), (2, 4)],
        #                            [(1, 6), (1, 1), (1, 5), (3, 3)]])
        if Config.jump_battle:
            Config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.quest, LOC.quest, at=True)
        page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no == 1:
            master.eat_apple(apple, True)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=False)
        logger.debug('Quest Chaos-android start...')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[2])
        wait_which_target(T.wave1a, LOC.master_skill)
        master.svt_skill_full(T.wave1a, T.wave1b, 1, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 2, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 2)

        # noinspection PyStatementEffect
        label.h
        master.attack([6, 1, 2])

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill, lapse=1, clicking=LOC.safe_area)
        master.svt_skill_full(T.wave2a, T.wave2b, 2, 1)
        master.svt_skill_full(T.wave2a, T.wave2b, 2, 2)
        master.svt_skill_full(T.wave2a, T.wave2b, 3, 3)
        master.attack([7, 1, 2])

        # wave 3
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        master.svt_skill_full(T.wave3a, T.wave3b, 1, 3)
        master.svt_skill_full(T.wave3a, T.wave3b, 3, 1, 1)
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
        LOC.relocate((178, 75, 1742, 955))
        master.set_card_weights([1, 3, 2, 3])
        # ---------------------------  NP    Quick    Arts    Buster ----
        # master.set_card_templates([[(1, 0), (3, 0), (2, 0), (1, 0)],
        #                            [(2, 7), (3, 1), (3, 2), (1, 2)],
        #                            [(2, 0), (2, 3), (2, 5), (2, 4)],
        #                            [(1, 6), (1, 1), (1, 5), (3, 3)]])
        if Config.jump_battle:
            Config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.quest, LOC.quest, at=True)
        page_no = wait_which_target([T.support, T.apple_page], [LOC.support_team_icon, LOC.apple_page])
        if page_no == 1:
            master.eat_apple(apple, False)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=False)
        logger.debug('Quest Chaos-iOS start...')

        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[2])
        wait_which_target(T.wave1a, LOC.master_skill)
        master.svt_skill_full(T.wave1a, T.wave1b, 1, 3)
        master.attack([6, 1, 2])

        # wave 2
        wait_which_target(T.wave2a, LOC.master_skill, lapse=1, clicking=LOC.safe_area)
        master.svt_skill_full(T.wave2a, T.wave2b, 3, 2)
        master.svt_skill_full(T.wave2a, T.wave2b, 3, 3)
        master.svt_skill_full(T.wave2a, T.wave2b, 1, 3)
        master.attack([6, 1, 2])

        # wave 3
        wait_which_target(T.wave3a, LOC.master_skill, lapse=1)
        master.svt_skill_full(T.wave3a, T.wave3b, 2, 3)
        master.svt_skill_full(T.wave3a, T.wave3b, 3, 1, 2)
        master.master_skill(T.wave3a, 2, 2)
        # noinspection PyStatementEffect
        label.h
        master.attack([7, 1, 2])
        master.xjbd(T.kizuna, LOC.kizuna, mode='xjbd')
        return
