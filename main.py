# %%
import sys

from battles import Battle
from util.gacha import Gacha


def start_battle():
    battle = Battle()
    globals()['battle'] = battle
    battle.start_with_supervisor(check=True, conf='data/config2.json')


def start_gacha():
    gacha = Gacha()
    globals()['gacha'] = gacha
    gacha.start_with_supervisor(check=True, conf='data/config.json')


# %% main
if __name__ == '__main__':
    if '-g' in sys.argv:
        start_gacha()
    else:
        start_battle()
