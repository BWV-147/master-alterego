from battle import *

glog = get_logger(save=False)


class Gacha:

    def __init__(self, path='img/gacha'):
        self.T = ImageTemplates(path)
        self.LOC = Regions()

    def draw(self):
        wait_which_target(self.T.get('gacha_initial'), self.LOC.drawer_10_initial)
        glog.info('start gacha...')
        num = 0
        whole_time = 0
        clock = Timer().start()
        while True:
            num += 1
            print(f'\r{num:<4d}', end='')
            click(self.LOC.drawer, lapse=0.1)
            shot = screenshot()
            if match_which_target(shot, self.T.get('gacha_empty'), self.LOC.drawer_empty) >= 0 and \
                    match_which_target(shot, self.T.get('gacha_empty'), self.LOC.reset_action) == -1:
                glog.warning('no ticket left!')
                return
            page_no = match_which_target(shot, [self.T.get('gacha_initial'), self.T.get('mailbox_full')],
                                         [self.LOC.reset_action, self.LOC.box_full_confirm])
            if page_no == 0:
                click(self.LOC.reset_action)
                _all_lapse = clock.lapse()
                whole_time += _all_lapse
                print('\n')
                glog.log(f'{num:<4d} reset: t={_all_lapse - whole_time:>3d}/{_all_lapse:<5d}\n', end='')
                wait_which_target(self.T.get('reset_confirm'), self.LOC.reset_confirm, at=True)
                wait_which_target(self.T.get('reset_finish'), self.LOC.reset_finish, at=True)
                wait_which_target(self.T.get('gacha_initial'), self.LOC.drawer_10_initial)
            elif page_no == 1:
                click(self.LOC.box_full_confirm)
                self.mailbox()
                return

    def mailbox(self, num=70):
        glog.info('cleaning mailbox...')
        while num > 0:
            num -= 1
            print(f'\r{num:<4d} ', end='')
            page_no = wait_which_target([self.T.get('mailbox'), self.T.get('bag_full')],
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
    Config.offset_x = -1920
    check_sys_admin()
    test = Gacha()
    time.sleep(2)
    if check:
        t1 = threading.Thread(target=test.draw, name='gacha',
                              args=[], daemon=True)
        supervise_log_time(t1, 120, mail=False, interval=3)
    else:
        pass
        test.draw()


# %%
if __name__ == '__main__':
    draw_with_check()


# %% backup
def get_center(pos):
    assert isinstance(pos, (list, tuple))
    if len(pos) == 2:
        return pos[0] + Config.offset_x, pos[1] + Config.offset_y
    elif len(pos) == 4:
        return (pos[0] + pos[2]) / 2 + Config.offset_x, (pos[1] + pos[3]) / 2 + Config.offset_y

# end
