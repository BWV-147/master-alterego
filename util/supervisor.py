from util.autogui import *


def supervise_log_time(thread: threading.Thread, secs=60, mail: bool = None, interval=10, alert: bool = None):
    assert thread is not None, thread
    if mail is None:
        mail = config.mail
    if alert is None:
        alert = config.alert

    def _overtime():
        return time.time() - BaseConfig.log_time > secs

    logger.info(f'start supervising thread {thread.name}...')
    thread.start()
    while not thread.is_alive():
        time.sleep(0.01)
    logger.info(f'Thread-{thread.ident}({thread.name}) started...')
    BaseConfig.log_time = time.time()
    # from here, every logging should have arg: NO_LOG_TIME, otherwise endless loop.
    loops = MAX_LOOPS = 15
    while True:
        # every case: stop or continue
        # case 1: all right - continue supervision
        if not _overtime():
            loops = MAX_LOOPS  # reset loops
            time.sleep(interval)
            continue
        # case 2: thread finished normally - stop supervision
        if not thread.is_alive() and BaseConfig.task_finished:
            # thread finished
            logger.debug(f'Thread-{thread.ident}({thread.name}) finished. Stop supervising.')
            if mail:
                send_mail('Task finished.')
            break

        # something wrong
        # case 3: network error - click "retry" and continue
        if config.img_net is not None and config.loc_net is not None:
            shot = screenshot()
            if is_match_target(shot, config.img_net, config.loc_net[0]) and \
                    is_match_target(shot, config.img_net, config.loc_net[1]):
                logger.warning('Network error! click "retry" button', NO_LOG_TIME)
                click(config.loc_net[1], lapse=3)
                BaseConfig.log_time += 60
                continue
        # case 4: unrecognized error - waiting user to handle (in 2*loops seconds)
        if loops == MAX_LOOPS:
            logger.warning(f'Something wrong, please solve it, or it will be force stopped...', NO_LOG_TIME)
        if loops >= 0:
            print(f'\r{loops}...\r', end='')
        else:
            logger.warning(f'Time out, it will be force stopped...', NO_LOG_TIME)
        loops -= 1
        if alert:
            beep(1, 2)
        else:
            time.sleep(3)
        if loops < 0:
            # not solved! kill thread and stop.
            err_msg = f'Thread-{thread.ident}({thread.name}): Time run out!\n' \
                      f'lapse={time.time() - BaseConfig.log_time:.2f}(>{secs}) secs.\n' \
                      f'lg_time={time.asctime(time.localtime(BaseConfig.log_time))}'
            print(err_msg)
            if mail:
                send_mail(err_msg, subject=f'[{thread.name}]something went wrong!')
            kill_thread(thread)
            print('exit supervisor after killing thread.')
            break
    if alert is True:
        beep(2, 1, 20)
    elif isinstance(alert, str):
        play_ringtone(alert, 5)


# inspired by https://github.com/mosquito/crew/blob/master/crew/worker/thread.py
def kill_thread(thread: threading.Thread):
    logger.warning(f'ready to kill thread-{thread.ident}({thread.name})')
    if not thread.is_alive():
        return

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), ctypes.py_object(SystemExit)
    )
    # print(f'kill thread res={res}')
    if res == 0:
        raise ValueError('nonexistent thread id')
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError('PyThreadState_SetAsyncExc failed')

    while thread.is_alive():
        time.sleep(0.01)
    logger.critical(f'Thread-{thread.ident}({thread.name}) have been killed!')
