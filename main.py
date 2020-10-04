# %% make sure correct dpi awareness at startup
from init import initial

initial()
# %%
from battles import Battle, start_loop
from modules.fp_gacha import FpGacha
from modules.lottery import Lottery
from util.autogui import config, screenshot, is_interactive_mode, ArgParser  # noqas, for interactive interpreter


def start(cfg=None):
    parser = ArgParser()
    cfg = cfg or parser.config
    if parser.task == 'battle':
        task = globals()['battle'] = Battle()
    elif parser.task == 'lottery':
        task = globals()['lottery'] = Lottery()
    elif parser.task == 'fp':
        task = globals()['fp_gacha'] = FpGacha()
    else:
        raise KeyError
    task.start(supervise=parser.supervise, cfg=cfg)


# %%
if __name__ == '__main__':
    start_loop(lambda: start())
# %%
if __name__ == '__main__' and is_interactive_mode():
    start_loop(lambda: start('data/config-jp.json'))
