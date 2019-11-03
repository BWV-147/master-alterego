from util.autogui import *
from util.supervisor import supervise_log_time

gacha_logger = get_logger(save=False)


class Gacha:
    def __init__(self, path='img/gacha'):
        self.T = ImageTemplates(path)
        self.LOC = Regions()

    def draw(self):
        wait_which_target(self.T.gacha_initial, self.LOC.drawer_10_initial)
        gacha_logger.info('start gacha...')
        num = 0
        while True:
            num += 1
            print(f'\r{num:<4d}', end='')
            for _ in range(15):
                click(self.LOC.drawer, lapse=0.1)
            shot = screenshot()
            if is_match_target(shot, self.T.gacha_empty, self.LOC.drawer_empty) and \
                    not is_match_target(shot, self.T.gacha_empty, self.LOC.reset_action):
                gacha_logger.warning('no ticket left!')
                return
            page_no = match_which_target(shot, [self.T.gacha_empty, self.T.mailbox_full],
                                         [self.LOC.reset_action, self.LOC.box_full_confirm])
            if page_no == 0:
                click(self.LOC.reset_action)
                gacha_logger.debug(f'{num:<4d} reset.')
                wait_which_target(self.T.reset_confirm, self.LOC.reset_confirm, at=True)
                wait_which_target(self.T.reset_finish, self.LOC.reset_finish, at=True)
                wait_which_target(self.T.gacha_initial, self.LOC.drawer_10_initial)
            elif page_no == 1:
                click(self.LOC.box_full_confirm)
                self.clean_mailbox()

    def clean_mailbox(self, num=40):
        gacha_logger.info('cleaning mailbox...')
        while num > 0:
            num -= 1
            print(f'{num:<4d}\n', end='')
            if num % 10 == 0:
                gacha_logger.debug(f'cleaning {num} left')
            page_no = wait_which_target([self.T.mailbox, self.T.bag_full],
                                        [self.LOC.box_get_all, self.LOC.bag_full_enhance])
            if page_no == 0:
                for loc in self.LOC.box_items:
                    click(loc, lapse=0.10)
                click(self.LOC.box_get_action)
            elif page_no == 1:
                gacha_logger.info('bag full!')
                click(self.LOC.bag_full_enhance)
                break
        click(self.LOC.box_back)


# main entrance
def draw_with_check(check=True):
    check_sys_admin()
    CONFIG.offset_x = 0
    gacha = Gacha()
    time.sleep(2)
    if check:
        t = threading.Thread(target=gacha.draw, name='gacha',
                             args=[], daemon=True)
        supervise_log_time(t, 90, mail=False, interval=3)
    else:
        gacha.draw()


# %%
if __name__ == '__main__':
    draw_with_check(True)
# end
