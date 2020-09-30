"""Store battle_func for different battles

- wrap @with_goto to enable goto and label statement.
- for card template of common used servants who have 3+dress sets of models(e.g. Kongming/CBA/Merlin),
  save all models' cards info(json) and templates into the same folder(e.g. `img/cards/jp/`).
  Then use `master.set_cards_from_json()` to load it.
- ensure the same app version(current & saved screenshots): e.g. command card's text might differ.
"""
from modules.battle_base import *


# noinspection DuplicatedCode
class AFree(BattleBase):
    @with_goto
    def a_smolensk(self, pre_process=False):
        """
        尼托(醉贞)-弓凛(空骑)-孔明support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-Smolensk'
        names = master.members = ['尼托', '弓凛', '孔明']
        master.set_card_weight(dict(zip(names, [1.01, 2, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.a', 'img/battles/free/a-smolensk/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (1, 3), (1, 4), (2, 3))
            master.set_cards(names[1], (3, 7), (2, 5), (2, 1), (1, 5))
            master.set_cards_from_json(names[2], 'img/cards/android/cards-android.json', '孔明')

            def _handler():  # noqas
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                              switch_classes=(5, 0), friend_only=False)

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(3, 1, 1)
            master.svt_skill(2, 1)
            master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(1, 2)
            master.svt_skill(2, 3)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 2)
            master.master_skill(2, 2)
        master.auto_attack(nps=7, mode='dmg')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return

    @with_goto
    def a_egg(self, pre_process=False):
        """
        阿福(相扑)-小贝(虚数)-小太阳(虚数)-X-X-support
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-Egg'
        names = master.members = ['阿福', '小贝', '小太阳']
        master.set_card_weight(dict(zip(names, [1.01, 2, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.a', 'img/battles/free/a-egg/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (2, 1), (1, 5), (3, 4))
            master.set_cards(names[1], (2, 7), (1, 2), (1, 4), (1, 1))
            master.set_cards(names[2], (3, 8), (1, 3), (3, 3), (2, 3))

            def _handler():  # noqas
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=False, match_ce=True, match_ce_max=True, match_skills=False,
                              switch_classes=(5, 0), friend_only=False)

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(1, 3)
            # master.svt_skill(1, 1)
        master.set_card_weight(dict(zip(names, [2, 1, 1.01])))
        master.auto_attack(nps=6, mode='alter')
        master.xjbd(T.wave2a, LOC.loc_wave)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(2, 2)
            master.svt_skill(2, 1)
        master.set_card_weight(dict(zip(names, [1, 2, 1.01])))
        master.auto_attack(nps=7, mode='dmg')
        master.xjbd(T.wave3a, LOC.loc_wave)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(3, 3)
            master.svt_skill(3, 2)
            master.svt_skill(1, 2)
            master.svt_skill(1, 1)
            master.master_skill(2, 3)
        master.set_card_weight(dict(zip(names, [1.5, 1, 2])))
        master.auto_attack(nps=8, mode='alter')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return

    @with_goto
    def a_egg2(self, pre_process=False):
        """
        陈宫(醉贞)-孔明support-阿周那(空骑)-小贝(熔岩巧克力)-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-Egg'
        names = master.members = ['陈宫', '孔明', '阿周那', '小贝']
        master.set_card_weight(dict(zip(names, [1.01, 0, 2, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.a', 'img/battles/free/a-egg2/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (6, 2), (1, 3), (6, 4))
            master.set_cards(names[2], (2, 7), (1, 2), (2, 3), (3, 5))
            master.set_cards(names[3], (3, 8), (2, 1), (2, 4), (3, 2))
            master.set_cards_from_json('孔明', 'img/cards/android/cards-android.json')

            def _handler():  # noqas
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                              switch_classes=(5, 0), friend_only=False)

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(2, 2)
            master.svt_skill(2, 3)
            master.svt_skill(2, 1, 1)
        master.auto_attack(nps=6)
        # master.xjbd(T.wave2a, LOC.loc_wave)
        master.members = ['陈宫', '小贝', '阿周那']

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7, clicking=LOC.safe_area)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(1, 2)
            master.svt_skill(2, 2)
            master.master_skill(2, 2)
        master.auto_attack(nps=7, mode='alter')
        master.xjbd(T.wave3a, LOC.loc_wave)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 1, 1)
            master.svt_skill(1, 3, 3)
            master.svt_skill(2, 1)
            master.svt_skill(3, 1)
            master.svt_skill(3, 2)
            master.master_skill(1)
        master.auto_attack(nps=8, mode='dmg')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return

    @with_goto
    def a_devar(self, pre_process=False):
        """
        黑C(虚数)-小贝(空骑)-孔明support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-devar'
        names = master.members = ['黑C', '小贝', '孔明']
        master.set_card_weight(dict(zip(names, [1, 2, 1.01])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.a', 'img/battles/free/a-devar/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (3, 1), (1, 2), (3, 4))
            master.set_cards(names[1], (3, 7), (1, 3), (2, 5), (3, 2))
            master.set_cards_from_json('孔明', 'img/cards/android/cards-android.json')

            def _handler():  # noqas
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                              switch_classes=(5, 0), friend_only=False)

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.master_skill(2, 1)
            master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7, clicking=LOC.safe_area)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 1, 1)
            master.svt_skill(1, 2)
            master.master_skill(1)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 1)
            master.svt_skill(2, 2)
        master.auto_attack(nps=7, mode='dmg')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return


