from battle import *


# main entrance
def battle_with_check(check=True):
    logger.warning('start battle', NO_LOG_TIME)
    check_sys_admin()
    time.sleep(3)
    my_battle = Battle()
    if check:
        apple = -1
        isAndroid = True
        if isAndroid:
            Config.jump_battle = False
            Config.check_drop = True
            Config.offset_x = 0
            t = threading.Thread(target=my_battle.start, name='a-zaxiu-ass',
                                 args=[my_battle.a_zaxiu_ass, 'img/a-zaxiu-ass', 100, apple, True], daemon=True)
        else:
            Config.jump_battle = False
            Config.check_drop = True
            Config.offset_x = -1920
            t = threading.Thread(target=my_battle.start, name='s-zaxiu-ass',
                                 args=[my_battle.s_zaxiu_ass, 'img/s-zaxiu-ass', 112, apple, True], daemon=True)
        supervise_log_time(t, 120, mail=True, interval=3)
    else:
        my_battle.start(my_battle.a_zaxiu, 2, -1, False)


# %%
if __name__ == '__main__':
    # pay attention to DPI settings of EACH monitor and proper offset_X/y for click,
    # otherwise, click will happen at wrong position
    battle_with_check(True)

# %%

# end file
