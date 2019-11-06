from gacha import *
from util.supervisor import supervise_log_time


# main entrance
def draw_with_check(gacha: Gacha, check=True):
    CONFIG.user.load_config()
    CONFIG.task_finished = False
    gacha_logger.info('start gacha')
    check_sys_admin()
    num = 0
    if CONFIG.user.id == 'android':
        gacha.max_clean_item_num = 100
        num = 20
    elif CONFIG.user.id == 'ios':
        gacha.max_clean_item_num = 100
        num = 20
    time.sleep(3)
    if check:
        thread = threading.Thread(target=gacha.draw, name='gacha',
                                  args=[num, ], daemon=True)
        supervise_log_time(thread, 120, mail=False, interval=3)
    else:
        gacha.draw()


# %%
if __name__ == '__main__':
    my_gacha = Gacha()
    draw_with_check(my_gacha, True)
# end
