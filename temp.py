# %%
from pprint import pprint

from util.master import *

sct = mss()
pprint(sct.monitors)


# %%
def generate(base):
    filenames = os.listdir(base)
    for filename in filenames:
        filepath = os.path.join(base, filename)
        if os.path.isfile(filepath) and filename.endswith('.png'):
            key = filename[:-4]
            s = f"""# %%\ncapture('{key}')"""
            s2 = f"""
    @property
    def {key}(self):
        return self.get('{key}')"""
            print(s2)


# %%
base_path = 'img/s-zaxiu-final'  # 'img/gacha'


def capture(fn: str):
    full_fp = os.path.join(base_path, fn + '.png')
    if os.path.exists(full_fp):
        print(f'"{full_fp}" exists, replace it.')
    screenshot().save(full_fp)


# %%
capture('quest')
# %%
capture('apple_page')
# %%
capture('apple_confirm')
# %%
capture('support')
# %%
capture('support_confirm')
# %%
capture('team')
# %%
capture('wave1a')
# %%
capture('wave1b')
# %%
capture('cards1')
# %%
capture('wave2a')
# %%
capture('wave2b')
# %%
capture('order_change')
# %%
capture('cards2')
# %%
capture('wave3a')
# %%
capture('wave3b')
# %%
capture('cards3')
# %%
capture('kizuna')
# %%
capture('rewards')
# %%
capture('restart_quest')
# %%
capture('apply_friend')
# %%
capture('friend_point')
# %%
capture('net_error')

# %% -------------extra parts-------------
capture('cards4')
# %%
capture('cards5')
# %%
capture('cards6')
# %%
capture('cards7')
# %%
capture('cards8')
# %%
capture('cards9')
# %%
capture('wave2c')
# %%
capture('wave2d')

# %% gacha
capture('gacha_initial')
# %%
capture('gacha_empty')
# %%
capture('reset_confirm')
# %%
capture('reset_finish')
# %%
capture('mailbox_full')
# %%
capture('mailbox')
# %%
capture('bag_full')

# %% temp
d = 'img/_drops'
for fn in os.listdir(d):
    if fn.startswith('craft'):
        new_name = fn.replace('craft', 'drops', 1)
        os.rename(os.path.join(d, fn), os.path.join(d, new_name))
        print(f'rename "{fn}" to "{new_name}"')
# end
