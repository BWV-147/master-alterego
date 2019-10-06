from battle import *


def check_sys_settings(admin=True):
    # set dpi awareness & check admin permission
    # useless in Python Console of Pycharm
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    if admin:
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            print('e.g. click somewhere inside admin programs(Blupapa), the python process also need admin permission.')
            print('applying admin permission in a new process, take no effect when in console mode.')
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            exit(0)
        else:
            print('already admin')


# main entrance
def battle_with_check(check=True):
    check_sys_settings()
    my_battle = Battle()
    if check:
        apple = -1
        t1 = threading.Thread(target=my_battle.start, name='C-cba',
                              args=[my_battle.zaxiu_cba, 200, apple, True], daemon=True)
        t2 = threading.Thread(target=my_battle.start, name='C-5bonus',
                              args=[my_battle.zaxiu_caster, 200, apple, True], daemon=True)
        supervise_log_time(t1, 60, mail=False, interval=3)
    else:
        my_battle.start(my_battle.zaxiu_caster_full, 2, -1, False)


# %%
if __name__ == '__main__':
    # when two monitors, and emulator not run at main? monitor,
    # make sure two monitors have the same scale (DPI) in windows settings,
    # otherwise, click will happen at wrong position
    G['goto'] = False
    G['goto_outer'] = False
    G['offset_x'] = -1920
    time.sleep(1)
    battle_with_check(True)

# %%
for i in range(10):
    time.sleep(2)
    pos = (300 + i * 100, 150)
    # click(pos)
    print(f'pos={pos},curPos=', win32api.GetCursorPos())

# end file
