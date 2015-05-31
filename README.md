Simple python+flask API demo and d3/c3 data visualization.

Clone and do the setup:

```bash
mkvirtualenv flask-graphs
pip install -r requirements.txt
```

Run an app:

```bash
python application.py
```

Open API app: http://localhost:5000/static/index.html.
Or access API directly:

- data - http://localhost:5000/data
- count - http://localhost:5000/data/count
- heatmap - http://localhost:5000/data/heatmap

When application is started it generates 10000 test data records.
Under the hood it uses super-simple in-memory database to store data, so if you re-start an app the data is lost.
To add more data - run `python generator.py` or POST data to /data endpoint:

```bash
curl -H "Content-Type: application/json" --data '[{
    "player": "Jack",
    "floor": "Ground",
    "position": {
        "x": 5,
        "y": 7
    },
    "ts": 1420070450
}]' http://localhost:5000/data
```
