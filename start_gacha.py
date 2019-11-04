from gacha import *
from util.supervisor import supervise_log_time


# main entrance
def draw_with_check(gacha: Gacha, check=True):
    CONFIG.user.load_config()
    gacha_logger.info('start battle')
    check_sys_admin()
    if CONFIG.user.id == 'android':
        gacha.max_clean_box_times = 35
    elif CONFIG.user.id == 'ios':
        gacha.max_clean_box_times = 40
    time.sleep(3)
    if check:
        thread = threading.Thread(target=gacha.draw, name='gacha',
                                  args=[], daemon=True)
        supervise_log_time(thread, 120, mail=False, interval=3)
    else:
        gacha.draw()


# %%
if __name__ == '__main__':
    my_gacha = Gacha()
    draw_with_check(my_gacha, True)
# end
