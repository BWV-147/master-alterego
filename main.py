# %%
import sys

from battles import Battle
from util.gacha import Gacha


def start_battle():
    globals()['battle'] = battle = Battle()
    battle.start_with_supervisor(check=True, conf='data/config.json')


def start_gacha():
    globals()['gacha'] = gacha = Gacha()
    gacha.start_with_supervisor(check=True, conf='data/config.json')


# %% main
if __name__ == '__main__':
    if '-g' in sys.argv:
        start_gacha()
    else:
        start_battle()
