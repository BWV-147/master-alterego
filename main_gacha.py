import argparse
import sys

from util.gacha import Gacha

parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-c', '--config', default='data/config.json', help='config file path.')
parser.add_argument('-d', '--disable-supervisor', action='store_false', help='disable supervisor (default enabled).')

if __name__ == '__main__':
    args, _ = parser.parse_known_intermixed_args(sys.argv[1:])
    gacha = globals()['gacha'] = Gacha()
    gacha.start(supervise=not args.disable_supervisor, conf=args.config)
