from util.supervisor import *
from .base_agent import BaseAgent


class FpGacha(BaseAgent):
    def __init__(self, path=None):
        super().__init__()
        self.T = ImageTemplates(path)
        self.LOC = Regions()
        logger.set_cur_logger('gacha')

    def start(self, supervise=True, cfg=None):
        # pre-processing
        self.pre_process(cfg)
        config.mail = config.fp_gacha.mail
        self.T.read_templates(config.fp_gacha.dir)
        config.T = self.T
        config.LOC = self.LOC
        start_func = self.draw

        # starting
        logger.info('starting friend point gacha...', extra=LOG_TIME)
        time.sleep(2)
        if supervise:
            t_name = f'fp-{os.path.basename(config.fp_gacha.dir)}'
            thread = threading.Thread(target=start_func, name=t_name, args=[config.fp_gacha.num], daemon=True)
            supervise_log_time(thread, 20, interval=3, alert_loops=3)
        else:
            config.task_thread = threading.current_thread()
            start_func(config.fp_gacha.num)
        self.post_process()

    def draw(self, num=100):
        """
        :param num: times of gacha10(2000fp)
        """
        T = self.T
        LOC = self.LOC

        wait_targets(T.gacha_fp_page, [LOC.gacha_fp_logo])
        logger.info('draw: starting...', extra=LOG_TIME)
        loops = 0
        while loops < num:
            config.update_time()
            if loops % 10 == 0:
                logger.debug(f'fp gacha {loops}/{num}...')
            # wait_targets(T.fp_gacha_page, LOC.fp_gacha_logo, at=LOC.fp_gacha_point)
            page_no = wait_which_target([T.gacha_fp_result, T.gacha_fp_bag2_full],
                                        [LOC.gacha_fp_result_summon, LOC.bag_full_sell_button],
                                        clicking=LOC.gacha_fp_point, interval=0.05)
            if page_no == 0:
                loops += 1
                click(LOC.gacha_fp_result_summon)
                config.update_time()
                config.count_fp_gacha()
            else:
                bag_no = wait_which_target([T.gacha_fp_bag1_full, T.gacha_fp_bag2_full], LOC.fp_bag_full_title)
                if bag_no == 0:
                    logger.info('servant bag full, make sure only show *LOW RARITY<=3* servants.')
                    click(LOC.fp_bag_full_sell_button)
                    self.sell(config.fp_gacha.sell_num, 1, 4)
                else:
                    logger.info('CE bag full, make sure only show *LOW RARITY<=2* CE.')
                    click(LOC.fp_bag_full_enhance_button)
                    self.enhance_ce(config.fp_gacha.enhance_num)
                if [config.fp_gacha.sell_num, config.fp_gacha.enhance_num][bag_no] > 0:
                    wait_targets(T.shop, LOC.menu_button, at=0)
                    wait_targets(T.menu, LOC.menu_gacha_button, at=0)
                    while True:
                        wait_targets(T.gacha_quartz_page, LOC.gacha_help, lapse=0.2)
                        shot = screenshot()
                        if match_targets(shot, T.gacha_quartz_page, LOC.gacha_quartz_logo):
                            click(LOC.gacha_arrow_left)
                        elif match_targets(shot, T.gacha_fp_page, LOC.gacha_fp_logo):
                            logger.debug('back to fp gacha page')
                            break
                else:
                    wait_targets(T.gacha_fp_page, [LOC.gacha_fp_logo])
        config.mark_task_finish()

    def enhance_ce(self, num=100):
        T, LOC = self.T, self.LOC
        logger.info('enhance ce', extra=LOG_TIME)
        if num <= 0:
            logger.info('need manual operation!')
            time.sleep(2)
            config.update_time(config.manual_operation_time)  # min for manual operation
            raise_alert()
            wait_targets(T.shop, LOC.menu_button)
            return
        no = 0
        while True:
            wait_targets(T.ce_enhance_empty, LOC.ce_enhance_help)
            if no >= num:
                click(LOC.bag_back)
                wait_targets(T.shop, LOC.menu_button)
                return
            target_selected = wait_which_target([T.ce_enhance_empty, T.ce_enhance_page], LOC.ce_target_box)
            if target_selected == 0:
                logger.debug('choose enhancement target', extra=LOG_TIME)
                click(LOC.ce_target_box)
                wait_targets(T.ce_select_target, LOC.ce_select_mode)
                shot = screenshot()
                for box in LOC.ce_targets:
                    if match_targets(shot, T.ce_select_target, box):
                        click(box)
                        break
            wait_targets(T.ce_enhance_page, LOC.ce_target_box, at=LOC.ce_select_items_box)
            wait_targets(T.ce_items_unselected, LOC.ce_select_button)
            drag(LOC.ce_select_start, LOC.ce_select_middle, 0.5, 0.5, None, 0)
            drag(LOC.ce_select_middle, LOC.ce_select_end, 0.1, None, 0.2)
            item_selected = wait_which_target([T.ce_items_unselected, T.ce_items_selected], LOC.ce_select_button)
            if item_selected == 0:
                logger.info('no ce left', extra=LOG_TIME)
                if no == 0:
                    logger.warning('ce bag full but nothing can be enhanced! waiting manual operation.')
                    config.update_time(config.manual_operation_time)
                    raise_alert()
                    wait_targets(T.shop, LOC.menu_button)
                    return
                click(LOC.bag_back)
                wait_targets(T.ce_enhance_empty, LOC.ce_enhance_help)
                click(LOC.bag_back)
                wait_targets(T.shop, LOC.menu_button)
                return
            else:
                click(LOC.ce_select_button)
                wait_targets(T.ce_enhance_page, LOC.ce_enhance_lv2)
                click(LOC.ce_enhance_button)
                wait_targets(T.ce_enhance_confirm, LOC.ce_enhance_confirm, at=0)
                wait_targets(T.ce_enhance_empty, LOC.ce_enhance_lv2, clicking=LOC.ce_enhance_button)
                no += 1
                logger.debug(f'enhance {no}', extra=LOG_TIME)
