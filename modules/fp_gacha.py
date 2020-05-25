from util.supervisor import *
from .base_agent import BaseAgent


class FpGacha(BaseAgent):
    def __init__(self, path=None):
        self.T = ImageTemplates(path)
        self.LOC = Regions()
        logger.set_cur_logger('gacha')

    def start(self, supervise=True, cfg=None):
        # pre-processing
        self.pre_process(cfg)
        self.T.read_templates(config.fp_gacha.dir)
        config.T = self.T
        config.LOC = self.LOC
        start_func = self.draw

        # starting
        logger.info('starting friend point gacha...', extra=LOG_TIME)
        time.sleep(2)
        if supervise:
            t_name = os.path.basename(config.fp_gacha.dir)
            thread = threading.Thread(target=start_func, name=t_name, args=[config.fp_gacha.num], daemon=True)
            supervise_log_time(thread, 10, interval=3, alert_loops=3)
        else:
            config.running_thread = threading.current_thread()
            start_func(config.fp_gacha.num)
        self.post_process()

    def draw(self, num=100):
        """
        :param num: times of gacha10(2000fp)
        """
        T = self.T
        LOC = self.LOC

        wait_targets(T.fp_gacha_result, [LOC.fp_gacha_logo])
        logger.info('draw: starting...', extra=LOG_TIME)
        loops = 0
        while loops < num:
            # print(f'\r loop {loops:<4d}', end='')
            config.update_time()
            if loops % 10 == 0:
                logger.debug(f'fp gacha {loops}/{num}...')
            # wait_targets(T.fp_gacha_page, LOC.fp_gacha_logo, at=LOC.fp_gacha_point)
            page_no = wait_which_target([T.fp_gacha_result, T.fp_bag2_full],
                                        [LOC.fp_gacha_result_summon, LOC.bag_full_sell_button],
                                        clicking=LOC.fp_gacha_point, interval=0.05)
            if page_no == 0:
                loops += 1
                click(LOC.fp_gacha_result_summon)
                config.update_time()
                config.count_fp_gacha()
            elif page_no > 0:
                if match_targets(screenshot(), T.fp_bag1_full, LOC.fp_bag_full_title):
                    logger.info('servant bag full, make sure only show *LOW RARITY<=3* servants.')
                    click(LOC.fp_bag_full_sell_button)
                    pass
                elif match_targets(screenshot(), T.fp_bag2_full, LOC.fp_bag_full_title):
                    logger.info('CE bag full, make sure only show *LOW RARITY<=2* CE.')
                    click(LOC.fp_bag_full_enhance_button)
                    pass

                logger.info(f'bag {page_no} full, sell or enhance manually.', extra=LOG_TIME)
                config.update_time(config.manual_operation_time)
                raise_alert(loops=1)
                wait_targets(T.fp_gacha_result, LOC.fp_gacha_logo)
                logger.info('back to fp gacha.', extra=LOG_TIME)
        config.mark_task_finish()
