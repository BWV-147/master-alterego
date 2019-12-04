from util.gacha import *
from util.supervisor import supervise_log_time


# main entrance
def gacha_with_check(gacha: Gacha, check=True):
    check_sys_admin()
    config.load_config()
    BaseConfig.task_finished = False
    config.log_file = 'logs/gacha.full.log'
    gacha_logger.info('start gacha...')
    if config.id == 'dell':
        gacha.T.read_templates('img/gacha-jp')
    elif config.id == 'msi':
        gacha.T.read_templates('img/gacha')
    time.sleep(2)
    if check:
        thread = threading.Thread(target=gacha.draw, name='xmas-gacha', args=[config.gacha_num], daemon=True)
        supervise_log_time(thread, 120, mail=False, interval=3)
    else:
        gacha.draw(config.gacha_num)


# %%
if __name__ == '__main__':
    my_gacha = Gacha()
    gacha_with_check(my_gacha, True)
# end
