from functools import wraps
import simplejson as json
import traceback
import datetime
from collections import defaultdict

from flask import Flask
from flask import jsonify
from flask import request

import database
import generator

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
    return jsonify({'result': 'OK', 'len': len(data)})


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
    return jsonify({'data': result})


@app.route("/data/count", methods=["GET"])
@print_exceptions
def get_data_count():
    data = database.find_if(lambda item: True)
    result = defaultdict(int)
    for item in data:
        ts_datetime = datetime.datetime.utcfromtimestamp(item['ts'])
        result[str(ts_datetime.date())] += 1
    return jsonify({'data': result})


if __name__ == '__main__':
    generator.generate(local=True)
    app.run()
