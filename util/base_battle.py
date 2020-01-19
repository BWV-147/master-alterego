# noinspection PyPackageRequirements
from goto import with_goto

from util.master import *
from util.supervisor import supervise_log_time


class BattleBase:
    def __init__(self):
        self.master = Master()

    @with_goto
    def start(self, battle_func, battle_num, apples=None):
        T = self.master.T
        LOC = self.master.LOC
        timer = Timer()
        battle_func(True)
        BaseConfig.img_net = T.net_error
        BaseConfig.loc_net = LOC.net_error
        BaseConfig.task_finished = False
        finished_num = 0
        actual_max_num = min(battle_num, config.max_finished_battles - config.finished_battles)
        while finished_num < actual_max_num:
            finished_num += 1
            logger.info(f'>>>>> Battle "{self.master.quest_name}" No.{finished_num}/{actual_max_num} <<<<<')
            if config.jump_start:
                config.jump_start = False
                logger.warning('in start: goto label.g')
                # noinspection PyStatementEffect
                goto.g
            if not config.jump_battle:
                while True:
                    shot = screenshot()
                    res = search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))
                    if res[0] > THR:
                        click(LOC.quest_c)
                    elif is_match_target(shot, T.apple_page, LOC.apple_page):
                        if self.master.eat_apple(apples) is False:
                            return
                    elif is_match_target(shot, T.get('bag_full_alert', LOC.gen_empty_img()), LOC.bag_full_sell_action):
                        # usually used in hunting events.
                        logger.info('bag full, to sell...')
                        click(LOC.bag_full_sell_action)
                        self.sell(1)
                    elif is_match_target(shot, T.restart_quest, LOC.restart_quest_yes):
                        click(LOC.restart_quest_yes)
                        logger.debug('restart the same battle')
                    elif is_match_target(shot, T.apply_friend, LOC.apply_friend):
                        click(LOC.apply_friend_deny)
                        logger.debug('not to apply friend')
                    elif is_match_target(shot, T.support, LOC.support_refresh):
                        break
                    time.sleep(0.5)
            battle_func()
            wait_which_target(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            dt = timer.lapse()
            logger.info(f'--- Battle {finished_num}/{actual_max_num} finished,'
                        f' time = {int(dt // 60)} min {int(dt % 60)} sec.'
                        f' (total {config.finished_battles})')
            rewards = screenshot()
            craft_dropped = is_match_target(rewards, T.rewards, LOC.finish_craft)
            png_fn = f'img/_drops/rewards-{self.master.quest_name}-{time.strftime("%m%d-%H%M")}'
            if craft_dropped and config.check_drop:
                config.count_battle(True)
                logger.warning(f'{config.craft_num}th craft dropped!!!')
                rewards.save(f'{png_fn}-drop{config.craft_num}.png')
                if config.craft_num in config.enhance_craft_nums:
                    send_mail(f'NEED Enhancement! {config.craft_num}th craft dropped!!!')
                    logger.warning('need to change party or enhance crafts. Exit.')
                    BaseConfig.task_finished = True
                    return
                else:
                    send_mail(f'{config.craft_num}th craft dropped!!!')
            else:
                config.count_battle(False)
                rewards.save(f"{png_fn}.png")
            # ready to restart a battle
            click(LOC.finish_next)
            if finished_num % 30 == 0:
                send_mail(f'Progress: {finished_num}/{actual_max_num} battles finished.', attach_shot=False)
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
        BaseConfig.task_finished = True
        logger.info(f'>>>>> All {finished_num} battles "{self.master.quest_name}" finished. <<<<<')
        if config.mail:
            send_mail(f'All {finished_num} battles "{self.master.quest_name}" finished')

    def start_with_supervisor(self, check=True, conf=None):
        """
        supervise battle progress.
        :param check: if True, start battle in child thread, else start battle directly.
        :param conf: config filename, default config.json.
        :return:
        """
        config.load_config(conf)
        check_sys_admin()
        BaseConfig.task_finished = False
        BaseConfig.log_file = 'logs/log.full.log'
        logger.info('start battle...')
        time.sleep(2)
        battle_func = getattr(self, config.battle_func)
        t_name: str = battle_func.__name__.replace('_', '-').capitalize()
        if config.battle_num <= 0 or config.finished_battles >= config.max_finished_battles:
            logger.warning(f'no battle, exit.')
            return
        if check:
            thread = threading.Thread(target=self.start, name=t_name,
                                      kwargs={"battle_func": battle_func,
                                              "battle_num": config.battle_num,
                                              "apples": config.apples},
                                      daemon=True)
            supervise_log_time(thread, 90, interval=3)
        else:
            self.start(battle_func=battle_func, battle_num=config.battle_num, apples=config.apples)

    @with_goto
    def battle_template(self, pre_process=False):
        """
        template procedures of a battle.
        :param pre_process: if True, only do pre-processing, no battle executed.
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'template'
        T.read_templates('img/template-jp')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['X', 'Y', 'Z'])
        master.show_svt_name = True
        master.set_card_weights([2, 3, 1])
        # ----  NP     Quick    Arts   Buster ----
        # master.set_card_templates([
        #     [(1, 6), (3, 3), (2, 3), (1, 2)],
        #     [(3, 7), (1, 4), (1, 1), (2, 4)],
        #     [(1, 0), (2, 1), (2, 2), (1, 3)],
        # ])
        if pre_process:
            return

        # battle part
        if config.jump_battle:
            config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        # # noinspection PyStatementEffect
        # label.h  # make sure master.set_waves(a,b) is called
        # master.set_waves(T.waveXa, T.waveXb)
        # noinspection PyStatementEffect
        label.h
        wait_which_target(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support_drag(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                                       switch_classes=(-1,))
        else:
            logger.debug('please choose support manually!')
        time.sleep(2)
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[0])
        logger.debug(f'Quest {master.quest_name} started...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(1, 1)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_which_target(T.wave2a, LOC.enemies[0])
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(1, 3)
        # master.attack([6, 1, 2])
        click(LOC.enemies[1])
        chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        # master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        # master.attack([6, 1, 2])
        master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    def sell(self, num=100):
        """
        Called when bag full before entering quest, usually hunting events. Back to supporting finally.
        :param num: selling times. 100~=ALL
        """
        T = self.master.T
        LOC = self.master.LOC
        logger.info('shop: selling...')
        print('Make sure the bag **FILTER** only shows "Experience Cards"/"Zhong Huo"!')
        no = 0
        while True:
            wait_which_target(T.bag_unselected, LOC.bag_sell_action)
            drag(LOC.bag_select_start, LOC.bag_select_end, duration=1, down_time=1, up_time=4)
            page_no = wait_which_target([T.bag_selected, T.bag_unselected], [LOC.bag_sell_action, LOC.bag_sell_action])
            if page_no == 0:
                no += 1
                logger.debug(f'sell {no} times.')
                click(LOC.bag_sell_action)
                wait_which_target(T.bag_sell_confirm, LOC.bag_sell_confirm, at=True)
                wait_which_target(T.bag_sell_finish, LOC.bag_sell_finish, at=True)
                if no >= num:
                    break
            elif page_no == 1:
                logger.debug('all items are sold.')
                break
        wait_which_target(T.bag_unselected, LOC.bag_sell_action)
        click(LOC.bag_back)
        wait_which_target(T.shop, LOC.shop_event_item_exchange)
        click(LOC.bag_back)
        wait_which_target(T.quest, LOC.quest_master_avatar)
        click(LOC.quest_c)
        logger.debug('from shop back to supporting')
        return
