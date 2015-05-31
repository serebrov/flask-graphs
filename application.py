from functools import wraps
import simplejson as json
import traceback

from flask import Flask
from flask import jsonify
from flask import request

import database

app = Flask(__name__)
app.debug = True


def print_exceptions(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception, e:
            print ''
            print '------'
            print 'API: exception'
            print e
            print traceback.format_exc()
            print request.url
            print request.data
            print '------'
            raise
    return wrapped


@app.route('/')
def hello_world():
    return jsonify({'data': 'Hello World!'})


@app.route("/data", methods=["POST"])
@print_exceptions
def post_data():
    data = json.loads(request.data)
    for item in data:
        database.put(item)
    return jsonify({'result': 'OK'})


@app.route("/data", methods=["GET"])
@print_exceptions
def get_data():
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    result = database.find_if(
        lambda item:
            (not start or (start and item['ts'] >= int(start))) and
            (not end or (end and item['ts'] <= int(end)))
    )
    return jsonify(result)


if __name__ == '__main__':
    player1 = {
        'player': 'Nick', 'floor': 'Ground',
        'position': {'x': 0, 'y': 0}, 'ts': 100
    }
    player2 = {
        'player': 'Ken', 'floor': 'TowerTop',
        'position': {'x': 100, 'y': 50}, 'ts': 200
    }
    database.put(player1)
    database.put(player2)
    app.run()
