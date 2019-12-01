from battle import *
from util.supervisor import supervise_log_time


# main entrance
def battle_with_check(battle: Battle, check=True):
    CONFIG.load_config()
    CONFIG.task_finished = False
    CONFIG.log_file = 'logs/log.full.log'
    logger.info('start battle...')
    check_sys_admin()
    time.sleep(3)
    user_id = CONFIG.id
    if user_id.lower() == 'dell':
        if check:
            thread = threading.Thread(target=battle.start, name='test',
                                      kwargs={"battle_func": battle.battle_template,
                                              "folder": 'img/template-jp',
                                              "battle_num": CONFIG.battle_num,
                                              "max_finished_battles": CONFIG.max_finished_battles,
                                              "apple": CONFIG.apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 90, mail=False, interval=3)
        else:
            battle.start(battle_func=battle.battle_template, folder='img/template-jp', apple=CONFIG.apple,
                         battle_num=CONFIG.battle_num, max_finished_battles=CONFIG.max_finished_battles,
                         auto_choose_support=True)
    elif user_id.lower() == 'msi':
        if check:
            thread = threading.Thread(target=battle.start, name='no_battle',
                                      kwargs={"battle_func": battle.battle_template,
                                              "folder": 'img/template-jp',
                                              "battle_num": CONFIG.battle_num,
                                              "max_finished_battles": CONFIG.max_finished_battles,
                                              "apple": CONFIG.apple,
                                              "auto_choose_support": True},
                                      daemon=True)
            supervise_log_time(thread, 200, mail=True, interval=3)
        else:
            battle.start(battle_func=battle.battle_template, folder='img/template-jp', apple=CONFIG.apple,
                         battle_num=CONFIG.battle_num, max_finished_battles=CONFIG.max_finished_battles,
                         auto_choose_support=True)
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
