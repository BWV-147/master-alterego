# %% make sure correct dpi awareness at startup
from init import initialize

initialize()

# %%
from util.autogui import *

if __name__ == '__main__' and not is_interactive_mode():
    raise EnvironmentError("Don't run script directly")

config.load('data/config.json')
config.initialize(False)

# %%
import util.template_util as template_util
from util.template_util import capture

template_util.base_path = 'img/battles/s-egg'

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
capture('rewards_init')
# %% !!!
capture('rewards')
# %%
capture('apply_friend')
# %%
capture('restart_quest')
# %% for hunting
capture('bag_full_alert')
# %% for exceptions
capture('net_error')
# %%
capture('login_news')
# %%
capture('login_popup')
# %%
capture('login_terminal')

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

# %% ======== fp gacha ========
capture('gacha_quartz_page')
# %%
capture('gacha_fp_page')
# %%
capture('gacha_fp_confirm')
# %%
capture('gacha_fp_result')
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
capture('gacha_fp_svt_full')
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
