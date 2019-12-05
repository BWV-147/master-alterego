from battle import *
from util.supervisor import supervise_log_time


# main entrance
def battle_with_check(battle: Battle, check=True, conf=None):
    config.load_config(conf)
    check_sys_admin()
    BaseConfig.task_finished = False
    config.log_file = 'logs/log.full.log'
    logger.info('start battle...')
    time.sleep(2)
    if config.id == 'dell':
        battle_func = battle.xmas_von
        t_name: str = battle_func.__name__.replace('_', '-').capitalize()
        if check:
            thread = threading.Thread(target=battle.start, name=t_name,
                                      kwargs={
                                          "battle_func": battle_func,
                                          "battle_num": config.battle_num,
                                          "apples": config.apples
                                      },
                                      daemon=True)
            supervise_log_time(thread, 90, mail=config.mail, interval=3)
        else:
            battle.start(battle_func=battle_func, battle_num=config.battle_num, apples=config.apples)
    elif config.id == 'rescue':
        battle_func = battle.xmas_rescue
        t_name: str = battle_func.__name__.replace('_', '-').capitalize()
        if check:
            thread = threading.Thread(target=battle.start, name=t_name,
                                      kwargs={
                                          "battle_func": battle_func,
                                          "battle_num": config.battle_num,
                                          "apples": config.apples
                                      },
                                      daemon=True)
            supervise_log_time(thread, 200, mail=config.mail, interval=3)
        else:
            battle.start(battle_func=battle_func, battle_num=config.battle_num, apples=config.apples)
    else:
        print(f'unknown user id: {config.id}')


# %%
if __name__ == '__main__':
    # pay attention to DPI settings of EACH monitor and proper offset_X/y for click,
    # otherwise, click will happen at wrong position
    my_battle = Battle()
    battle_with_check(my_battle, True, 'config.json')
# %%
#
# end file
