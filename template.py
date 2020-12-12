# %% make sure correct dpi awareness at startup
from init import initialize

initialize()

# %%
from util.autogui import *
import matplotlib.pyplot as plt

if __name__ == '__main__' and not is_interactive_mode():
    raise EnvironmentError("Don't run the script directly")

config.load('data/config.json')
config.initialize(False)

# %%
base_path: Optional[str] = None


# %%
def capture(fn: str = None, _base: str = None):
    # pyautogui.hotkey('alt', 'tab')
    _base = _base or base_path
    if not os.path.exists(_base):
        os.makedirs(_base)
        print(f'make dir: {_base}')
    time.sleep(0.1)
    t0 = time.time()
    img = screenshot()
    plt.figure('screenshot')
    plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.show()
    if fn and _base is not None:
        full_fp = os.path.join(_base or base_path, fn + '.png')
        if os.path.exists(full_fp):
            print(f'! Replace: "{full_fp}"', end='')
        else:
            print(f'   Save  : "{full_fp}" saved', end='')
        print(f'\t\t{time.time() - t0:.4f} sec')
        img.save(full_fp)
    # pyautogui.hotkey('alt', 'tab')


def save_rewards(quest_name: str = None, drop: int = None):
    plt.figure('rewards')
    img = screenshot()
    if quest_name:
        fn = f'img/_drops/{quest_name}/rewards-{quest_name}-{time.strftime("%m%d-%H%M")}'
        fn = fn + (f'-drop{drop}.png' if drop else '.png')
        print(f'Save "{fn}"')
        img.save(fn)
    plt.show()


def compare(fp1, fp2, region, dx=0, dy=0, dw=0, dh=0):
    plt.figure('compare', clear=True)
    m1 = Image.open(fp1)
    m2 = Image.open(fp2)
    plt.subplot(1, 2, 1)
    plt.imshow(m1.crop(region))
    plt.subplot(1, 2, 2)
    region2 = [region[0] + dx, region[1] + dy, region[2] + dx + dw, region[3] + dy + dh]
    plt.imshow(m2.crop(region2))
    print(f'{region}\n{tuple(region2)}')
    plt.show()


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
capture('skill_targets')
# %% !!!
capture('svt_status_window')
# %% !!!
capture('wave1a')
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
# %%-
capture('gacha_fp_svt_full')
# %%-
capture('gacha_fp_ce_full')
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
