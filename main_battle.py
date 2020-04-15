# %%
from battles import FreeBattle, ArgParser

# %%
if __name__ == '__main__':
    parser = ArgParser()
    conf = parser.config
    # conf = 'data/config-jp.json'
    battle = globals()['battle'] = FreeBattle()
    battle.start(supervise=parser.supervise, conf=conf, force_jump=False)
