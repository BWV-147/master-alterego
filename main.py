# %% make sure correct dpi awareness at startup
from init import initialize

initialize()
# %%
from modules.base_agent import BaseAgent
from battles import Battle, start_loop
from modules.fp_gacha import FpGacha
from modules.lottery import Lottery
from util.autogui import config, screenshot, is_interactive_mode, ArgParser  # noqas, for interactive interpreter


def start(cfg=None):
    parser = ArgParser()
    cfg = cfg or parser.config
    if parser.task == 'battle':
        task = Battle()
    elif parser.task == 'lottery':
        task = Lottery()
    elif parser.task == 'fp':
        task = FpGacha()
    elif parser.task == 'server':
        task = BaseAgent()
    else:
        raise KeyError
    globals()['task'] = task
    task.start(supervise=parser.supervise, cfg=cfg)


# %%
if __name__ == '__main__':
    start_loop(lambda cfg=None: start(cfg))
# %%
if __name__ == '__main__' and is_interactive_mode():
    start_loop(lambda: start('data/config-jp.json'))
