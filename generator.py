import time
import random
import requests
import database


def generate(local=False):
    count = 10000
    players = ['Nick', 'Mike', 'Ben', 'Ken', 'Jane', 'Kelly', 'Jack', 'Alex']
    floors = [
        'Underground', 'Ground', 'Fist', 'Second',
        'TowerGround', 'TowerFirst', 'TowerSecond', 'TowerTop'
    ]

    ts_now = int(time.time())
    ts_2015_01_01 = 1420070400
    data = []

    for i in range(0, count):
        item = {
            'player': random.choice(players),
            'floor': random.choice(floors),
            'position': {
                'x': random.randint(0, 100),
                'y': random.randint(0, 300)
            },
            'ts': random.randint(ts_2015_01_01, ts_now)
        }
        if local:
            database.put(item)
        else:
            data.append(item)

    if not local:
        return requests.post("http://localhost:5000/data", json=data)


if __name__ == '__main__':
    resp = generate()
    print resp.text
