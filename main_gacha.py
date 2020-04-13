# %%
from modules.gacha import Gacha, ArgParser

# %%
if __name__ == '__main__':
    parser = ArgParser()
    conf = parser.config
    # conf = 'data/config-jp.json'
    gacha = globals()['gacha'] = Gacha()
    gacha.start(supervise=parser.supervise, conf=conf)
