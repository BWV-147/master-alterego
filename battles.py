"""Store battle_func for different battles

- wrap @with_goto to enable goto and label statement.
- for card template of common used servants who have 3+dress sets of models(e.g. Kongming/CBA/Merlin),
  save all models' cards info(json) and templates into the same folder(e.g. `img/battles/cards/jp/`).
  Then use `master.set_cards_from_json()` to load it.
- ensure the same app version(current & saved screenshots): e.g. command card's text might differ.
"""
from modules.battle_base import *

try:
    from battles_local import BattleLocal
except ImportError:
    class BattleLocal(BattleBase):
        pass


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
            T.read_templates(['img/share/android', 'img/battles/free/a-charlotte/'])

            # LOC.relocate((0, 0, 1920, 1080))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards_from_json('黑C', 'android')
            master.set_cards_from_json('高文', 'android')
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
        master.auto_attack(nps=6, mode=AttackMode.alter)
        master.xjbd(T.wave2a, LOC.loc_wave, mode=AttackMode.alter)

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
        master.auto_attack(nps=6, mode=AttackMode.damage)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 3)
        master.auto_attack(nps=7, mode=AttackMode.alter)

        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.alter, allow_unknown=True)
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

            # LOC.relocate((0, 0, 1920, 1080))
            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards_from_json('黑C', 'android')
            master.set_cards_from_json('小贝', 'android')
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
            master.svt_skill(1, 1)
            master.svt_skill(3, 1, 1)
            master.svt_skill(2, 1)
        master.auto_attack(nps=6, mode=AttackMode.alter)
        master.xjbd(T.wave2a, LOC.loc_wave, mode=AttackMode.alter)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(1, 2)
            master.master_skill(1, 1)
        master.auto_attack(nps=6, mode=AttackMode.alter)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 2)
        master.auto_attack(nps=7, mode=AttackMode.damage)

        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.alter, allow_unknown=True)
        return


# noinspection DuplicatedCode
class JFree(BattleBase):
    @with_goto
    def j_charlotte(self, pre_process=False):
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
            T.read_templates(['img/share/jp', 'img/battles/free/j-charlotte/'])

            # LOC.relocate((0, 0, 1920, 1080))

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards_from_json('紫式部', 'jp')
            master.set_cards_from_json('Lily', 'jp')
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
        wait_targets(T.wave1a, LOC.master_skill, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 1)
            master.svt_skill(3, 2, 1)
            master.svt_skill(3, 3, 1)
            master.master_skill(3, 1)
        master.auto_attack(nps=6, mode=AttackMode.alter)

        # wave 2
        wait_targets(T.wave2a, LOC.master_skill, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(1, 2)
            master.master_skill(1, 1)
        master.auto_attack(nps=6, mode=AttackMode.damage)

        # wave 3
        wait_targets(T.wave3a, LOC.master_skill, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 1)
            master.svt_skill(2, 2)
        master.auto_attack(nps=7, mode=AttackMode.alter)

        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.alter, allow_unknown=True)
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
        names = master.members = ['小王子', '芬恩', '术呆']
        master.set_card_weight(dict(zip(names, [2, 3, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/share/jp', 'img/battles/free/j-meadow/'])

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards_from_json('小王子', 'jp')
            master.set_cards_from_json('芬恩', 'jp')
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
        master.auto_attack(nps=6, mode=AttackMode.alter)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 2, 1)
            master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode=AttackMode.alter)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 2)
            master.svt_skill(2, 3)
            master.svt_skill(3, 3, 2)
            master.master_skill(1, 2)
            master.master_skill(3, 2)
        master.auto_attack(nps=7, mode=AttackMode.alter)

        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.damage, allow_unknown=True)
        return


# noinspection DuplicatedCode
class SFree(BattleBase):
    @with_goto
    def s_charlotte(self, pre_process=False):
        """
        Saber(50NP)-黑C(80NP)-孔明support-X-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'S-Charlotte'
        names = master.members = ['Saber', '黑C', '孔明']
        master.set_card_weight(dict(zip(names, [2, 1, 1.01])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/share/6s', 'img/battles/free/s-charlotte/'])

            LOC.relocate((0, 0, 1334, 750))

            # --------------  name       NP    Quick    Arts   Buster -----------
            master.set_cards_from_json('Saber', '6s')
            master.set_cards_from_json('黑C', '6s')
            master.set_cards_from_json('孔明', '6s')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas
        label.h  # noqas

        wait_targets(T.support, LOC.support_refresh)
        master.choose_support(match_svt=True, match_skills=False, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

        # wave 1
        wait_targets(T.wave1a, LOC.loc_wave, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 2)
            master.svt_skill(3, 3)
            master.svt_skill(2, 1)
            master.svt_skill(1, 1)
        master.auto_attack(nps=7, mode=AttackMode.alter)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(2, 2)
            master.svt_skill(3, 1, 2)
            master.master_skill(1, 2)
        master.auto_attack(nps=7, mode=AttackMode.damage)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(1, 3)
            master.svt_skill(1, 2)
        master.auto_attack(nps=6, mode=AttackMode.alter)

        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.alter, allow_unknown=True)
        return


# noinspection DuplicatedCode
class Battle(JFree, AFree, SFree, BattleLocal):
    pass
