from util.autogui import *

gacha_logger = get_logger('gacha')


class Gacha:
    def __init__(self, path=None):
        self.T = ImageTemplates(path)
        self.LOC = Regions()
        self.do_sell = True

    def draw(self, num=100):
        T = self.T
        LOC = self.LOC
        wait_which_target(T.gacha_initial, LOC.gacha_tab)
        gacha_logger.info('gacha: starting...')
        loops = 0
        reset_i = 0
        while True:
            loops += 1
            # print(f'\rloop {loops:<4d}', end='')
            for _ in range(25):
                click(LOC.gacha_point, lapse=0.05)
            shot = screenshot()
            if is_match_target(shot, T.gacha_empty, LOC.gacha_empty) and \
                    not is_match_target(shot, T.gacha_empty, LOC.gacha_reset_action):
                gacha_logger.warning('no ticket left!')
                BaseConfig.task_finished = True
                return
            if is_match_target(shot, T.gacha_empty, LOC.gacha_reset_action):
                click(LOC.gacha_reset_action)
                config.count_gacha()
                reset_i += 1
                gacha_logger.info(f'reset {reset_i}/{num} times(total {config.total_gacha_num}).')
                wait_which_target(T.gacha_reset_confirm, LOC.gacha_reset_confirm, at=True)
                wait_which_target(T.gacha_reset_finish, LOC.gacha_reset_finish, at=True)
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial)
                if reset_i >= num:
                    gacha_logger.info(f'All {num} gacha finished.')
                    BaseConfig.task_finished = True
                    return
            elif is_match_target(shot, T.mailbox_full_alert, LOC.mailbox_full_confirm):
                click(LOC.mailbox_full_confirm)
                gacha_logger.info('mailbox full.')
                wait_which_target(T.mailbox_unselected1, LOC.mailbox_get_all_action)
                if config.mailbox_clean_num <= 0:
                    print('clean mailbox manually!')
                    return
                self.clean_mailbox(config.mailbox_clean_num)
                wait_which_target(T.gacha_initial, LOC.gacha_tab)
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial, clicking=LOC.gacha_tab)
                gacha_logger.info('already back to gacha.')

    def clean_mailbox(self, num: int = 100):
        """
        Pay attention if cleaning before mailbox is full.
        :param num: max item num to get out from mailbox, num < (box_max_num - 10 - retained_num)
        TODO: if num = np.INF, use get_all_items action.
        """

        T = self.T
        LOC = self.LOC
        gacha_logger.info('mailbox: cleaning...')
        print('Make sure the mailbox **FILTER** only shows "Experience Cards"/"Zhong Huo"!')
        wait_which_target(T.mailbox_unselected1, LOC.mailbox_get_all_action)

        drag_num = 10

        def _is_match_offset(_shot, template, old_loc, _offset):
            return is_match_target(_shot.crop(np.add(old_loc, [0, _offset, 0, _offset])), template.crop(old_loc))

        no = 0
        while True:
            page_no = wait_which_target([T.mailbox_unselected1, T.bag_full_alert],
                                        [LOC.mailbox_get_all_action, LOC.bag_full_sell_action])
            if page_no == 0:
                gacha_logger.info('check mailbox items...')
                drag_no = 0
                while drag_no < drag_num and no < num:
                    drag_no += 1
                    time.sleep(0.2)
                    for mailbox_unselect in [T.mailbox_unselected1, T.mailbox_unselected2]:
                        shot = screenshot()
                        peaks = search_peaks(shot.crop(LOC.mailbox_check_column),
                                             mailbox_unselect.crop(LOC.mailbox_first_checkbox))
                        # print(f'peaks {i}={peaks}')
                        for y_peak in peaks:
                            no += 1
                            y_offset = y_peak - (LOC.mailbox_first_checkbox[1] - LOC.mailbox_check_column[1])
                            if _is_match_offset(shot, mailbox_unselect, LOC.mailbox_first_xn, y_offset) \
                                    or _is_match_offset(shot, mailbox_unselect, LOC.mailbox_first_icon, y_offset):
                                click(np.add(LOC.mailbox_first_checkbox, [0, y_offset] * 2), lapse=0.01)
                            if no % 10 == 0:
                                gacha_logger.debug(f'reviewed items {no}/{num}...')
                            if no == num:
                                gacha_logger.info(f'reviewed all items {no}/{num}...')
                                break
                    if no < num:
                        drag(start=LOC.mailbox_drag_start, end=LOC.mailbox_drag_end,
                             duration=0.5, down_time=0.1, up_time=0.3, lapse=0.1)
                gacha_logger.info('get mailbox items.')
                wait_which_target(T.mailbox_selected, LOC.mailbox_get_action)
                click(LOC.mailbox_get_action, lapse=1)
                click(LOC.mailbox_get_action, lapse=1)
            elif page_no == 1:
                gacha_logger.info('bag full.')
                click(LOC.bag_full_sell_action)
                if config.do_sell:
                    self.sell()
                else:
                    gacha_logger.info('bag full! clean bag please!')
                return
            if no >= num:
                break
        wait_which_target(T.mailbox_unselected1, LOC.mailbox_get_all_action)
        click(self.LOC.mailbox_back)
        gacha_logger.info('from mailbox back to gacha')

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
                gacha_logger.info(f'sell {num} times.')
                click(LOC.bag_sell_action)
                wait_which_target(T.bag_sell_confirm, LOC.bag_sell_confirm, at=True)
                wait_which_target(T.bag_sell_finish, LOC.bag_sell_finish, at=True)
            elif page_no == 1:
                gacha_logger.info('all items are sold.')
                click(LOC.bag_back)
                wait_which_target(T.shop, LOC.shop_event_item_exchange, at=True)
                wait_which_target(T.shop_event_banner_list, LOC.shop_event_banner_list[config.event_banner_no], at=True)
                wait_which_target(T.gacha_initial, LOC.gacha_10_initial, clicking=LOC.gacha_tab)
                gacha_logger.info('from shop back to gacha')
                return
