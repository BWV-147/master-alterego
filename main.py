from battle import *


# main entrance
def battle_with_check(check=True):
    logger.warning('start battle', NO_LOG_TIME)
    check_sys_admin()
    my_battle = Battle()
    if check:
        apple = 3
        t1 = threading.Thread(target=my_battle.start, name='A-zaxiu-1',
                              args=[my_battle.a_zaxiu, 10, apple, False], daemon=True)
        t2 = threading.Thread(target=my_battle.start, name='C-5bonus',
                              args=[my_battle.a_zaxiu, 200, apple, False], daemon=True)
        supervise_log_time(t1, 60, mail=False, interval=3)
    else:
        my_battle.start(my_battle.a_zaxiu, 2, -1, False)


# %%
if __name__ == '__main__':
    # when two monitors, and emulator not run at main? monitor,
    # make sure two monitors have the same scale (DPI) in windows settings,
    # otherwise, click will happen at wrong position
    G['goto'] = True
    G['goto_outer'] = False
    G['offset_x'] = -1920
    time.sleep(1)
    battle_with_check(True)

# %%

# end file
