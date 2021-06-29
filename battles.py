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
    # write default file content
    with open('battles_local.py', 'w', encoding='utf8') as fd:
        fd.write('from modules.battle_base import *\n\n\n'
                 '# noinspection DuplicatedCode\n'
                 'class BattleLocal(BattleBase):\n'
                 '    pass\n')
        print('generated empty battles_local.py')


    class BattleLocal(BattleBase):
        pass


# noinspection DuplicatedCode
class AFree(BattleBase):
    @with_goto
    def a_charlotte(self, pre_process=False):
        """
        尼托(醉贞)-黑呆(空骑)-孔明support-X-X-X 热带夏日
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'A-charlotte'
        names = master.members = ['尼托', '黑呆', '孔明']
        master.set_card_weight(dict(zip(names, [1.01, 2, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name} ...')
            T.read_templates(['img/share/android', 'img/battles/free/a-charlotte/'])
            for name in names:
                master.set_cards_from_json(name, 'android')

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
            # master.svt_skill(1, 1)
        master.auto_attack(nps=6, mode=AttackMode.alter)

        # wave 2
        wait_targets(T.wave2a, LOC.loc_wave, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            # master.svt_skill(1, 1)
            master.svt_skill(1, 2)
            master.svt_skill(2, 3)
            master.master_skill(1, 1)
        master.auto_attack(nps=6, mode=AttackMode.damage)

        # wave 3
        wait_targets(T.wave3a, LOC.loc_wave, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            master.svt_skill(2, 2)
            master.master_skill(3, 2)
            master.svt_skill(2, 1)
        master.auto_attack(nps=7, mode=AttackMode.alter)

        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.alter, allow_unknown=True)
        return


# noinspection DuplicatedCode
class JFree(BattleBase):
    @with_goto
    def j_charlotte(self, pre_process=False):
        """
        村正(75NP)-水阿比(50NP)-术呆support-X-X-X 04服
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        master.quest_name = 'J-Charlotte'
        names = master.members = ['村正', '水阿比', '术呆']
        master.set_card_weight(dict(zip(names, [2, 1, 1])))

        # pre-processing: e.g. set templates, only once
        if pre_process:
            logger.debug(f'pre-process for {master.quest_name}...')
            T.read_templates(['img/share/jp', 'img/battles/free/j-charlotte/'])
            for name in names:
                master.set_cards_from_json(name, 'jp')

            config.battle.login_handler = None
            return

        # battle part
        if config.battle.jump_battle:
            config.battle.jump_battle = False
            logger.warning('goto label.h')
            goto.h  # noqas
        label.h  # noqas

        print('hahah')
        wait_targets(T.support, LOC.support_refresh)
        print('hahah22')
        master.choose_support(match_svt=True, match_skills=True, match_ce=True, match_ce_max=True,
                              friend_only=False, switch_classes=(5, 0))

        # wave 1
        wait_targets(T.wave1a, LOC.master_skill, 0.7)
        logger.debug(f'Quest {master.quest_name} started...')
        logger.debug('wave 1...')
        with master.set_waves(T.wave1a, T.wave1b):
            master.svt_skill(3, 1)
            master.svt_skill(2, 3)
        master.auto_attack(nps=7, mode=AttackMode.alter)

        # wave 2
        wait_targets(T.wave2a, LOC.master_skill, 0.7)
        logger.debug('wave 2...')
        with master.set_waves(T.wave2a, T.wave2b):
            master.svt_skill(3, 3, 1)
            master.master_skill(3, 1)
        master.auto_attack(nps=6, mode=AttackMode.alter)

        # wave 3
        wait_targets(T.wave3a, LOC.master_skill, 0.7)
        logger.debug('wave 3...')
        with master.set_waves(T.wave3a, T.wave3b):
            # master.svt_skill(2, 1)
            master.svt_skill(3, 2, 1)
            master.svt_skill(1, 3)
            master.svt_skill(1, 1)
            master.svt_skill(2, 2)  # optional
            master.master_skill(1, 1)
        master.auto_attack(nps=6, mode=AttackMode.alter)

        master.xjbd(T.kizuna, LOC.kizuna, mode=AttackMode.alter, allow_unknown=True)
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
            for name in names:
                master.set_cards_from_json(name, '6s')
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
