# %%
from battles import Battle
from util.autogui import config, screenshot, is_interactive_mode, ArgParser  # noqas


def start(cfg=None):
    parser = ArgParser()
    cfg = cfg or parser.config
    battle = globals()['battle'] = Battle()
    battle.start(supervise=parser.supervise, cfg=cfg, force_jump=False)


# %%
if __name__ == '__main__':
    start()
# %%
if __name__ == '__main__' and is_interactive_mode():
    start('data/config-jp.json')
