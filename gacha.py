from battle import *

glog = get_logger(save=False)


class Gacha:

    def __init__(self, path='img/gacha'):
        self.T = ImageTemplates(path)
        self.LOC = Regions()

    def draw(self):
        wait_which_target(self.T.gacha_initial, self.LOC.drawer_10_initial)
        glog.info('start gacha...')
        num = 0
        while True:
            num += 1
            print(f'\r{num:<4d}', end='')
            for _ in range(15):
                click(self.LOC.drawer, lapse=0.1)
            shot = screenshot()
            if match_which_target(shot, self.T.gacha_empty, self.LOC.drawer_empty) >= 0 and \
                    match_which_target(shot, self.T.gacha_empty, self.LOC.reset_action) == -1:
                glog.warning('no ticket left!')
                return
            page_no = match_which_target(shot, [self.T.gacha_empty, self.T.mailbox_full],
                                         [self.LOC.reset_action, self.LOC.box_full_confirm])
            if page_no == 0:
                click(self.LOC.reset_action)
                glog.debug(f'{num:<4d} reset.')
                wait_which_target(self.T.reset_confirm, self.LOC.reset_confirm, at=True)
                wait_which_target(self.T.reset_finish, self.LOC.reset_finish, at=True)
                wait_which_target(self.T.gacha_initial, self.LOC.drawer_10_initial)
            elif page_no == 1:
                click(self.LOC.box_full_confirm)
                self.mailbox()

    def mailbox(self, num=40):
        glog.info('cleaning mailbox...')
        while num > 0:
            num -= 1
            print(f'{num:<4d}\n', end='')
            if num % 10 == 0:
                glog.debug(f'cleaning {num} left')
            page_no = wait_which_target([self.T.mailbox, self.T.bag_full],
                                        [self.LOC.box_get_all, self.LOC.bag_full_enhance])
            if page_no == 0:
                for loc in self.LOC.box_items:
                    click(loc, lapse=0.10)
                click(self.LOC.box_get_action)
            elif page_no == 1:
                glog.info('bag full!')
                click(self.LOC.bag_full_enhance)
                break
        click(self.LOC.box_back)


# main entrance
def draw_with_check(check=True):
    Config.offset_x = 0
    check_sys_admin()
    gacha = Gacha()
    time.sleep(2)
    if check:
        t1 = threading.Thread(target=gacha.draw, name='gacha',
                              args=[], daemon=True)
        supervise_log_time(t1, 90, mail=False, interval=3)
    else:
        gacha.draw()


# %%
if __name__ == '__main__':
    draw_with_check(True)


# %% backup
def get_center(pos):
    assert isinstance(pos, (list, tuple))
    if len(pos) == 2:
        return pos[0] + Config.offset_x, pos[1] + Config.offset_y
    elif len(pos) == 4:
        return (pos[0] + pos[2]) / 2 + Config.offset_x, (pos[1] + pos[3]) / 2 + Config.offset_y

# end
