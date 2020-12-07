from init import initialize

initialize()

from . import battle_base
from . import drops_stat
from . import fp_gacha
from . import lottery
from . import master
from . import server

__all__ = [
    'battle_base',
    'drops_stat',
    'fp_gacha',
    'lottery',
    'master',
    'server'
]
