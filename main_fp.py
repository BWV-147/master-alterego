# %%
from modules.fp_gacha import FpGacha, ArgParser
from util.autogui import config, screenshot  # noqas


def start(conf=None):
    parser = ArgParser()
    conf = conf or parser.config
    fp_gacha = globals()['fp_gacha'] = FpGacha()
    fp_gacha.start(supervise=parser.supervise, conf=conf)


# %%
if __name__ == '__main__':
    start()
# %%
if __name__ == '__main__':
    start('data/config-jp.json')
