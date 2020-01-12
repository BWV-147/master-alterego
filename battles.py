"""Store battle_func for different battles"""
from util.battle import *


# noinspection PyPep8Naming,DuplicatedCode
class Battle(BattleBase):
    @with_goto
    def a_rider(self, pre_process=False):
        """
        阵容: 杀师匠-大龙娘-羽蛇神-X-X
        xjb打，给大龙娘凑宝具
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'A-Rider'
        T.read_templates('img/a-rider')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['杀师匠', '大龙娘', '羽蛇神', '羽蛇神R'])
        master.show_svt_name = True
        master.set_card_weights([1.0, 1.1, 0.81, 0.80])
        # ---- NP     Quick   Arts   Buster ----
        master.set_card_templates([
            [(1, 0), (2, 1), (1, 2), (3, 4)],
            [(4, 7), (1, 4), (2, 4), (1, 3)],
            [(1, 0), (2, 3), (1, 1), (1, 5)],
            [(1, 0), (5, 3), (5, 4), (5, 2)]
        ])
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
        wait_which_target(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support_drag(match_svt=False, match_ce=False, match_ce_max=False, match_skills=False,
                                       switch_classes=(6, 9))
        else:
            logger.debug('please choose support manually in 60s!')

        cur_turn = 1
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a)
        master.svt_skill(2, 1)
        master.svt_skill(3, 1)
        cur_turn += master.xjbd(T.wave2a, [LOC.wave_num, LOC.master_skill], 'alter')

        # wave 2
        wait_targets(T.wave2a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 2...')
        master.set_waves(T.wave2a)
        click(LOC.enemies[0])
        cur_turn += master.xjbd(T.wave3a, [LOC.wave_num, LOC.master_skill], mode='alter')

        # noinspection PyStatementEffect
        label.h
        # wave 3
        wait_targets(T.wave3a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 3...')
        master.set_waves(T.wave3a)
        master.svt_skill(2, 3, enemy=1)
        click(LOC.enemies[-1])
        if cur_turn < 8:
            master.xjbd(T.kizuna, LOC.kizuna, turns=8 - cur_turn)
        wait_which_target(T.wave3a, LOC.master_skill)
        master.svt_skill(3, 1)
        master.svt_skill(2, 1, enemy=1)
        master.svt_skill(2, 2)
        master.master_skill(2, 2)
        master.xjbd(T.kizuna, LOC.kizuna, turns=1, nps=7, allow_unknown=True)
        master.xjbd(T.kizuna, LOC.kizuna, allow_unknown=True, mode='alter')
        return
