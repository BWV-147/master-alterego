from util.goto import *
from util.supervisor import *
from .base_agent import *
from .master import *


class BattleBase(BaseAgent):
    def __init__(self):
        self.master = Master()
        super().__init__()

    @property
    def T(self):  # noqa
        return self.master.T

    @T.setter
    def T(self, value):  # noqa
        self.master.T = value

    @property
    def LOC(self):  # noqa
        return self.master.LOC

    @LOC.setter
    def LOC(self, value):  # noqa
        self.master.LOC = value

    def start(self, timeout: int = None, cfg=None, force_jump=False):
        """
        Start battle.

        :param timeout: timeout limit for child thread, if non positive, start battle in main thread, timeout
        :param cfg: config filename, default data/config.json.
        :param force_jump: if True, set True for config.battle.jump_battle, do nothing if False.
                            Just a convenient way to jump other then edit config file.
        :return:
        """
        if timeout is None:
            timeout = 120
        # pre-processing
        self.pre_process(cfg)
        config.mail = config.battle.mail
        self.LOC.relocate(config.battle.location)
        battle_func = getattr(self, config.battle.battle_func)
        battle_func(True)
        config.T = self.T
        config.LOC = self.LOC
        if force_jump:
            config.battle.jump_battle = True
        if config.battle.num <= 0:
            logger.warning(f'no battle, exit.')
            return

        # starting
        logger.info('starting battle...', extra=LOG_TIME)
        time.sleep(2)
        if timeout > 0:
            t_name: str = battle_func.__name__.replace('_', '-').title()
            thread = threading.Thread(target=self._start, name=t_name,
                                      kwargs={"battle_func": battle_func,
                                              "battle_num": config.battle.num,
                                              "apples": config.battle.apples},
                                      daemon=True)
            supervise_log_time(thread, timeout, interval=3)
        else:
            config.task_thread = threading.current_thread()
            self._start(battle_func=battle_func, battle_num=config.battle.num, apples=config.battle.apples)
        self.post_process()

    def _start(self, battle_func, battle_num, apples=None):
        T = self.T
        LOC = self.LOC
        timer = Timer()
        finished_num = 0
        while config.battle.end_until_eating_apple or finished_num < battle_num:
            finished_num += 1
            logger.info(f'========= Battle "{self.master.quest_name}" No.{finished_num}/{battle_num} =========',
                        extra=LOG_TIME)
            if not config.battle.jump_battle:
                while True:
                    shot = screenshot()
                    res = search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))
                    if res[0] > THR:
                        # match quest entrance
                        _x = LOC.quest_outer[0] + res[1][0] + (LOC.quest[2] - LOC.quest[0]) / 2
                        _y = LOC.quest_outer[1] + res[1][1] + (LOC.quest[3] - LOC.quest[1]) / 2
                        click((_x, _y))
                    elif match_targets(shot, T.apple_page, LOC.apple_close):
                        if finished_num > battle_num and config.battle.end_until_eating_apple:
                            config.mark_task_finish(f'Finished: all {battle_num} battles finished and AP cleared')
                        else:
                            self.master.eat_apple(apples)
                    elif T.bag_full_alert is not None \
                            and match_targets(shot, T.bag_full_alert, LOC.bag_full_sell_button):
                        # usually used in hunting events.
                        logger.info('bag full, to sell...')
                        click(LOC.bag_full_sell_button)
                        self.sell(config.battle.sell_times, 1, 3)
                        wait_search_template(T.quest.crop(LOC.quest), LOC.quest_outer)
                        logger.debug('back from shop to quest', extra=LOG_TIME)
                    elif match_targets(shot, T.restart_quest, LOC.restart_quest_yes):
                        click(LOC.restart_quest_yes)
                        logger.debug('restart the same battle')
                    elif match_targets(shot, T.apply_friend, LOC.apply_friend):
                        click(LOC.apply_friend_deny)
                        logger.debug('not to apply friend')
                    elif match_targets(shot, T.quest, LOC.menu_button):
                        # maybe re-login when daily refresh
                        if callable(config.battle.login_handler):
                            config.battle.login_handler()
                    elif match_targets(shot, T.support, LOC.support_refresh):
                        break
                    sleep(0.5)

            battle_func()

            config.count_battle()
            dt = timer.lapse()
            logger.info(f'Battle {finished_num}/{battle_num} finished, '
                        f'time = {int(dt // 60)} min {int(dt % 60)} sec. '
                        f'(total {config.battle.finished})', extra=LOG_TIME)

            # wait_targets(T.rewards, LOC.rewards_qp, 0.5, clicking=LOC.rewards_clicking)
            page_no = wait_which_target([T.craft_detail, T.rewards_init], [LOC.craft_detail_tab1, LOC.rewards_show_num],
                                        clicking=LOC.rewards_clicking)
            if page_no == 0:
                config.mark_task_finish('Interrupted: Bone craft!!!', MailLevel.warning)
                return

            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            rewards = screenshot()
            drop_dir = f'img/_drops/{self.master.quest_name}'
            if not os.path.exists(drop_dir):
                os.makedirs(drop_dir)
            # png_fn without suffix
            png_fn = os.path.join(drop_dir, f'rewards-{self.master.quest_name}-{time.strftime("%m%d-%H%M")}'
                                            f'-{config.battle.finished}')
            if config.battle.check_drop > 0 and self.master.check_rewards(rewards, config.battle.check_drop):
                config.record_craft_drop()
                logger.warning(f'{config.battle.craft_num}th craft dropped!!!')
                rewards.save(f'{png_fn}-drop{config.battle.craft_num}.png')
                if config.battle.craft_num in config.battle.enhance_craft_nums:
                    logger.warning('need to change party or enhance crafts. Exit.')
                    config.mark_task_finish(f'Enhance! {config.battle.craft_num}th craft dropped!!!', MailLevel.warning)
                    return
                else:
                    send_mail(f'{config.battle.craft_num}th craft dropped!!!', level=MailLevel.warning)
                click(LOC.rewards_next)
            else:
                click(LOC.rewards_next)
                rewards.save(f"{png_fn}.png")

            # ready to restart a battle
            if finished_num % 30 == 0:
                send_mail(f'Progress: {finished_num}/{battle_num} battles finished.',
                          attach_shot=False, level=MailLevel.info)
            while True:
                shot = screenshot()
                if search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))[0] > THR:
                    break
                elif match_targets(shot, T.restart_quest, LOC.restart_quest_yes):
                    break
                elif match_targets(shot, T.apply_friend, LOC.apply_friend):
                    click(LOC.apply_friend_deny)
                    logger.debug('not to apply friend')
                sleep(0.5)
        logger.info(f'>>>>> All {finished_num} battles "{self.master.quest_name}" finished. <<<<<')
        send_mail(f'All {finished_num} battles "{self.master.quest_name}" finished', level=MailLevel.info)
        config.mark_task_finish(f'Finished: all {finished_num} battles of "{self.master.quest_name}"')
        return

    # noinspection DuplicatedCode
    @with_goto
    def battle_template(self, pre_process=False):
        """
        Template of a battle.
        旧剑(75NP>=60NP)-豆爸50NP-孔明support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-Charlotte'  # should be a valid folder name
        names = master.members = ['旧剑', '豆爸', '孔明']
        master.set_card_weight(dict(zip(names, [3, 1, 1.1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.info(f'pre-process for {master.quest_name}...', extra=LOG_TIME)
            T.read_templates(['img/share/android', 'img/battles/a-charlotte/'])

            # LOC.relocate((0, 0, 1920, 1080))

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (3, 6), (1, 5), (1, 3), (3, 3))
            master.set_cards(names[1], (1, 7), (2, 2), (1, 1), (2, 4))
            # here 'android' default to 'img/share/{device}/cards/cards.json',
            # use full path if not match the default pattern
            master.set_cards_from_json('孔明', 'android')

            def _handler():
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = _handler or None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        # use different process with different support servant
        # noinspection PyUnusedLocal
        support = master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                                        friend_only=False, switch_classes=(5, 0),
                                        images=[T.support, T.support_cba])

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            # skills must place in with-statement, or use svt_skill_full/master_skill_full
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(3, 1, 2)
            master.svt_skill(2, 2)
        master.auto_attack(nps=7)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(2, 1)
            master.master_skill(2, 2)
        master.auto_attack(nps=7)
        # chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        # master.play_cards([chosen_cards[i] for i in (2, 0, 1)])

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 3)
            master.svt_skill(1, 1)
            master.svt_skill(1, 2)
        master.auto_attack(nps=6, mode=AttackMode.alter, buster_first=True)
        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.alter, allow_unknown=True)
        return

    def default_login_handler(self, quest_regions=None):
        """Handle login event at 3am(UTC+8) for jp server, back to quest/support page at last.
        This should be called in supervisor thread.

        To pass parameters, use lambda function:

        config.battle.login_handler = lambda: self.default_login_handler(params)

        :return: True if successfully back to quest/support page
        """

        T, LOC = self.T, self.LOC
        if match_which_target(screenshot(), [T.login_news, T.login_popup], [LOC.login_news_close, LOC.menu_button]) < 0:
            return False

        logger.warning('Handle login or popups')
        # if reach time limit, failed, return False
        time_limit = 120
        t0 = time.time()

        if quest_regions is None:
            quest_regions = [LOC.quest]
        while True:
            shot = screenshot()
            if match_targets(shot, T.login_news, LOC.login_news_close):
                click(LOC.login_news_close)
                logger.debug('close login news page')
            elif match_targets(shot, T.login_terminal, LOC.login_terminal_event_banner):
                click(LOC.login_terminal_event_banner)
                logger.debug('enter event banner')
                time.sleep(3)
            elif match_targets(shot, T.quest, quest_regions):
                click(LOC.quest_c)
                logger.debug('enter quest')
            elif match_targets(shot, T.login_popup, LOC.menu_button):
                click(LOC.login_popup_clicking)
            elif match_targets(T.support, LOC.support_refresh):
                logger.debug('back to support page!')
                return True
            time.sleep(3)
            if time.time() - t0 > time_limit:
                return False
