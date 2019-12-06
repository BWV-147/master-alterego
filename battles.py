"""Store battle_func for different battles"""
from util.battle import *


# noinspection PyPep8Naming,DuplicatedCode
class Battle(BattleBase):
    @with_goto
    def xmas_kong(self, pre_process=False):
        """
        阵容: 狂兰(50NP)-CBA-CBA(s)-孔明-X-X
        CBA(s) T2换下去, 魔力逆流*T1*开
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'Xmas-kong'
        T.read_templates('img/xmas-kong')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['狂兰', 'CBA', 'CBA(s)', '孔明'])
        master.set_card_weights([3, 1, 1])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (2, 4), (3, 4), (2, 3)],
            [(1, 0), (3, 3), (1, 3), (2, 1)],
            [(1, 0), (3, 1), (1, 2), (1, 1)],
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
        # label.h
        wait_which_target(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support_drag(match_svt=True, match_ce=False, match_ce_max=False, match_skills=True,
                                       switch_classes=(5, 0))
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 3, 1)
        master.svt_skill(3, 1, 1)
        master.svt_skill(2, 1, 1)
        master.svt_skill(1, 3)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_targets(T.wave2a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(3, 2)
        master.master_skill(3, order_change=(3, 4), order_change_img=T.order_change)
        master.set_waves(T.get('wave2c'), T.get('wave2d'))
        master.svt_skill(3, 1, 1)
        # chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        # master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        master.attack([6, 1, 2])
        # master.auto_attack(nps=7)

        # wave 3
        wait_targets(T.wave3a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.svt_skill(2, 2)
        master.svt_skill(2, 3, 1)
        master.master_skill(1)
        # noinspection PyStatementEffect
        label.h
        # master.master_skill(2)
        wait_which_target(T.wave3a, LOC.master_skill)
        click(LOC.enemies[1])
        chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def xmas_rescue(self, pre_process=False):
        """
        阵容: 尼托(80NP)-Saber(50NP)-小麻雀-support-X-X
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'Xmas-rescue'
        T.read_templates('img/xmas-rescue')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['尼托', 'Saber', '小麻雀'])
        master.set_card_weights([1, 3, 2])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (2, 3), (1, 1), (2, 2)],
            [(3, 7), (1, 3), (3, 2), (2, 1)],
            [(1, 0), (3, 4), (1, 2), (1, 5)],
        ])
        if pre_process:
            return

        # battle part
        if config.jump_battle:
            config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        # noinspection PyStatementEffect
        label.h
        wait_which_target(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support_drag(match_svt=False, match_ce=False, match_ce_max=False, match_skills=False,
                                       switch_classes=(-1,))
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 3)
        master.svt_skill(2, 1)
        master.svt_skill(1, 1)
        master.auto_attack(nps=6)

        # wave 2
        wait_targets(T.wave2a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(1, 2)
        master.auto_attack(nps=6)

        # wave 3
        wait_targets(T.wave3a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(3, 2)
        master.svt_skill(2, 3)
        master.svt_skill(2, 2)
        master.master_skill(2, 2)
        wait_which_target(T.wave3a, LOC.master_skill)
        master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def xmas_rescue2(self, pre_process=False):
        """
        bond: 615*1.25+50=818 point
        阵容: Alter(80NP)-Saber(50NP)-小麻雀-support-X-X
        T1: xjbd
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'Xmas-rescue2'
        T.read_templates('img/xmas-rescue2')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['Alter', 'Saber', '小麻雀'])
        master.set_card_weights([1, 1, 1])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (1, 5), (1, 2), (2, 3)],
            [(1, 7), (2, 1), (1, 3), (2, 5)],
            [(1, 0), (2, 2), (3, 2), (1, 1)],
        ])
        if pre_process:
            return

        # battle part
        if config.jump_battle:
            config.jump_battle = False
            logger.warning('goto label.h')
            # noinspection PyStatementEffect
            goto.h

        wait_which_target(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support_drag(match_svt=False, match_ce=True, match_ce_max=False, match_skills=False,
                                       switch_classes=(5,))
        else:
            logger.debug('please choose support manually!')
        # noinspection PyStatementEffect
        label.h
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 3)
        master.svt_skill(2, 3)
        master.svt_skill(1, 2)
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        click(LOC.skills[0][2])
        master.xjbd(T.wave2a, LOC.wave_num, mode='alter')

        # wave 2
        wait_targets(T.wave2a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.set_card_weights([2, 1, 3])
        # master.attack([6, 1, 2])
        master.auto_attack(nps=6)

        # wave 3
        wait_targets(T.wave3a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(2, 1)
        master.svt_skill(2, 2)
        # master.svt_skill(3, 2)
        master.master_skill(2, 2)
        wait_which_target(T.wave3a, LOC.master_skill)
        master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def xmas_kong2(self, pre_process=False):
        """
        阵容: 狂兰(50NP)-CBA-CBA(s)-孔明-X-X
        CBA(s) T2换下去, 魔力逆流*T2*开
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'Xmas-kong2'
        T.read_templates('img/xmas-kong2')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['狂兰', 'CBA', '孔明'])
        master.set_card_weights([3, 1, 1])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (2, 4), (3, 4), (2, 3)],
            [(1, 0), (3, 3), (1, 3), (2, 1)],
            [(1, 0), (3, 1), (1, 2), (1, 1)],
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
        # label.h
        wait_which_target(T.support, LOC.support_refresh)
        support = True
        if support:
            master.choose_support_drag(match_svt=True, match_ce=False, match_ce_max=False, match_skills=True,
                                       switch_classes=(5, 0))
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 3, 1)
        master.svt_skill(3, 1, 1)
        master.svt_skill(2, 1, 1)
        # master.svt_skill(1, 3)
        master.attack([6, 1, 2])
        # master.auto_attack(nps=6)

        # wave 2
        wait_targets(T.wave2a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(3, 2)
        master.svt_skill(1, 3)
        master.master_skill(3, order_change=(3, 4), order_change_img=T.order_change)
        master.set_waves(T.get('wave2c'), T.get('wave2d'))
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.svt_skill(2, 3, 1)
        # chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        # master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        master.attack([6, 1, 2])
        # master.auto_attack(nps=7)

        # wave 3
        wait_targets(T.wave3a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(3, 1, 1)
        master.svt_skill(2, 2)
        master.master_skill(1)
        # noinspection PyStatementEffect
        label.h
        # master.master_skill(2)
        wait_which_target(T.wave3a, LOC.master_skill)
        click(LOC.enemies[1])
        chosen_cards = master.auto_attack(nps=6, no_play_card=True)
        master.play_cards([chosen_cards[i] for i in (2, 0, 1)])
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def xmas_von(self, pre_process=False):
        """
        阵容: 狂兰(50NP)-豆爸(30NP)-CBA(s)-CBA-X-X
        T1: CBA(s)换下去, 魔力逆流，豆爸狂兰二连
        a) 高宝狂兰(>4?)可以不开豆爸宝具，把豆爸换下去，垫刀回满
        b) 50NP:
            醉贞: T3开CBA降防/换人服加攻
            轨迹: T2换人服加攻, T3 CBA降防防爆+Gandr
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'Xmas-von'
        T.read_templates('img/xmas-von')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['狂兰', '豆爸', 'CBA(s)', 'CBA'])
        master.show_svt_name = True
        master.set_card_weights([3, 1, 2, 2])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [(1, 6), (2, 2), (2, 3), (1, 2)],
            [(1, 7), (1, 4), (1, 3), (1, 5)],
            [],
            [(1, 0), (2, 1), (1, 1), (3, 2)],
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
            master.choose_support_drag(match_svt=True, match_ce=False, match_ce_max=False, match_skills=True,
                                       switch_classes=(5, 0))
        else:
            logger.debug('please choose support manually!')
        # noinspection PyStatementEffect
        label.h
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 3, 1)
        # master.svt_skill(3, 2)
        master.svt_skill(3, 1, 1)
        master.master_skill(3, order_change=(3, 4), order_change_img=T.order_change)
        master.set_waves(T.get('wave1c'), T.get('wave1d'))
        master.svt_skill(3, 1, 1)
        master.svt_skill(2, 1)
        # master.svt_skill(2, 2)
        master.svt_skill(2, 3, 1)
        master.svt_skill(1, 3)

        master.auto_attack(nps=[7, 6])

        # wave 2
        wait_targets(T.wave2a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.master_skill(1)
        master.auto_attack(nps=6)

        # wave 3
        wait_targets(T.wave3a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(3, 3, 1)
        master.svt_skill(3, 2)
        master.master_skill(2, enemy=2)
        master.auto_attack(nps=6)
        # master.auto_attack(nps=6)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return

    @with_goto
    def xmas_chen(self, pre_process=False):
        """
        阵容: CBA(s)-狂兰(轨迹)-陈宫(50NP)-CBA-X-X
        T1: CBA(s)献祭, T2魔力逆流，碎片服
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'Xmas-chen'
        T.read_templates('img/xmas-chen')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['CBA(s)', '狂兰', '陈宫', 'CBA'])
        master.set_card_weights([1.2, 3, 1, 1.2])
        # ----  NP     Quick    Arts   Buster ----
        master.set_card_templates([
            [],
            [(1, 0), (2, 1), (1, 4), (3, 4)],
            [(1, 7), (1, 5), (1, 2), (2, 5)],
            [(4, 8), (1, 1), (1, 3), (2, 3)],
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
            master.choose_support_drag(match_svt=True, match_ce=False, match_ce_max=False, match_skills=True,
                                       switch_classes=(5, 0))
        else:
            logger.debug('please choose support manually!')
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(1, 3, 3)
        master.svt_skill(1, 2)
        master.svt_skill(1, 1, 2)
        master.attack([8, 1, 2])
        master.realtime_party = ['CBA(s)', '狂兰', '陈宫', 'CBA']
        # noinspection PyStatementEffect
        label.h
        # wave 2
        wait_targets(T.wave2a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 2...')
        master.set_waves(T.wave2a, T.wave2b)
        master.svt_skill(1, 3, 2)
        master.svt_skill(1, 2)
        master.svt_skill(1, 1, 2)
        master.svt_skill(2, 3)
        master.master_skill(3, 2)
        master.auto_attack(nps=7)

        # wave 3
        wait_targets(T.wave3a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        master.svt_skill(3, 2)
        master.svt_skill(3, 1, 1)
        master.svt_skill(3, 3, 2)
        master.master_skill(1, 2)
        master.auto_attack(nps=7)
        master.xjbd(T.kizuna, LOC.kizuna, mode='dmg', allow_unknown=True)
        return
