from battle import *


def shutdown(signum, frame):
    print('shutdown: ', signum, frame)
    raise RuntimeError('something went wrong.')


# main entrance
def battle_with_check(battle_func, num=10, apple=-1, quest='default-quest', check=True):
    # type:(Callable[[Master,int],None],int,int,str,bool)->None
    master = Master(quest)
    check_admin()
    if check:
        executor = ThreadPoolExecutor()
        thread1 = executor.submit(master.start_battle, battle_func, num, apple)
        thread2 = executor.submit(check_log_time, 50)
        while not G.get('shutdown', False) and not thread1.done():
            time.sleep(2)
        import sys
        print('shutdown.')
        # raise RuntimeError('runtime error')
        sys.exit(0)
    else:
        master.start_battle(battle_func, num, apple)


# %%
if __name__ == '__main__':
    G['goto'] = False
    G['mail'] = False
    battle_with_check(battle_charlotte_android, 2, -1, 'charlotte-android', True)
    # battle_with_check(battle_charlotte_ios, 'img/charlotte-ios', 5, -1, True)

# end file
