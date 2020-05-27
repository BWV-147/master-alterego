from .addon import *
from .autogui import *
from .log import *


def supervise_log_time(thread, time_out=60, mail=None, interval=10, alert_type=None, alert_loops=15):
    # type: (threading.Thread,float,bool,float,bool,int)->None
    assert thread is not None, thread
    config.running_thread = thread
    if mail is None:
        mail = config.mail
    if alert_type is None:
        alert_type = config.alert_type

    def _overtime():
        return config.get_dt() > time_out

    logger.info(f'start supervising thread {thread.name}...')
    thread.start()
    while not thread.is_alive():
        time.sleep(0.01)
    logger.info(f'Thread-{thread.ident}({thread.name}) started...')
    config.update_time()
    # from here, every logging should have arg: NO_LOG_TIME, otherwise endless loop.
    loops = alert_loops
    while True:
        # every case: stop or continue
        # case 1: all right - continue supervision
        if thread.is_alive() and not _overtime():
            loops = alert_loops  # reset loops
            time.sleep(interval)
            continue
        # case 2: thread finished normally - stop supervision
        if config.task_finished:
            # thread finished: all battles finished(thread exit normally)
            logger.info(f'Thread-{thread.ident}({thread.name}) finished. Stop supervising.')
            if mail:
                send_mail(f'[{thread.name}]Task finished.')
            # make sure thread is stopped
            if thread.is_alive():
                kill_thread(thread)
            break

        T: ImageTemplates = config.T
        LOC: Regions = config.LOC
        # case 3: network error - click "retry" and continue
        img_net, loc_net = T.net_error, LOC.net_error
        if img_net is not None and loc_net is not None:
            shot = screenshot()
            if match_targets(shot, img_net, loc_net[0]) and match_targets(shot, img_net, loc_net[1]):
                logger.warning('Network error! click "retry" button')
                click(loc_net[1], lapse=3)
                config.update_time(60)
                continue

        # case 4: re-login after 3am in jp server
        # if match menu button, click save_area until match quest1234, click 1234
        if callable(config.battle.login_handler):
            if match_targets(screenshot(), T.quest, LOC.menu_button):
                config.battle.login_handler()

        # case 5: unrecognized error - waiting user to handle (in 2*loops seconds)
        if loops == alert_loops:
            logger.warning(f'Something wrong, please solve it, or it will be force stopped...\n'
                           f' - thread  alive: {thread.is_alive()}.\n'
                           f' - task finished: {config.task_finished}.\n'
                           f' - last log time: {time.asctime()}')
        if loops >= 0:
            # print(f'{loops}...\r', end='')
            print(f'loops={loops}')
        else:
            logger.warning(f'Time out, it will be force stopped...')
        loops -= 1
        if alert_type:
            beep(1, 2)
        else:
            time.sleep(3)
        if loops < 0:
            # not solved! kill thread and stop.
            err_msg = f'Thread-{thread.ident}({thread.name}): Time run out!\n' \
                      f' - current  time: {time.asctime()}\n' \
                      f' - last log time: {time.asctime(time.localtime(config.log_time))}\n' \
                      f' - over time: {time.time() - config.log_time:.2f}(>{time_out}) secs.\n'
            logger.warning(err_msg)
            if mail:
                send_mail(err_msg, subject=f'[{thread.name}]Went wrong!')
            kill_thread(thread)
            logger.info('exit supervisor after killing thread.')
            break
    raise_alert(alert_type, loops=5)
