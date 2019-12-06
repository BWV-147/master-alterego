# %% battle
from battles import *

my_battle = Battle()
my_battle.start_with_supervisor(check=True, conf='data/config.json')

# %% gacha
from util.gacha import Gacha

gacha = Gacha()
gacha.start_with_supervisor(check=True, conf='data/config.json')

# %% main
if __name__ == '__main__':
    pass
