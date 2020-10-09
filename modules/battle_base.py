from goto import with_goto  # noqas

from util.supervisor import *
from .base_agent import *
from .master import *


class BattleBase(BaseAgent):
    def __init__(self):
        super().__init__()
        self.master = Master()
        self.T = self.master.T
        self.LOC = self.master.LOC

    def start(self, supervise=True, cfg=None, force_jump=False):
        """
        Start battle.

        :param supervise: if True, start battle in child thread, else directly.
        :param cfg: config filename, default data/config.json.
        :param force_jump: if True, set True for config.battle.jump_battle, do nothing if False.
                            Just a convenient way to jump other then edit config file.
        :return:
        """
        # pre-processing
        self.pre_process(cfg)
        config.mail = config.battle.mail
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
        if supervise:
            t_name: str = battle_func.__name__.replace('_', '-').title()
            thread = threading.Thread(target=self._start, name=t_name,
                                      kwargs={"battle_func": battle_func,
                                              "battle_num": config.battle.num,
                                              "apples": config.battle.apples},
                                      daemon=True)
            supervise_log_time(thread, 120, interval=3)
        else:
            config.task_thread = threading.current_thread()
            self._start(battle_func=battle_func, battle_num=config.battle.num, apples=config.battle.apples)
        self.post_process()

    def _start(self, battle_func, battle_num, apples=None):
        T = self.T
        LOC = self.LOC
        timer = Timer()
        finished_num = 0
        max_num = battle_num
        while finished_num < max_num:
            finished_num += 1
            logger.info(f'========= Battle "{self.master.quest_name}" No.{finished_num}/{max_num} =========',
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
                        self.master.eat_apple(apples)
                    elif T.bag_full_alert is not None \
                            and match_targets(shot, T.bag_full_alert, LOC.bag_full_sell_button):
                        # usually used in hunting events.
                        logger.info('bag full, to sell...')
                        click(LOC.bag_full_sell_button)
                        self.sell(config.battle.sell_num, 1, 3)
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
                    time.sleep(0.5)
            battle_func()
            wait_targets(T.rewards, LOC.finish_qp, 0.7, clicking=LOC.finish_qp)
            click(LOC.rewards_show_num, lapse=1)
            # check reward_page has CE dropped or not
            dt = timer.lapse()
            logger.info(f'Battle {finished_num}/{max_num} finished, '
                        f'time = {int(dt // 60)} min {int(dt % 60)} sec. '
                        f'(total {config.battle.finished})', extra=LOG_TIME)
            rewards = screenshot()
            drop_dir = f'img/_drops/{self.master.quest_name}'
            if not os.path.exists(drop_dir):
                os.makedirs(drop_dir)
            # png_fn without suffix
            png_fn = os.path.join(drop_dir, f'rewards-{self.master.quest_name}-{time.strftime("%m%d-%H%M")}'
                                            f'-{config.battle.finished + 1}')

            if config.battle.check_drop > 0 and match_targets(rewards, T.rewards,
                                                              LOC.rewards_check_drop[config.battle.check_drop]):
                config.count_battle(True)
                logger.warning(f'{config.battle.craft_num}th craft dropped!!!')
                rewards.save(f'{png_fn}-drop{config.battle.craft_num}.png')
                if config.battle.craft_num in config.battle.enhance_craft_nums:
                    logger.warning('need to change party or enhance crafts. Exit.')
                    send_mail(f'Enhance! {config.battle.craft_num}th craft dropped!!!')
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
            if finished_num % 30 == 0:
                send_mail(f'Progress: {finished_num}/{max_num} battles finished.', attach_shot=False)
            while True:
                shot = screenshot()
                if search_target(shot.crop(LOC.quest_outer), T.quest.crop(LOC.quest))[0] > THR:
                    break
                elif match_targets(shot, T.restart_quest, LOC.restart_quest_yes):
                    break
                elif match_targets(shot, T.apply_friend, LOC.apply_friend):
                    click(LOC.apply_friend_deny)
                    logger.debug('not to apply friend')
                time.sleep(0.5)
        logger.info(f'>>>>> All {finished_num} battles "{self.master.quest_name}" finished. <<<<<')
        send_mail(f'All {finished_num} battles "{self.master.quest_name}" finished')
        config.mark_task_finish()
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
            T.read_templates(['img/battles/.a', 'img/battles/a-charlotte/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (3, 6), (1, 5), (1, 3), (3, 3))
            master.set_cards(names[1], (1, 7), (2, 2), (1, 1), (2, 4))
            # here 'android' default to 'img/battles/cards/android/cards-android.json',
            # use full path if not match the default pattern
            master.set_cards_from_json('孔明', 'android')

            def _handler():
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = _handler
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
        master.auto_attack(nps=6, mode='alter', buster_first=True)
        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return
