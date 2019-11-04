from util.autogui import *

gacha_logger = get_logger('gacha')


class Gacha:
    def __init__(self, path='img/gacha'):
        self.T = ImageTemplates(path)
        self.LOC = Regions()
        self.max_clean_box_times = 20
        self.do_sell = True

    def draw(self):
        T = self.T
        LOC = self.LOC
        wait_which_target(T.gacha_initial, LOC.gacha_10_initial)
        gacha_logger.info('start gacha...')
        loops = 0
        reset_num = 0
        while True:
            loops += 1
            print(f'\rloop {loops:<4d}', end='')
            for _ in range(15):
                click(LOC.gacha_point, lapse=0.1)
            shot = screenshot()
            if is_match_target(shot, T.gacha_empty, LOC.gacha_empty) and \
                    not is_match_target(shot, T.gacha_empty, LOC.gacha_reset_action):
                gacha_logger.warning('no ticket left!')
                return
            if is_match_target(shot, T.gacha_empty, LOC.gacha_reset_action):
                click(LOC.gacha_reset_action)
                reset_num += 1
                gacha_logger.debug(f'reset {reset_num} times.')
                wait_which_target(T.gacha_reset_confirm, LOC.gacha_reset_confirm, at=True)
                wait_which_target(T.gacha_reset_finish, LOC.gacha_reset_finish, at=True)
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial)
            elif is_match_target(shot, T.box_full_alert, LOC.box_full_confirm):
                click(LOC.box_full_confirm)
                gacha_logger.debug('mailbox full.')
                wait_which_target(T.box_unselected, LOC.box_get_all_action)
                self.clean_mailbox()
                wait_which_target(T.gacha_initial, LOC.gacha_logo)
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial, clicking=LOC.gacha_tab)
                gacha_logger.debug('already back to gacha.')

    def clean_mailbox(self, num: int = None):
        """
        Pay attention if cleaning before mailbox is full.
        :param num: loops for [select 4 items]->[get action], num < (box_max_num - 10 - retained_num) /4
        """
        T = self.T
        LOC = self.LOC
        gacha_logger.info('cleaning mailbox...')
        num = self.max_clean_box_times if num is None else num
        wait_which_target(T.box_unselected, LOC.box_get_all_action)
        while num > 0:
            print(f'{num:<4d}\r', end='')
            if num % 10 == 0:
                gacha_logger.debug(f'cleaning loops left {num}')
            page_no = wait_which_target([T.box_unselected, T.bag_full_alert],
                                        [LOC.box_get_all_action, LOC.bag_full_sell_action])
            if page_no == 0:
                for loc in self.LOC.box_items:
                    click(loc, lapse=0.10)
                num -= 1
                wait_which_target(T.box_unselected,LOC.box_get_all_action,clicking=LOC.box_get_action)
            elif page_no == 1:
                gacha_logger.debug('bag full.')
                click(LOC.bag_full_sell_action)
                self.sell()
                return
        click(self.LOC.box_back)
        gacha_logger.debug('from mailbox back to gacha')

    def sell(self):
        T = self.T
        LOC = self.LOC
        gacha_logger.info('shop: selling...')
        num = 0
        while True:
            wait_which_target(T.bag_unselected, LOC.bag_sell_action)
            drag(LOC.bag_select_start, LOC.bag_select_end, duration=1, down_time=1, up_time=3)
            page_no = wait_which_target([T.bag_selected, T.bag_unselected], [LOC.bag_sell_action, LOC.bag_sell_action])
            if page_no == 0:
                num += 1
                gacha_logger.debug(f'sell {num} times.')
                click(LOC.bag_sell_action)
                wait_which_target(T.bag_sell_confirm, LOC.bag_sell_confirm, at=True)
                wait_which_target(T.bag_sell_finish, LOC.bag_sell_finish, at=True)
            elif page_no == 1:
                gacha_logger.debug('all items are sold.')
                click(LOC.bag_back)
                wait_which_target(T.shop, LOC.shop_sell)
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial, clicking=LOC.gacha_tab)
                gacha_logger.debug('from shop back to gacha')
                return
