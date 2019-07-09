from battle import *


def start_battle(battle_func, num=10, apple=-1):
    # type:(Callable[[Master,int],None],int,int)->None
    """
    set_battle_data first.
    :param battle_func: start at quest banner screen, end at kizuna screen
    :param num:
    :param apple:
    :return:
    """
    master = Master()
    T = master.T
    LOC = master.LOC
    timer = Timer()
    finished = 0
    while finished < num:
        timer.start()
        finished += 1
        logger.info(f'>>>>> Battle "{master.quest_name}" No.{finished}/{num} <<<<<')
        battle_func(master, apple)
        wait_which_target(T.rewards, LOC.finish_qp, clicking=LOC.finish_qp, lapse=0.5)
        # check reward_page has CE dropped or not
        ce = screenshot()
        ce.save(f"img/craft/craft-{time.strftime('%m%d-%H-%M-%S')}.png")
        click(LOC.finish_next)
        logger.info('battle finished, checking rewards.')
        while True:
            page_no = wait_which_target([T.quest, T.apply_friend, T.friend_point],
                                        [LOC.quest, LOC.apply_friend, LOC.friend_point])
            if page_no == 1:
                click(LOC.apply_friend_deny)
            elif page_no == 2:
                click(LOC.friend_point)
            elif page_no == 0:
                break
        dt = timer.stop().dt
        logger.info(f'--- Battle {finished} finished, time = {int(dt // 60)} min {int(dt % 60)} sec.')
        with open('log/time.log', 'a') as fd:
            fd.write(str(dt) + '\n')
    logger.info(f'>>>>> All {finished} battles "{master.quest_name}" finished. <<<<<')


# main entrance
def battle_with_check(check=True):
    check_admin()
    battle = Battle()
    if check:
        t_ios = threading.Thread(target=battle.start, name='left-ios',
                                 args=[battle.chaos_ios, 400, 2], daemon=True)
        t_adr = threading.Thread(target=battle.start, name='android',
                                 args=[battle.chaos_android, 400, 2], daemon=True)
        supervise_log_time([t_adr], 50, mail=False, interval=10)
    else:
        battle.start(battle.chaos_android, 2, -1)


if __name__ == '__main__':
    G['goto'] = False
    time.sleep(1)
    battle_with_check(True)

# end file
