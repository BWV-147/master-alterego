from gacha import *
from util.supervisor import supervise_log_time


# main entrance
def gacha_with_check(gacha: Gacha, check=True):
    CONFIG.load_config()
    CONFIG.task_finished = False
    CONFIG.log_file = 'logs/gacha.full.log'
    gacha_logger.info('start gacha')
    check_sys_admin()
    if CONFIG.id == 'android':
        pass
    elif CONFIG.id == 'ios':
        pass
    time.sleep(3)
    if check:
        thread = threading.Thread(target=gacha.draw, name='gacha',
                                  args=[], daemon=True)
        supervise_log_time(thread, 120, mail=True, interval=3, )
    else:
        gacha.draw()


# %%
if __name__ == '__main__':
    my_gacha = Gacha()
    gacha_with_check(my_gacha, True)
# end
