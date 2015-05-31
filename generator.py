import time
import random
import requests
import simplejson as json

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
    data.append({
        'player': random.choice(players),
        'floor': random.choice(floors),
        'position': {
            'x': random.randint(0, 100),
            'y': random.randint(0, 300)
        },
        'ts': random.randint(ts_2015_01_01, ts_now)
    })

headers = {'Content-type': 'application/json'}
resp = requests.post("http://localhost:5000/data", json=data)
print resp.text
