# %%
from battles import Battle, ArgParser
from util.autogui import config, screenshot  # noqas


def start(conf=None):
    parser = ArgParser()
    conf = conf or parser.config
    battle = globals()['battle'] = Battle()
    battle.start(supervise=parser.supervise, conf=conf, force_jump=False)


# %%
if __name__ == '__main__':
    start()
# %%
if __name__ == '__main__':
    start('data/config-jp.json')
