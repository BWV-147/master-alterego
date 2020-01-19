from battles import Battle

globals()['battle'] = battle = Battle()
battle.start_with_supervisor(check=True, conf='data/config.json')
