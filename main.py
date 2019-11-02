from battle import *


# main entrance
def battle_with_check(check=True):
    config.load_config()
    logger.warning('start battle', NO_LOG_TIME)
    check_sys_admin()
    time.sleep(3)
    my_battle = Battle()
    user_id = config.id
    if user_id == 'android':
        apple = 1
        config.jump_battle = False
        config.check_drop = True
        config.offset_x = 0
        config.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 19, 20)
        if check:
            thread = threading.Thread(target=my_battle.start, name='a-zaxiu-final',
                                      kwargs={"battle_func": my_battle.a_zaxiu_final,
                                              "folder": 'img/a-zaxiu-final',
                                              "num": 300,
                                              "apple": apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 120, mail=True, interval=3)
        else:
            my_battle.start(battle_func=my_battle.a_zaxiu_final, folder='img/a-zaxiu-final',
                            num=300, apple=apple, auto_choose_support=True)
    elif user_id == 'ios':
        apple = 1
        config.jump_battle = False
        config.check_drop = True
        config.offset_x = 0
        config.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 19, 20)
        if check:
            thread = threading.Thread(target=my_battle.start, name='s-zaxiu-final',
                                      kwargs={"battle_func": my_battle.s_zaxiu_final,
                                              "folder": 'img/s-zaxiu-final',
                                              "num": 300,
                                              "apple": apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 120, mail=True, interval=3)
        else:
            my_battle.start(battle_func=my_battle.s_zaxiu_final, folder='img/s-zaxiu-final',
                            num=300, apple=apple, auto_choose_support=True)
    else:
        print(f'unknown user id: {user_id}')


# %%
if __name__ == '__main__':
    # pay attention to DPI settings of EACH monitor and proper offset_X/y for click,
    # otherwise, click will happen at wrong position
    battle_with_check(True)
# %%

# end file
