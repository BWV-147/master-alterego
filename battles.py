"""Store battle_func for different battles

- wrap @with_goto to enable goto and label statement.
- for card template of common used servants who have 3+dress sets of models(e.g. Kongming/CBA/Merlin),
  save all models' cards info(json) and templates into the same folder(e.g. `img/battles/cards/jp/`).
  Then use `master.set_cards_from_json()` to load it.
- ensure the same app version(current & saved screenshots): e.g. command card's text might differ.
"""
from modules.battle_base import *


# noinspection DuplicatedCode
class AFree(BattleBase):
    @with_goto
    def a_charlotte(self, pre_process=False):
        """
        黑C(虚数)-高文(虚数)-孔明support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-charlotte'
        names = master.members = ['黑C', '高文', '孔明']
        master.set_card_weight(dict(zip(names, [2, 1, 2.01])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.a', 'img/battles/free/a-charlotte/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (1, 4), (1, 3), (1, 1))
            master.set_cards(names[1], (4, 7), (2, 3), (1, 5), (2, 2))
            master.set_cards_from_json('孔明', 'android')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 1, 1)
            master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode='alter')
        master.xjbd(T.wave2a, LOC.loc_wave, 'alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        master.set_card_weight(dict(zip(names, [2, 3, 2.01])))
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(1, 2)
            master.svt_skill(2, 2)
            master.svt_skill(2, 1)
            master.master_skill(1, 1)
        master.auto_attack(nps=6, mode='dmg')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 3)
        master.auto_attack(nps=7, mode='alter')

        master.xjbd(T.kizuna, LOC.kizuna, mode='alter', allow_unknown=True)
        return

    @with_goto
    def a_devar2(self, pre_process=False):
        """
        黑C(虚数)-小贝(空骑)-孔明support-X-X-X 10mp
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
            master.set_cards_from_json('孔明', 'android')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

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
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
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
            master.set_cards_from_json('孔明', 'android')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        master.svt_skill_full(T.wave1a, T.wave1b, 1, 1)
        master.svt_skill_full(T.wave2a, T.wave2b, 3, 1, 1)
        master.svt_skill_full(T.wave3a, T.wave3b, 2, 1)

        master.auto_attack(nps=6, mode='alter')
        master.xjbd(T.wave2a, LOC.loc_wave, 'alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 2)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 3)
        master.svt_skill_full(T.wave2a, T.wave2b, 1, 2)
        master.master_skill_full(T.wave2a, 1, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
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
            master.set_cards_from_json('孔明', 'jp')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

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
            master.set_cards_from_json('孔明', 'jp')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

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
    def j_charlotte3(self, pre_process=False):
        """
        紫式部(50NP)-lily(75NP)-术呆support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'J-Charlotte'
        names = master.members = ['紫式部', 'Lily', '术呆']
        master.set_card_weight(dict(zip(names, [1.1, 2, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/battles/.j', 'img/battles/free/j-charlotte3/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (2, 1), (1, 2), (3, 3))
            master.set_cards(names[1], (1, 7), (2, 4), (1, 1), (1, 3))
            master.set_cards_from_json('术呆', 'jp')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 1)
            master.svt_skill(3, 2, 1)
            master.svt_skill(3, 3, 1)
            master.master_skill(3, 1)
            master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(1, 2)
            master.master_skill(1, 1)
            master.auto_attack(nps=6, mode='dmg')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 1)
            master.svt_skill(2, 2)
            master.auto_attack(nps=7, mode='dmg')

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
            master.set_cards_from_json('孔明', 'jp')
            master.set_cards_from_json('CBA', 'jp')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        support = master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                                        friend_only=False, switch_classes=(5, 0),
                                        images=[T.support, T.support2])
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
        # master.members = [names[3], names[1], names[2]]  # A sacrifice
        master.svt_die(1)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
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
            master.set_cards_from_json('孔明', 'jp')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0),
                              images=[T.support])

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

    @with_goto
    def j_meadow(self, pre_process=False):
        """
        小王子(满破虚数)-芬恩(黑杯)-术呆-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'J-Meadow'
        names = master.members = ['小王子', '芬恩', '术呆', ]
        master.set_card_weight(dict(zip(names, [2, 3, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/battles/.j', 'img/battles/free/j-meadow/'])

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (2, 1), (1, 5), (1, 3))
            master.set_cards(names[1], (3, 7), (2, 5), (1, 1), (2, 3))
            master.set_cards_from_json('术呆', 'jp')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0),
                              images=[T.support])

        label.h  # noqas

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 1)
            master.svt_skill(2, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 2, 1)
            master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 2)
            master.svt_skill(2, 3)
            master.svt_skill(3, 3, 2)
            master.master_skill(1, 2)
            master.master_skill(3, 2)
        master.auto_attack(nps=7, mode='alter')

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return


# noinspection DuplicatedCode
class SFree(BattleBase):
    pass


# noinspection DuplicatedCode
class Battle(JFree, AFree, SFree):
    @with_goto
    def a3_ticket(self, pre_process=False):
        """
        贞德-花嫁-豆爸-花嫁support-X-X 换人
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A3-Ticket'
        names = master.members = ['贞德', '花嫁', '豆爸', '花嫁']
        master.set_card_weight(dict(zip(names, [3, 2, 1, 2])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.a', 'img/battles/a3-ticket/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (3, 2), (1, 1), (1, 2))
            master.set_cards_from_json('花嫁', 'android')

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(1,))

        label.h  # noqas
        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3, 1)
            master.master_skill(3, order_change=(3, 4), order_change_img=T.order_change)
        with master.set_waves(T.wave1c, T.wave1d):
            master.svt_skill(2, 1, 1)
            master.svt_skill(2, 2, 1)
            master.svt_skill(3, 1, 1)
            master.svt_skill(3, 2, 1)
            master.svt_skill(1, 1)
            master.svt_skill(1, 2)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(1, 3)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.master_skill(1)
            master.master_skill(2)
        master.auto_attack(nps=6, mode='dmg', buster_first=True)

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def s3_ticket(self, pre_process=False):
        """
        贞德-花嫁-花嫁support-C闪-X-X 换人
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'S3-Ticket'
        names = master.members = ['贞德', '花嫁', '花嫁S', 'C闪']
        master.set_card_weight(dict(zip(names, [3, 2.01, 2.01, 2])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.s', 'img/battles/s3-ticket/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (3, 2), (1, 1), (1, 2))
            master.set_cards(names[1], (1, 6), (3, 2), (1, 1), (1, 2))
            master.set_cards(names[2], (1, 6), (3, 2), (1, 1), (1, 2))

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(1,))

        label.h  # noqas
        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 1, 1)
            master.svt_skill(3, 2, 1)
            master.master_skill(3, order_change=(3, 4))
        with master.set_waves(T.wave1c, T.wave1d):
            master.svt_skill(2, 1, 1)
            master.svt_skill(2, 2, 1)
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(1, 1)
            master.svt_skill(1, 2)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(1, 3)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.master_skill(1)
            master.master_skill(2)
        master.auto_attack(nps=6, mode='dmg', buster_first=True)

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return