# noinspection DuplicatedCode
class JFree(BattleBase):
    @with_goto
    def j_charlotte(self, pre_process=False):
        """
        lily(80NP)-黑C(80NP)-孔明support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'J-Charlotte'
        names = master.members = ['Lily', '黑C', '孔明']
        master.set_card_weight(dict(zip(names, [3, 1, 1.1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/battles/.j', 'img/battles/free/j-charlotte/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (1, 3), (2, 1), (2, 4))
            master.set_cards(names[1], (1, 7), (2, 5), (1, 1), (2, 3))
            master.set_cards_from_json(names[2], 'img/cards/jp/cards-jp.json', '孔明')

            def _handler():
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None if True else _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                              switch_classes=(5, 0), friend_only=False)

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(2, 1)
            master.auto_attack(nps=7, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 1, 2)
            master.svt_skill(2, 2)
            master.master_skill(1, 2)
            master.auto_attack(nps=7)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 2)
            master.svt_skill(1, 1)
            master.auto_attack(nps=6, mode='alter')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return

    @with_goto
    def j_charlotte2(self, pre_process=False):
        """
        宇宙凛(80NP)-伊阿宋(80NP)-孔明support-X-X-X 增伤服
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'J-Charlotte'
        names = master.members = ['宇宙凛', '伊阿宋', '孔明']
        master.set_card_weight(dict(zip(names, [3, 2, 1.1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/battles/.j', 'img/battles/free/j-charlotte2/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (2, 3), (1, 2), (2, 5))
            master.set_cards(names[1], (1, 7), (3, 2), (1, 4), (1, 3))
            master.set_cards_from_json(names[2], 'img/cards/jp/cards-jp.json', '孔明')

            def _handler():
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None if True else _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                              switch_classes=(5, 0), friend_only=False)

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(2, 3)
        master.auto_attack(nps=7, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(3, 1, 1)
            master.svt_skill(1, 3)
            master.svt_skill(1, 2, 1)
            master.master_skill_full(T.cloth11, 2, 1)
        master.auto_attack(nps=6, mode='dmg')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return

    @with_goto
    def j_riverside(self, pre_process=False):
        """
        A(>10NP to all)-陈宫(80NP)-弓凛-孔明support-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'J-Riverside'
        names = master.members = ['海妈', '陈宫', '弓凛', '孔明', 'CBA']
        master.set_card_weight(dict(zip(names, [0, 1, 3, 1.09, 1.09])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/battles/.j', 'img/battles/free/j-riverside/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))

            # --------------  name       NP    Quick    Arts   Buster -----------
            # master.set_cards(names[0], (), (), (), ())
            master.set_cards(names[1], (4, 7), (2, 1), (1, 2), (3, 1))
            master.set_cards(names[2], (1, 8), (2, 5), (1, 5), (1, 1))
            master.set_cards_from_json('孔明', 'img/cards/jp/cards-jp.json')
            master.set_cards_from_json('CBA', 'img/cards/jp/cards-jp.json')

            def _handler():
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None if True else _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        support = master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                                        switch_classes=(5, 0), friend_only=False,
                                        images=[master.T.support, master.T.support2])
        # support 0-孔明, 1-CBA
        if support == 0:
            names.pop(-1)
        else:
            names.pop(-2)

        label.h  # noqas

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(1, 1)
            # master.auto_attack(nps=7, mode='alter')
            master.attack([7, 1, 2])
        master.members = [names[3], names[1], names[2]]  # A sacrifice

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7, clicking=LOC.safe_area)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 1)
            master.svt_skill(3, 3)
            master.auto_attack(nps=8, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        if support == 0:
            with master.set_waves(T.wave3a, T.wave3b):
                master.svt_skill(1, 2)
                master.svt_skill(1, 3)
                master.svt_skill(1, 1, 3)
        else:
            with master.set_waves(T.wave3a2, T.wave3b2):
                master.svt_skill(1, 2)
                master.svt_skill(1, 3, 3)

        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(3, 2)
            master.svt_skill(2, 3, 3)
            # master.master_skill(2, 3)
            master.auto_attack(nps=8, mode='dmg')

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def j_nemesis(self, pre_process=False):
        """
        小王子(宝石)-小灰(黑杯)-孔明support-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'J-Nemesis'
        names = master.members = ['小王子', '小灰', '孔明', ]
        master.set_card_weight(dict(zip(names, [2, 3, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/battles/.j', 'img/battles/free/j-nemesis/'])

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (3, 3), (1, 5), (1, 2))
            master.set_cards(names[1], (3, 7), (1, 4), (2, 1), (3, 2))
            master.set_cards_from_json('孔明', 'img/cards/jp/cards-jp.json')

            def _handler():
                # mainly for jp, re-login handler at 3am(UTC+8)
                wait_targets(T.get('login_page'), LOC.menu_button)
                wait_targets(T.get('login1'), (1000, 480, 1350, 600), at=0, clicking=LOC.safe_area)
                # ....
                wait_targets(T.quest, LOC.quest)

            config.battle.login_handler = None if True else _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_ce=True, match_ce_max=True, match_skills=True,
                              switch_classes=(5, 0), friend_only=False,
                              images=[master.T.support])

        label.h  # noqas

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 1, 1)
            master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 1)
            master.svt_skill(2, 2)
            master.svt_skill(2, 3)
        master.auto_attack(nps=7, mode='alter')

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return


# noinspection DuplicatedCode
class SFree(BattleBase):
    pass


# noinspection DuplicatedCode
class Battle(JFree, AFree, SFree):
    pass
