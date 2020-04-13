# %%
from modules.fp_gacha import FpGacha, ArgParser

# %%
if __name__ == '__main__':
    parser = ArgParser()
    conf = parser.config
    # conf = 'data/config-jp.json'
    fp_gacha = globals()['fp_gacha'] = FpGacha()
    fp_gacha.start(supervise=parser.supervise, conf=conf)
