"""Store battle_func for different battles"""
from util.base_battle import *


# noinspection PyPep8Naming,DuplicatedCode
class Battle(BattleBase):
    """
    采用好友助战(如孔明)时，若涉及其指令卡识别，务必加入三个再临阶段的指令卡
    ensure the same app version.
    """

    @with_goto
    def a_archer(self, pre_process=False):
        """
        阵容: 幼贞-艾蕾-孔明-X-X，减CD服
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'A-Archer'
        T.read_templates('img/a-archer')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['幼贞', '艾蕾', '孔明'])
        master.show_svt_name = True

        # w_np: 幼贞 np first; w_dmg: damage first
        w_np = [[19, 25, 22], [10, 15, 20], [1, 2, 3]]
        w_dmg = [[19, 21, 22], [10, 15, 20], [1, 2, 3]]
        master.set_card_weights(w_np)
        # ---- NP     Quick   Arts   Buster ----
        master.set_card_templates([
            [(5, 6), (2, 4), (3, 1), (1, 1)],
            [(4, 7), (1, 5), (2, 1), (3, 4)],
            [(1, 0), [(2, 3), (5, 2), (8, 4)], [(1, 2), (4, 1), (8, 3)], [(3, 2), (5, 1), (9, 4)]]
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
                                       switch_classes=(0, 5))
        else:
            logger.debug('please choose support manually in 60s!')

        # noinspection PyStatementEffect
        label.h
        cur_turn = 1
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(1, 2)
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.svt_skill(3, 1, 2)
        master.master_skill(3, 3)
        master.set_card_weights(w_np)
        cards_t1 = master.auto_attack(mode='alter')
        cur_turn += 1
        if Card.has_card(cards_t1, 1, 2) > 0:
            # T1 幼贞蓝爆+10NP，自由打
            master.set_card_weights(w_dmg)
            xjbd1_cards = master.xjbd(T.wave2a, [LOC.wave_num, LOC.master_skill], 'alter')
            cur_turn += len(xjbd1_cards)
            # wave 2
            logger.debug('wave 2...')
            master.set_waves(T.wave2a, T.wave2b)
            click(LOC.enemies[0])
            master.svt_skill(2, 3)
        else:
            # T1没蓝爆，则开艾蕾全体黄金律
            master.set_card_weights(w_np)
            master.svt_skill_full(T.wave2a, T.wave2b, 2, 3)
            xjbd1_cards = master.xjbd(T.wave2a, [LOC.wave_num, LOC.master_skill], 'alter')
            # wave 2
            logger.debug('wave 2...')
            click(LOC.enemies[0])
            master.set_card_weights(w_dmg)
            master.set_waves(T.wave2a, T.wave2b)
            cur_turn += len(xjbd1_cards)
            possible_cards = []
            for i, t_cards in enumerate(xjbd1_cards):
                if i < len(xjbd1_cards) - 1:
                    possible_cards = possible_cards + t_cards
                else:
                    possible_cards.append(t_cards[0])
            if Card.has_card(possible_cards, 1, 2) > 0:
                # 至wave2有蓝卡，则正常打
                pass
            else:
                # 至wave2无蓝卡(wave1 <3t)，盯着奇美拉打完前3T必有蓝卡
                master.xjbd(T.wave3a, [LOC.wave_num, LOC.master_skill], turns=4 - cur_turn)
                cur_turn = 4
        master.svt_skill(2, 2)
        master.auto_attack(nps=7)
        cur_turn += 1
        xjbd2_cards = master.xjbd(T.wave3a, [LOC.wave_num, LOC.master_skill])
        cur_turn += len(xjbd2_cards)

        # wave 3
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        click(LOC.enemies[1])
        if cur_turn < 5:
            # 确保T5孔明技能冷却
            master.xjbd(T.kizuna, LOC.kizuna, turns=5 - cur_turn)
            cur_turn = 5
        master.svt_skill(1, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 2)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 1, 1)
        master.auto_attack(nps=6)
        cur_turn += 1
        # # noinspection PyStatementEffect
        # label.h
        # cur_turn = 5
        xjbd4_cards = master.xjbd(T.kizuna, LOC.kizuna, allow_unknown=True)
        cur_turn += len(xjbd4_cards)
        logger.info(f'Battle finished in {cur_turn - 1} turns.')
        return

    @with_goto
    def s_archer(self, pre_process=False):
        """
        阵容: 幼贞-艾蕾-孔明-X-X，减CD服
        """
        master = self.master
        T = master.T
        LOC = master.LOC

        # pre-processing: only configure base info
        master.quest_name = 'S-Archer'
        T.read_templates('img/s-archer')
        # LOC.relocate((0, 0, 1920 - 1, 1080 - 1))
        master.set_party_members(['幼贞', '艾蕾', '孔明'])
        master.show_svt_name = True

        # w_np: 幼贞 np first; w_dmg: damage first
        w_np = [[19, 25, 22], [10, 15, 20], [1, 2, 3]]
        w_dmg = [[19, 21, 22], [10, 15, 20], [1, 2, 3]]
        master.set_card_weights(w_np)
        # ---- NP     Quick   Arts   Buster ----
        master.set_card_templates([
            [(9, 6), (1, 1), (1, 2), (1, 3)],
            [(3, 7), (3, 2), (3, 4), (3, 1)],
            [(1, 0), [(1, 5), (6, 4), (7, 5)], [(1, 4), (4, 3), (7, 2)], [(3, 3), (6, 5), (8, 3)]]
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
                                       switch_classes=(0, 5))
        else:
            logger.debug('please choose support manually in 60s!')

        # noinspection PyStatementEffect
        label.h
        cur_turn = 1
        # wave 1
        wait_targets(T.wave1a, [LOC.wave_num, LOC.master_skill])
        logger.debug('wave 1...')
        master.set_waves(T.wave1a, T.wave1b)
        master.svt_skill(3, 2)
        master.svt_skill(3, 3)
        master.svt_skill(3, 1, 2)
        master.master_skill(3, 3)
        master.set_card_weights(w_np)
        cards_t1 = master.auto_attack(mode='alter')
        cur_turn += 1
        if Card.has_card(cards_t1, 1, 2) > 0:
            # T1 幼贞蓝爆+10NP，自由打
            master.set_card_weights(w_dmg)
            xjbd1_cards = master.xjbd(T.wave2a, [LOC.wave_num, LOC.master_skill], 'alter')
            cur_turn += len(xjbd1_cards)
            # wave 2
            logger.debug('wave 2...')
            master.set_waves(T.wave2a, T.wave2b)
            click(LOC.enemies[0])
            master.svt_skill(2, 3)
        else:
            # T1没蓝爆，则开艾蕾全体黄金律
            master.set_card_weights(w_np)
            master.svt_skill_full(T.wave2a, T.wave2b, 2, 3)
            xjbd1_cards = master.xjbd(T.wave2a, [LOC.wave_num, LOC.master_skill], 'alter')
            # wave 2
            logger.debug('wave 2...')
            click(LOC.enemies[0])
            master.set_card_weights(w_dmg)
            master.set_waves(T.wave2a, T.wave2b)
            cur_turn += len(xjbd1_cards)
            possible_cards = []
            for i, t_cards in enumerate(xjbd1_cards):
                if i < len(xjbd1_cards) - 1:
                    possible_cards = possible_cards + t_cards
                else:
                    possible_cards.append(t_cards[0])
            print(f'possible cards: {possible_cards}')
            if Card.has_card(possible_cards, 1, 2) > 0:
                # 至wave2有蓝卡，则正常打
                pass
            else:
                # 至wave2无蓝卡(wave1 <3t)，盯着奇美拉打完前3T必有蓝卡
                master.xjbd(T.wave3a, [LOC.wave_num, LOC.master_skill], turns=4 - cur_turn)
                cur_turn = 4
        master.svt_skill(2, 2)
        master.auto_attack(nps=7)
        cur_turn += 1
        xjbd2_cards = master.xjbd(T.wave3a, [LOC.wave_num, LOC.master_skill])
        cur_turn += len(xjbd2_cards)

        # wave 3
        logger.debug('wave 3...')
        master.set_waves(T.wave3a, T.wave3b)
        click(LOC.enemies[1])
        if cur_turn < 5:
            # 确保T5孔明技能冷却
            master.xjbd(T.kizuna, LOC.kizuna, turns=5 - cur_turn)
            cur_turn = 5
        master.svt_skill(1, 2)
        master.svt_skill(1, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 2)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 3)
        master.svt_skill_full(T.wave1a, T.wave1b, 3, 1, 1)
        master.auto_attack(nps=6)
        cur_turn += 1
        # # noinspection PyStatementEffect
        # label.h
        # cur_turn = 5
        xjbd4_cards = master.xjbd(T.kizuna, LOC.kizuna, allow_unknown=True)
        cur_turn += len(xjbd4_cards)
        logger.info(f'Battle finished in {cur_turn - 1} turns.')
        return
