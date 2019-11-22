from battle import *
from util.supervisor import supervise_log_time


# main entrance
def battle_with_check(battle: Battle, check=True):
    # TODO: add start server before start battle, if is not listening. the port
    CONFIG.load_config()
    CONFIG.task_finished = False
    CONFIG.log_file = 'logs/log.full.log'
    logger.info('start battle')
    check_sys_admin()
    time.sleep(3)
    user_id = CONFIG.id
    if user_id == 'jp':
        if check:
            thread = threading.Thread(target=battle.start, name='jp-bond-nito',
                                      kwargs={"battle_func": battle.jp_bond_nito,
                                              "folder": 'img/jp-bond-nito',
                                              "battle_num": CONFIG.battle_num,
                                              "total_battle_num": 2000,
                                              "apple": CONFIG.apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 120, mail=True, interval=3)
        else:
            battle.start(battle_func=battle.a_zaxiu_final, folder='img/jp-bond', apple=CONFIG.apple,
                         battle_num=CONFIG.battle_num, total_battle_num=1000, auto_choose_support=True)
    elif user_id == 'ios':
        if check:
            thread = threading.Thread(target=battle.start, name='s-zaxiu-final',
                                      kwargs={"battle_func": battle.s_zaxiu_final,
                                              "folder": 'img/s-zaxiu-final',
                                              "battle_num": CONFIG.battle_num,
                                              "total_battle_num": 1000,
                                              "apple": CONFIG.apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 200, mail=True, interval=3)
        else:
            battle.start(battle_func=battle.s_zaxiu_final, folder='img/s-zaxiu-final', apple=CONFIG.apple,
                         battle_num=CONFIG.battle_num, total_battle_num=1000, auto_choose_support=True)
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
