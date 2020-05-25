# %%
from modules.lottery import Lottery
from util.autogui import config, screenshot, is_interactive_mode, ArgParser  # noqas


def start(cfg=None):
    parser = ArgParser()
    cfg = cfg or parser.config
    lottery = globals()['lottery'] = Lottery()
    lottery.start(supervise=parser.supervise, cfg=cfg)


# %%
if __name__ == '__main__':
    start()
# %%
if __name__ == '__main__' and is_interactive_mode():
    start('data/config-jp.json')
