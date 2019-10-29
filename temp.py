# %%
from pprint import pprint
from mss import mss
import os
from util.image_process import screenshot
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
# base_path = 'img/a-zaxiu-ass'
base_path = 'img/gacha'


def capture(fn: str):
    full_fp = os.path.join(base_path, fn + '.png')
    if os.path.exists(full_fp):
        print(f'"{full_fp}" exists, replace it.')
    screenshot().save(full_fp)


# generate(base)
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
capture('wave2c')
# %%
capture('wave2d')
# %%
capture('cards4')
# %%
capture('wave3a')
# %%
capture('wave3b')
# %%
capture('cards3')
# %%
capture('cards4')
# %%
capture('cards5')
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
# %% pickling
import json

app_dir = "C:/Apps/of/apps/MD_visual 2/bin/data/atom_data"
for fn in os.listdir(app_dir):
    fp = os.path.join(app_dir, fn)
    if fp.endswith('.json'):
        obj = json.load(open(fp, 'r'))
        json.dump(obj, open("C:/Apps/of/apps/MD_visual 2/bin/data/atom_data2/" + fn, 'w'), ensure_ascii=False, indent=2)
        print('converted ' + fp)

# %%
