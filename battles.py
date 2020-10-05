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
            master.set_cards_from_json('孔明', 'img/battles/cards/android/cards-android.json')

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

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=False, match_skills=False, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

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
            master.set_cards_from_json('孔明', 'img/battles/cards/android/cards-android.json')

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
            master.svt_skill(2, 2)
            master.svt_skill(2, 3)
            master.svt_skill(2, 1, 1)
        master.auto_attack(nps=6)
        # master.xjbd(T.wave2a, LOC.loc_wave)
        # master.members = ['陈宫', '小贝', '阿周那']
        master.svt_die(2)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
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
            master.set_cards_from_json('孔明', 'img/battles/cards/android/cards-android.json')

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
            master.set_cards_from_json('孔明', 'img/battles/cards/jp/cards-jp.json')

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
            master.set_cards_from_json('孔明', 'img/battles/cards/jp/cards-jp.json')

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
            master.set_cards_from_json('孔明', 'img/battles/cards/jp/cards-jp.json')
            master.set_cards_from_json('CBA', 'img/battles/cards/jp/cards-jp.json')

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
            master.set_cards_from_json('孔明', 'img/battles/cards/jp/cards-jp.json')

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
    @with_goto
    def s2_ticket(self, pre_process=False):
        """
        大英雄-弓凛-CBA-孔明support-莎翁-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'S2-ticket'
        names = master.members = ['大英雄', '弓凛', 'CBA', '孔明', '莎翁']
        master.set_card_weight(dict(zip(names, [3, 3.09, 1.01, 1.01, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.s', 'img/battles/s2-ticket/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (3, 6), (1, 3), (3, 1), (1, 4))
            master.set_cards(names[1], (4, 7), (1, 1), (1, 5), (2, 3))
            master.set_cards(names[4], (1, 0), (2, 2), (2, 4), (2, 5))
            master.set_cards_from_json('孔明', 'img/battles/cards/iOS/cards-ios.json')
            master.set_cards_from_json('CBA', 'img/battles/cards/iOS/cards-ios.json')

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(9,))

        label.h  # noqas
        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        time.sleep(5)
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 3, 1)
            master.svt_skill(3, 2)
            master.svt_skill(3, 1, 1)
        master.xjbd(T.wave2a, LOC.loc_wave, 'alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.master_skill_full(T.wave1a, 3, order_change=(3, 5))
            master.svt_skill(3, 3, 1)
            master.svt_skill(1, 3)
            master.svt_skill(2, 1)
            master.svt_skill(2, 3)
        master.auto_attack(nps=6, mode='alter')
        # master.members = ['孔明', '弓凛', '莎翁']
        master.svt_die(1)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 2)
            master.svt_skill(1, 3)
            master.svt_skill(1, 1, 2)
            master.svt_skill(2, 2)
            master.svt_skill(3, 1)
            master.master_skill(1)
        master.auto_attack(nps=7, mode='alter')
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return


# noinspection DuplicatedCode
class Battle(JFree, AFree, SFree):
    @with_goto
    def shi1(self, pre_process=False):
        """
        狂兰50NP-CBA-孔明-孔明-X-X-support
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'Shi1'
        names = master.members = ['狂兰', 'CBA', '孔明', '孔明']
        master.set_card_weight(dict(zip(names, [3, 2.01, 2, 2])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.s', 'img/battles/shi1/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (1, 6), (1, 3), (3, 1), (2, 2))
            master.set_cards(names[1], (1, 0), (2, 3), (2, 4), (1, 1))
            master.set_cards_from_json('CBA', 'img/battles/cards/ios/cards-ios.json')
            master.set_cards_from_json('孔明', 'img/battles/cards/ios/cards-ios.json')

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        support = master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                                        friend_only=False, switch_classes=(9,), images=[T.support, T.support_cba])
        if support == 0:
            logger.info('chosen support: 孔明')
        else:
            logger.info('chosen support: CBA')
            master.members = ['狂兰', 'CBA', 'CBA', '孔明']
            T.read_templates('img/battles/shi1-cba/', True)

        label.h  # noqas
        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            if support == 0:
                master.svt_skill(3, 2)
                master.svt_skill(3, 3)
                master.svt_skill(3, 1, 1)
            else:
                master.svt_skill(3, 1, 1)
                master.svt_skill(3, 3, 1)
            master.svt_skill(2, 1, 1)
            master.svt_skill(1, 3)
            master.master_skill(3, order_change=(3, 4), order_change_img=T.order_change)
        master.auto_attack(nps=6, mode='alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 1, 1)
        master.auto_attack(nps=6, mode='alter')

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(2, 3, 1)
            master.svt_skill(2, 2)
        master.auto_attack(nps=6, mode='dmg')

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def a2_ticket(self, pre_process=False):
        """
        阿拉什-狂娜-孔明-孔明support-大王-X 换人
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A2-ticket'
        names = master.members = ['阿拉什', '狂娜', '孔明', '孔明', '大王']
        master.set_card_weight(dict(zip(names, [2.01, 2.02, 1, 1, 2])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/battles/.a', 'img/battles/a2-ticket/'])

            # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards(names[0], (3, 6), (2, 3), (3, 1), (1, 4))
            master.set_cards(names[1], (4, 7), (2, 5), (1, 3), (3, 3))
            master.set_cards(names[4], (0, 0), (1, 2), (1, 1), (2, 4))
            master.set_cards_from_json('孔明', 'img/battles/cards/android/cards-android.json')

            config.battle.login_handler = None  # _handler
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(9,))

        label.h  # noqas
        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3, enemy=3)
            master.svt_skill(3, 1, 1)
            master.master_skill(3, order_change=(3, 5), order_change_img=T.order_change)
        master.xjbd(T.wave2a, LOC.loc_wave, 'alter')

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 1, 1)
            master.svt_skill(1, 3)
        master.set_card_weight(dict(zip(['阿拉什', '狂娜', '孔明', '大王'], [0, 2.02, 1, 2])))
        master.auto_attack(nps=6, mode='dmg')
        # master.members = ['孔明', '狂娜', '大王']
        master.svt_die(1)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 1, 2)
            master.svt_skill(1, 2)
            master.svt_skill(1, 3)
            master.svt_skill(2, 1)
            master.svt_skill(2, 2)
            # master.svt_skill(2, 3)
            master.svt_skill(3, 2, 2)
            master.master_skill(2)
            master.master_skill(1, enemy=3)
        master.auto_attack(nps=7, mode='alter')

        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return
