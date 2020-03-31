# %%
import argparse
import sys

from modules.fp_gacha import FpGacha

parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-c', '--config', default='data/config.json', help='config file path.')
parser.add_argument('-d', '--disable-supervisor', action='store_false', default=False,
                    help='disable supervisor (default enabled).')
pass

# %%
if __name__ == '__main__':
    args, _ = parser.parse_known_intermixed_args(sys.argv[1:])
    fp_gacha = globals()['fp_gacha'] = FpGacha()
    fp_gacha.start(supervise=not args.disable_supervisor, conf=args.config)
