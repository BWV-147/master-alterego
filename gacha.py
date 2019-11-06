from util.autogui import *

gacha_logger = get_logger('gacha')


class Gacha:
    def __init__(self, path='img/gacha'):
        self.T = ImageTemplates(path)
        self.LOC = Regions()
        self.do_sell = True

    def draw(self):
        T = self.T
        LOC = self.LOC
        wait_which_target(T.gacha_initial, LOC.gacha_10_initial)
        gacha_logger.info('gacha: starting...')
        loops = 0
        total_num = CONFIG.gacha_num
        while True:
            loops += 1
            # print(f'\rloop {loops:<4d}', end='')
            for _ in range(15):
                click(LOC.gacha_point, lapse=0.1)
            shot = screenshot()
            if is_match_target(shot, T.gacha_empty, LOC.gacha_empty) and \
                    not is_match_target(shot, T.gacha_empty, LOC.gacha_reset_action):
                gacha_logger.warning('no ticket left!')
                return
            if is_match_target(shot, T.gacha_empty, LOC.gacha_reset_action):
                click(LOC.gacha_reset_action)
                CONFIG.count_gacha()
                gacha_logger.debug(f'reset {total_num - CONFIG.gacha_num}/{total_num} times.')
                wait_which_target(T.gacha_reset_confirm, LOC.gacha_reset_confirm, at=True)
                wait_which_target(T.gacha_reset_finish, LOC.gacha_reset_finish, at=True)
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial)
                if CONFIG.gacha_num <= 0:
                    gacha_logger.info(f'All {total_num} gacha finished.')
                    CONFIG.task_finished = True
                    return
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
        :param num: max item num to get out from mailbox, num < (box_max_num - 10 - retained_num)
        TODO: if num = np.INF, use get_all_items action.
        """

        T = self.T
        LOC = self.LOC
        gacha_logger.info('mailbox: cleaning...')
        print('Make sure the mailbox **FILTER** only shows "Experience Cards"/"Zhong Huo"!')
        if num is None:
            num = CONFIG.mailbox_clean_num
        wait_which_target(T.box_unselected, LOC.box_get_all_action)

        first_item = LOC.box_items[0]
        checkbox_height = first_item[3] - first_item[1]
        x = (first_item[0] + first_item[2]) // 2
        dy = LOC.box_items[1][1] - LOC.box_items[0][1]
        drag_num = 10

        no = 0
        while no <= num:
            page_no = wait_which_target([T.box_unselected, T.bag_full_alert],
                                        [LOC.box_get_all_action, LOC.bag_full_sell_action])
            if page_no == 0:
                drag_no = 0
                while drag_no < drag_num and no < num:
                    drag_no += 1
                    peaks = search_peaks(screenshot().crop(LOC.box_check_column),
                                         T.box_unselected.crop(first_item),
                                         distance=dy // 2)
                    ys = [LOC.box_check_column[1] + checkbox_height // 2 + p for p in peaks]
                    # print(f'{len(ys)} peaks={ys}', end='')
                    for y in ys:
                        no += 1
                        click((x, y), lapse=0.1)
                        # print(f'{no:<4d}', end='\r')
                        if no % 10 == 0:
                            gacha_logger.debug(f'cleaning items {no}/{num}...')
                        if no == num:
                            gacha_logger.debug(f'cleaned all items {no}/{num}...')
                            break
                    if no < num:
                        drag(start=LOC.box_drag_start, end=LOC.box_drag_end,
                             duration=0.5, down_time=0.1, up_time=0.3, lapse=0.1)
                gacha_logger.debug('get mailbox items.')
                click(LOC.box_get_action, lapse=1)
                click(LOC.box_get_action, lapse=1)
            elif page_no == 1:
                gacha_logger.debug('bag full.')
                click(LOC.bag_full_sell_action)
                self.sell()
                return
        wait_which_target(T.box_unselected, LOC.box_get_all_action)
        click(self.LOC.box_back)
        gacha_logger.debug('from mailbox back to gacha')

    def sell(self):
        T = self.T
        LOC = self.LOC
        gacha_logger.info('shop: selling...')
        print('Make sure the bag **FILTER** only shows "Experience Cards"/"Zhong Huo"!')
        num = 0
        while True:
            wait_which_target(T.bag_unselected, LOC.bag_sell_action)
            drag(LOC.bag_select_start, LOC.bag_select_end, duration=1, down_time=1, up_time=4)
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
                # TODO: if event banner is not first one, add shop_event_list_page
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial, clicking=LOC.gacha_tab)
                gacha_logger.debug('from shop back to gacha')
                return
