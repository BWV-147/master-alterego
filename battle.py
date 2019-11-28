"""Store battle_func for different battles"""
from util.master import *


# noinspection PyPep8Naming,DuplicatedCode
class Battle(BattleBase):
    @with_goto
    def christmas_final(self, support=True):
        """
        阵容: lilith-艾蕾-梅莉-support-X-X
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'christmas_final'
        master.svt_names = ['lilith', '艾蕾', '梅莉']
        master.set_card_weights([2, 3, 1])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (3, 3), (2, 3), (1, 2)],
            [(3, 7), (1, 4), (1, 1), (2, 4)],
            [(1, 0), (2, 1), (2, 2), (1, 3)],
        ])
        if CONFIG.jump_battle:
            CONFIG.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        if support:
            master.choose_support(match_svt=False, match_ce=True, match_ce_max=False, switch_classes=(5,))
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_which_target(T.wave1a, LOC.enemies[0])
        logger.debug(f'Quest {master.quest_name} start...')
        wait_which_target(T.wave1a, LOC.master_skill)
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 1)
        master.svt_skill(2, 3)
        master.svt_skill(1, 1)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_which_target(T.wave2a, LOC.enemies[0])
        wait_which_target(T.wave2a, LOC.master_skill)
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(1, 3)
        master.master_skill(T.wave2a, 2, 1)
        # noinspection PyStatementEffect
        label.h
        click(LOC.enemies[1])
        chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        # master.attack([6, 1, 2])
        # master.auto_attack(nps=7)

        # wave 3
        wait_which_target(T.wave3a, LOC.enemies[1])
        wait_which_target(T.wave3a, LOC.master_skill)
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(2, 2)
        master.svt_skill(3, 3, 2)
        # master.attack([6, 1, 2])
        master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    # unused
    @with_goto
    def no_battle(self, support=True):
        """
        template, no battle.
        """
        master = self.master
        T = self.master.T
        LOC = self.master.LOC
        if not master.quest_name:
            master.quest_name = 'no battle'
        master.svt_names = ['X', 'Y', 'Z']
        master.set_card_weights([2, 3, 1])
        # ----  NP     Quick    Arts   Buster ----
        # master.set_card_templates([
        #     [(1, 6), (3, 3), (2, 3), (1, 2)],
        #     [(3, 7), (1, 4), (1, 1), (2, 4)],
        #     [(1, 0), (2, 1), (2, 2), (1, 3)],
        # ])
        if CONFIG.jump_battle:
            CONFIG.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        # noinspection PyStatementEffect
        label.h
        wait_which_target(T.support, LOC.support_refresh)
        if support:
            master.choose_support(match_svt=True, match_ce=False, match_ce_max=False, switch_classes=(5,))
        else:
            logger.debug('please choose support manually!')
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
        click(LOC.enemies[1])
        chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        # master.attack([6, 1, 2])
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
