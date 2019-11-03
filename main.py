from battle import *


# main entrance
def battle_with_check(battle: Battle, check=True):
    config.load_config()
    logger.warning('start battle', NO_LOG_TIME)
    check_sys_admin()
    time.sleep(3)
    user_id = config.id
    if user_id == 'android':
        apple = 1
        config.jump_battle = False
        config.check_drop = True
        config.offset_x = 0
        config.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 19, 20)
        if check:
            thread = threading.Thread(target=battle.start, name='a-zaxiu-final',
                                      kwargs={"battle_func": battle.a_zaxiu_final,
                                              "folder": 'img/a-zaxiu-final',
                                              "battle_num": 200,
                                              "total_battle_num": 750,
                                              "apple": apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 120, mail=True, interval=3)
        else:
            battle.start(battle_func=battle.a_zaxiu_final, folder='img/a-zaxiu-final',
                         battle_num=300, apple=apple, auto_choose_support=True)
    elif user_id == 'ios':
        apple = 1
        config.jump_battle = False
        config.check_drop = True
        config.offset_x = 0
        config.enhance_craft_nums = (7, 8, 11, 12, 15, 16, 19, 20)
        if check:
            thread = threading.Thread(target=battle.start, name='s-zaxiu-final',
                                      kwargs={"battle_func": battle.s_zaxiu_final,
                                              "folder": 'img/s-zaxiu-final',
                                              "battle_num": 200,
                                              "total_battle_num": 690,
                                              "apple": apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 120, mail=True, interval=3)
        else:
            battle.start(battle_func=battle.s_zaxiu_final, folder='img/s-zaxiu-final',
                         battle_num=200, apple=apple, auto_choose_support=True)
    else:
        print(f'unknown user id: {user_id}')


# %%
if __name__ == '__main__':
    # pay attention to DPI settings of EACH monitor and proper offset_X/y for click,
    # otherwise, click will happen at wrong position
    my_battle = Battle()
    battle_with_check(my_battle, True)
# %%

# end file
