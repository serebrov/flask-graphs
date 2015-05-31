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
            print request.form
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


@app.route("/data", methods=["GET"])
@print_exceptions
def get_data(**kwargs):
    start = kwargs['start'] if 'start' in kwargs else None
    end = kwargs['end'] if 'end' in kwargs else None
    database.find_if(
        lambda item:
            (not start or (start and item['ts'] >= start)) and
            (not end or (end and item['ts'] <= end))
    )


if __name__ == '__main__':
    app.run()
