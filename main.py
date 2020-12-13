# %% make sure correct dpi awareness at startup
from init import initialize

initialize()
# %%
from modules.base_agent import BaseAgent
from battles import Battle, start_loop
from modules.fp_gacha import FpGacha
from modules.lottery import Lottery
from util.autogui import config, screenshot, is_interactive_mode  # noqas, for interactive interpreter
from util.base import catch_exception, ArgParser


@catch_exception
def start(action=None, cfg=None):
    """
    Parameters `action` and `cfg` can be overridden
    """
    ArgParser.instance = parser = ArgParser()
    parser.action = ArgParser.override_action or action or parser.action
    parser.config = ArgParser.override_config or cfg or parser.config
    if parser.action == 'battle':
        task = Battle()
    elif parser.action == 'lottery':
        task = Lottery()
    elif parser.action == 'fp':
        task = FpGacha()
    elif parser.action == 'server':
        task = BaseAgent()
    else:
        raise KeyError(f'invalid key: action={parser.action}')
    globals()['task'] = task
    task.start(supervise=parser.supervise, cfg=parser.config)


# %%
if __name__ == '__main__':
    start_loop(lambda: start())
# %%
if __name__ == '__main__' and is_interactive_mode():
    start_loop(lambda: start(cfg='data/config-jp.json'))
