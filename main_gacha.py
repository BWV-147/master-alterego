from util.gacha import Gacha

globals()['gacha'] = gacha = Gacha()
gacha.start_with_supervisor(check=True, conf='data/config.json')
