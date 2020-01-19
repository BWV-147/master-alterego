# %%
from util.master import *

check_sys_admin()

# %%
base_path = 'img/gacha'  # 'img/gacha-jp'


# %%
def capture(fn: str):
    time.sleep(1)
    full_fp = os.path.join(base_path, fn + '.png')
    if os.path.exists(full_fp):
        print(f'! Replace: "{full_fp}"')
    else:
        print(f'   Saved : "{full_fp}" saved')
    screenshot().save(full_fp)
    pyautogui.hotkey('alt', 'tab')


# %%
def save_rewards(quest_name):
    screenshot().save(f'img/_drops/rewards-{quest_name}-{time.strftime("%m%d-%H%M")}.png')


# %% ------------- battle part --------------
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
# %% --- order change ----
capture('order_change')
# %%
capture('wave2c')
# %%
capture('wave2d')
# --- end order change ---
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

# %% ---------- battle extra parts ----------
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

# %% -------------- gacha part --------------
capture('gacha_initial')
# %%
capture('gacha_empty')
# %%
capture('gacha_reset_confirm')
# %%
capture('gacha_reset_finish')
# %%
capture('mailbox_full_alert')
# %% sliver card ×1
capture('mailbox_unselected1')
# %% sliver card ×2
capture('mailbox_unselected2')
# %%
capture('mailbox_selected')
# %%
capture('bag_full_alert')
# %%
capture('bag_unselected')
# %%
capture('bag_selected')
# %%
capture('bag_sell_confirm')
# %%
capture('bag_sell_finish')
# %%
capture('shop')
# %%
capture('shop_event_banner_list')
# %%
capture('net_error')

# %% debug during battle
from battles import *

config.load_config('data/config.json')
check_sys_admin()
BaseConfig.task_finished = False
BaseConfig.log_file = 'logs/log.full.log'
# _battle: Battle = globals()['battle']
_battle = Battle()
getattr(_battle, config.battle_func)(True)
master = _battle.master
T = master.T
LOC = master.LOC
# start debugging
print(master.quest_name)
# end debug
