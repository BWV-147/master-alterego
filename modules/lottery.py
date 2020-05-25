from util.supervisor import *
from .base_agent import BaseAgent


class Lottery(BaseAgent):
    def __init__(self, path=None):
        self.T = ImageTemplates(path)
        self.LOC = Regions()
        logger.set_cur_logger('gacha')

    def start(self, supervise=True, cfg=None):
        # pre-processing
        self.pre_process(cfg)
        self.T.read_templates(config.lottery.dir)
        config.T = self.T
        config.LOC = self.LOC
        start_func = getattr(self, config.lottery.start_func or self.draw.__name__)

        # starting
        logger.info(f'start lottery({start_func.__name__})...', extra=LOG_TIME)
        args = {self.draw.__name__: [config.lottery.num],
                self.clean.__name__: [config.lottery.clean_num],
                self.sell.__name__: [config.lottery.sell_times]
                }[start_func.__name__]
        time.sleep(2)
        if supervise:
            t_name = os.path.basename(config.lottery.dir)
            thread = threading.Thread(target=start_func, name=t_name, args=args, daemon=True)
            supervise_log_time(thread, 120, interval=3)
        else:
            config.running_thread = threading.current_thread()
            start_func(*args)
        self.post_process()

    def draw(self, num=100):
        logger.info('draw: starting...', extra=LOG_TIME)
        T = self.T
        LOC = self.LOC
        wait_targets(T.lottery_initial, LOC.lottery_tab)
        loops = 0
        reset_i = 0
        while True:
            loops += 1
            # print(f'\r loop {loops:<4d}', end='')
            for _ in range(10):
                click(LOC.lottery_point, lapse=0.05)
            shot = screenshot()
            if match_targets(shot, T.lottery_empty, LOC.lottery_empty) and \
                    not match_targets(shot, T.lottery_empty, LOC.lottery_reset_action):
                logger.warning('no ticket left!')
                config.mark_task_finish()
                return
            if match_targets(shot, T.lottery_empty, LOC.lottery_reset_action):
                click(LOC.lottery_reset_action)
                config.count_lottery()
                reset_i += 1
                logger.info(f'reset {reset_i}/{num} times(total {config.lottery.finished}).', extra=LOG_TIME)
                wait_targets(T.lottery_reset_confirm, LOC.lottery_reset_confirm, at=0)
                wait_targets(T.lottery_reset_finish, LOC.lottery_reset_finish, at=0)
                wait_targets(T.lottery_initial, LOC.lottery_10_initial)
                if reset_i >= num:
                    logger.info(f'All {num} lotteries finished.', extra=LOG_TIME)
                    config.mark_task_finish()
                    return
            elif match_targets(shot, T.mailbox_full_alert, LOC.mailbox_full_confirm):
                click(LOC.mailbox_full_confirm)
                logger.info('mailbox full.', extra=LOG_TIME)
                wait_targets(T.mailbox_unselected1, LOC.mailbox_get_all_action)
                self.clean(config.lottery.clean_num)
                wait_targets(T.lottery_initial, LOC.lottery_tab)
                wait_targets(T.lottery_initial, LOC.lottery_10_initial, clicking=LOC.lottery_tab)
                logger.info('already back to lottery.', extra=LOG_TIME)

    def clean(self, num: int = 100):
        """
        Pay attention if cleaning before mailbox is full.
        TODO: if num = numpy.INF, use get_all_items action.

        :param num: max item num to get out from mailbox, if <0: manual mode. num < (box_max_num - 10 - retained_num)
        """
        T = self.T
        LOC = self.LOC
        logger.info('mailbox: cleaning...', extra=LOG_TIME)
        print('Make sure the mailbox **FILTER** only shows "Experience Cards"/"Zhong Huo"!')
        wait_targets(T.mailbox_unselected1, LOC.mailbox_get_all_action)
        if num < 0:
            logger.warning('please clean mailbox manually and return to lottery page!')
            time.sleep(2)
            config.update_time(config.manual_operation_time)  # n min for manual operation
            raise_alert()
            return
        drag_num = config.lottery.clean_drag_times

        def _is_match_offset(_shot, template, old_loc, _offset):
            return match_targets(_shot.crop(numpy.add(old_loc, [0, _offset, 0, _offset])), template.crop(old_loc))

        no = 0
        skipped_drag_num = 0
        MAX_SKIP_NUM = drag_num * 0.2
        while no < num:
            page_no = wait_which_target([T.mailbox_unselected1, T.bag_full_alert],
                                        [LOC.mailbox_get_all_action, LOC.bag_full_sell_button])
            if page_no == 0:
                logger.info('check mailbox items...', extra=LOG_TIME)
                drag_no = 0
                if skipped_drag_num > MAX_SKIP_NUM:  # no item checked:
                    logger.debug(f'no item available, stop cleaning.', extra=LOG_TIME)
                    wait_targets(T.mailbox_unselected1, LOC.mailbox_get_all_action)
                    click(self.LOC.mailbox_back)
                    logger.info('from mailbox back to lottery')
                    return
                while drag_no < drag_num and no < num:
                    drag_no += 1
                    time.sleep(0.2)
                    for mailbox_unselect in [T.mailbox_unselected1, T.mailbox_unselected2]:
                        shot = screenshot()
                        peaks = search_peaks(shot.crop(LOC.mailbox_check_column),
                                             mailbox_unselect.crop(LOC.mailbox_first_checkbox))
                        for y_peak in peaks:
                            y_offset = y_peak - (LOC.mailbox_first_checkbox[1] - LOC.mailbox_check_column[1])
                            if _is_match_offset(shot, mailbox_unselect, LOC.mailbox_first_xn, y_offset) \
                                    or (_is_match_offset(shot, mailbox_unselect, LOC.mailbox_first_icon, y_offset)
                                        and _is_match_offset(shot, mailbox_unselect, LOC.mailbox_first_xn2, y_offset)):
                                click(numpy.add(LOC.mailbox_first_checkbox, [0, y_offset] * 2), lapse=0.01)
                                no += 1
                                skipped_drag_num = 0
                                if no % 10 == 0 or no == num:
                                    logger.debug(f'got items {no}/{num}...', extra=LOG_TIME)
                                if no == num:
                                    break
                        if no >= num:
                            break
                        time.sleep(0.3)
                    if no < num:
                        drag(start=LOC.mailbox_drag_start, end=LOC.mailbox_drag_end,
                             duration=0.5, down_time=0.1, up_time=0.3, lapse=0.1)
                        skipped_drag_num += 1
                    if skipped_drag_num > MAX_SKIP_NUM:
                        break
                logger.info('get mailbox items.', extra=LOG_TIME)
                # wait_which_target(T.mailbox_selected, LOC.mailbox_get_action)
                click(LOC.mailbox_get_action, lapse=1)
                click(LOC.mailbox_get_action, lapse=1)
            elif page_no == 1:
                logger.info('bag full.')
                click(LOC.bag_full_sell_button)
                self.sell(config.lottery.sell_times)
                return

    def sell(self, num=100):
        """
        Back to lottery_initial page finally.

        :param num: num<0: manual mode; num=0: don't sell, go back directly; num>0: sell times.
        :return:
        """
        T = self.T
        LOC = self.LOC
        logger.info('shop: selling...', extra=LOG_TIME)
        print('Make sure the bag **FILTER** only shows "Experience Cards"/"Zhong Huo"!')
        if num <= 0:
            logger.warning('please sell items manually and return to lottery page!')
            time.sleep(2)
            config.update_time(config.manual_operation_time)  # min for manual operation
            raise_alert()
        else:
            no = 0
            while True:
                wait_targets(T.bag_unselected, LOC.bag_sell_action)
                if no < num:
                    drag(LOC.bag_select_start, LOC.bag_select_end, duration=1, down_time=1, up_time=4)
                page_no = wait_which_target([T.bag_selected, T.bag_unselected],
                                            [LOC.bag_sell_action, LOC.bag_sell_action])
                if page_no == 0:
                    no += 1
                    logger.info(f'sell: {no} times...', extra=LOG_TIME)
                    click(LOC.bag_sell_action)
                    wait_targets(T.bag_sell_confirm, LOC.bag_sell_confirm, at=True)
                    wait_targets(T.bag_sell_finish, LOC.bag_sell_finish, at=0)
                else:
                    logger.info('all sold.', extra=LOG_TIME)
                    click(LOC.bag_back)
                    wait_targets(T.shop, LOC.shop_event_item_exchange, at=0)
                    wait_targets(T.shop_event_banner_list,
                                 LOC.shop_event_banner_list[config.lottery.event_banner_no], at=True)
                    wait_targets(T.lottery_initial, LOC.lottery_10_initial, clicking=LOC.lottery_tab)
                    break
        wait_targets(T.lottery_initial, LOC.lottery_10_initial)
        logger.info('from shop back to lottery', extra=LOG_TIME)
