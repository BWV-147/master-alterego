from battle import *


# main entrance
def battle_with_check(check=True):
    logger.warning('start battle', NO_LOG_TIME)
    check_sys_admin()
    time.sleep(3)
    my_battle = Battle()
    if check:
        apple = 1
        t1 = threading.Thread(target=my_battle.start, name='a-zaxiu-ass',
                              args=[my_battle.a_zaxiu_ass, 100, apple, True], daemon=True)
        t2 = threading.Thread(target=my_battle.start, name='C-5bonus',
                              args=[my_battle.a_zaxiu, 200, apple, False], daemon=True)
        supervise_log_time(t1, 90, mail=True, interval=3)
    else:
        my_battle.start(my_battle.a_zaxiu, 2, -1, False)


# %%
if __name__ == '__main__':
    # pay attention to DPI settings of EACH monitor and proper offset_X/y for click,
    # otherwise, click will happen at wrong position
    screenshot()
    Config.jump_battle = False
    Config.check_drop = False
    Config.offset_x = 0
    battle_with_check(True)

# %%

# end file
