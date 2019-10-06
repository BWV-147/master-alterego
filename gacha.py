from battle import *

glog = get_logger(save=False)


def get_center(pos):
    assert isinstance(pos, (list, tuple))
    if len(pos) == 2:
        return pos[0] + G.get('offset_x', 0), pos[1] + G.get('offset_y', 0)
    elif len(pos) == 4:
        return (pos[0] + pos[2]) / 2 + G.get('offset_x', 0), (pos[1] + pos[3]) / 2 + G.get('offset_y', 0)


class Gacha:

    def __init__(self):
        self.T = ImageTemplates('img/gacha')
        self.LOC = Regions()

    def draw(self):
        wait_which_target(self.T.get('gacha_initial'), self.LOC.drawer_10_initial)
        glog.info('start gacha...')
        num = 0
        while True:
            num += 1
            print(f'\r{num:<4d} ', end='')
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
                glog.info('reset')
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


# %%
G['offset_x'] = -1920
time.sleep(2)
test = Gacha()
test.draw()

