# %% make sure correct dpi awareness at startup
from init import initial

initial()
# %%
from util.autogui import *

check_sys_setting(False)
config.load('data/config.json')
config.init_wda()

# %%
base_path: Optional[str] = None


# %%
def capture(fn: str, _base=None):
    # pyautogui.hotkey('alt', 'tab')
    # avoid running template.py directly
    assert (_base or base_path) is not None
    time.sleep(0.1)
    t0 = time.time()
    full_fp = os.path.join(_base or base_path, fn + '.png')
    img = screenshot()
    if os.path.exists(full_fp):
        print(f'! Replace: "{full_fp}"', end='')
    else:
        print(f'   Save  : "{full_fp}" saved', end='')
    print(f'\t\t{time.time() - t0:.4f} sec')
    img.save(full_fp)
    # pyautogui.hotkey('alt', 'tab')


# %%
def save_rewards(quest_name):
    fn = f'img/_drops/{quest_name}/rewards-{quest_name}-{time.strftime("%m%d-%H%M")}.png'
    print(f'Save "{fn}"')
    screenshot().save(fn)


# %% ------------- battle part --------------
capture('quest')
# %%
capture('apple_page')
# %%
capture('apple_confirm')
# %% !!! support/support2
capture('support')
# %%
capture('support_confirm')
# %% !!!
capture('team')
# %% !!!
capture('wave1a')
# %% !!!
capture('skill_targets')
# %% !!!
capture('wave1b')
# %% !!!
capture('cards1')
# %% !!!
capture('wave2a')
# %% !!!
capture('wave2b')
# %% !!!
capture('cards2')
# %% --- order change ----
capture('order_change')
# %% !!!
capture('wave2c')
# %% !!!
capture('wave2d')
# %% !!!
capture('cards2')
# --- end order change ---
# %% !!!
capture('wave3a')
# %% !!!
capture('wave3b')
# %% !!!
capture('cards3')
# %% !!!
capture('kizuna')
# %% !!!
capture('rewards')
# %%
capture('restart_quest')
# %%
capture('apply_friend')
# %%
capture('net_error')
# %% for hunting
capture('bag_full_alert')

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

# %% -------------- lottery part --------------
capture('lottery_initial')
# %%
capture('lottery_empty')
# %%
capture('lottery_reset_confirm')
# %%
capture('lottery_reset_finish')
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
capture('bag_qp_limit')
# %%
capture('shop')
# %%
capture('shop_event_banner_list')
# %%
capture('net_error')

# %% ======== fp gacha ========
capture('gacha_quartz_page')
# %%
capture('gacha_fp_page')
# %%
capture('gacha_fp_confirm')
# %%
capture('gacha_fp_result')
# %%
capture('gacha_fp_bag2_full')
# %%
capture('ce_enhance_empty')
# %%
capture('ce_select_target')
# %%
capture('ce_items_unselected')
# %%
capture('ce_items_selected')
# %%
capture('ce_enhance_page')
# %%
capture('ce_enhance_confirm')
# %%
capture('gacha_fp_bag1_full')
# %%
capture('bag_unselected')
# %%
capture('bag_selected')
# %%
capture('bag_sell_confirm')
# %%
capture('bag_sell_finish')
# %%
capture('menu')
# %%
capture('net_error')
# %%
capture('shop')

# %% test code
pass
