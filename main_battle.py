# %%
import argparse
import sys

from battles import FreeBattle

parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('-c', '--config', default='data/config.json', help='config file path.')
parser.add_argument('-d', '--disable-supervisor', action='store_true',
                    help='disable supervisor (default enabled).')
pass

# %%
if __name__ == '__main__':
    args, _ = parser.parse_known_intermixed_args(sys.argv[1:])
    battle = globals()['battle'] = FreeBattle()
    supervise = True  # args.disable_supervisor
    conf = 'data/config-jp.json' or args.config
    # conf = 'data/config.json' or args.config
    battle.start(supervise=supervise, conf=conf)
