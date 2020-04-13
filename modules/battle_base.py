# noinspection PyPackageRequirements
from goto import with_goto

from modules.master import *
from util.supervisor import supervise_log_time


class BattleBase:
    def __init__(self):
        self.master = Master()

    def pre_process(self, conf=None):
        config.load(conf)
        check_sys_admin()
        config.log_file = 'logs/log.full.log'
        battle_func = getattr(self, config.battle.battle_func)
        battle_func(True)
        config.T = self.master.T
        config.LOC = self.master.LOC

    @with_goto
    def _start(self, battle_func, battle_num, apples=None):
        T = self.master.T
        LOC = self.master.LOC
        timer = Timer()
        finished_num = 0
        max_num = battle_num
        while finished_num < max_num:
            finished_num += 1
            logger.info(f'>>>>> Battle "{self.master.quest_name}" No.{finished_num}/{max_num} <<<<<')
            if config.battle.jump_start:
                config.battle.jump_start = False
                logger.warning('in start: goto label.g')
                # noinspection PyStatementEffect
                goto.g
            if not config.battle.jump_battle:
                while True:
                    shot = screenshot()
                    res = search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))
                    if res[0] > THR:
                        _x = LOC.quest_outer[0] + res[1][0] + (LOC.quest[2] - LOC.quest[0]) / 2
                        _y = LOC.quest_outer[1] + res[1][1] + (LOC.quest[3] - LOC.quest[1]) / 2
                        click((_x, _y))
                    elif is_match_target(shot, T.apple_page, LOC.apple_close):
                        self.master.eat_apple(apples)
                    elif T.get('bag_full_alert') is not None \
                            and is_match_target(shot, T.bag_full_alert, LOC.bag_full_sell_action):
                        # usually used in hunting events.
                        logger.info('bag full, to sell...')
                        click(LOC.bag_full_sell_action)
                        self.sell(config.battle.sell_when_battle)
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
            wait_targets(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            dt = timer.lapse()
            logger.info(f'--- Battle {finished_num}/{max_num} finished,'
                        f' time = {int(dt // 60)} min {int(dt % 60)} sec.'
                        f' (total {config.battle.finished})')
            rewards = screenshot()
            craft_dropped = is_match_target(rewards, T.rewards, LOC.finish_craft)
            png_fn = f'img/_drops/rewards-{self.master.quest_name}-{time.strftime("%m%d-%H%M")}'
            if craft_dropped and config.battle.check_drop:
                config.count_battle(True)
                logger.warning(f'{config.battle.craft_num}th craft dropped!!!')
                rewards.save(f'{png_fn}-drop{config.battle.craft_num}.png')
                if config.battle.craft_num in config.battle.enhance_craft_nums:
                    logger.warning('need to change party or enhance crafts. Exit.')
                    send_mail(f'NEED Enhancement! {config.battle.craft_num}th craft dropped!!!')
                    config.mark_task_finish()
                    return
                else:
                    send_mail(f'{config.battle.craft_num}th craft dropped!!!')
                    click(LOC.finish_next)
            else:
                config.count_battle(False)
                click(LOC.finish_next)
                rewards.save(f"{png_fn}.png")
            # ready to restart a battle
            if finished_num % 30 == 0 and config.mail:
                send_mail(f'Progress: {finished_num}/{max_num} battles finished.', attach_shot=False)
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
        logger.info(f'>>>>> All {finished_num} battles "{self.master.quest_name}" finished. <<<<<')
        if config.mail:
            send_mail(f'All {finished_num} battles "{self.master.quest_name}" finished')
        config.mark_task_finish(False)

    def start(self, supervise=True, conf=None):
        """
        supervise battle progress.
        :param supervise: if True, start battle in child thread, else directly.
        :param conf: config filename, default config.json.
        :return:
        """
        self.pre_process(conf)
        logger.info('starting battle...')
        time.sleep(2)
        battle_func = getattr(self, config.battle.battle_func)
        t_name: str = battle_func.__name__.replace('_', '-').capitalize()
        if config.battle.num <= 0:
            logger.warning(f'no battle, exit.')
            return
        if supervise:
            thread = threading.Thread(target=self._start, name=t_name,
                                      kwargs={"battle_func": battle_func,
                                              "battle_num": config.battle.num,
                                              "apples": config.battle.apples},
                                      daemon=True)
            config.running_thread = thread
            supervise_log_time(thread, 90, interval=3)
        else:
            self._start(battle_func=battle_func, battle_num=config.battle.num, apples=config.battle.apples)

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
        if num <= 0:
            logger.warning('please sell items manually and return to gacha page!', NO_LOG_TIME)
            time.sleep(2)
            config.log_time = time.time() + config.manual_operation_time  # min for manual operation
            raise_alert()
            return
        while True:
            wait_which_target(T.bag_unselected, LOC.bag_sell_action)
            drag(LOC.bag_select_start, LOC.bag_select_end, duration=1, down_time=1, up_time=3)
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
        wait_which_target(T.quest, LOC.quest)
        click(LOC.quest_c)
        logger.debug('from shop back to supporting')
        return

    # noinspection DuplicatedCode
    @with_goto
    def battle_template(self, pre_process=False):
        """
        旧剑(75NP>=60NP)-豆爸50NP-孔明support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-Charlotte'
        names = master.members = ['旧剑', '豆爸', '孔明']
        master.set_card_weight(dict([(svt, [3, 1, 1.1][i]) for i, svt in enumerate(names)]))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.info(f'pre-process for {master.quest_name}...')
            T.read_templates('img/battles/a-charlotte/')

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))

            # -----------------------    NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (3, 6), (1, 5), (1, 3), (3, 3))
            master.set_cards(names[1], (1, 7), (2, 2), (1, 1), (2, 4))
            master.set_cards_from_json(names[2], 'img/cards/android/cards-android.json', '孔明')

            def _handler():
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=True, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        # # noinspection PyStatementEffect
        # label.h  # make sure master.set_waves(a,b) is called
        # master.set_waves(T.waveXa, T.waveXb)
        # noinspection PyStatementEffect
        label.h

        wait_targets(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                                  switch_classes=(5, 0))
        else:
            logger.debug('please choose support manually!')
        time.sleep(2)

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.svt_skill(3, 1, 2)
        master.svt_skill(2, 2)
        master.auto_attack(nps=7)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(2, 1)
        master.master_skill(2, 2)
        master.auto_attack(nps=7)
        # chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        # master.play_cards([chosen_cards[i] for i in (2, 0, 1)])

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(1, 3)
        master.svt_skill(1, 1)
        master.svt_skill(1, 2)
        master.auto_attack(nps=6, mode='alter')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return
