from flask.ext.api import FlaskAPI
import csv
from collections import deque
from flask import request, current_app, abort
from functools import wraps

app = FlaskAPI(__name__)
app.config.from_object('settings')


def token_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-TOKEN', None) != current_app.config['API_TOKEN']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# curl -X POST -H "X-API-TOKEN: FOOBAR1" -H "Content-Type: application/json; charset=utf-8" http://127.0.0.1:5000/predict -d "{\"item\":5,\"num\":2}"
@app.route('/predict', methods=['POST'])
@token_auth
def predict():
    from engines import content_engine
    item = request.data.get('item')
    num_predictions = request.data.get('num', 10)
    if not item:
        return []
    return content_engine.predict(str(item), num_predictions)


# curl -X POST -H "X-API-TOKEN: FOOBAR1" -H "Content-Type: application/json; charset=utf-8" http://127.0.0.1:5000/push -d "{\"content\":\"A big dog\", \"filename\": \"articles.csv\"}"
@app.route('/push', methods=['POST'])
@token_auth
def push():
    from engines import content_engine
    content = request.data.get('content', None)
    filename = request.data.get('filename', None)
    num = 0
    if content:
        with open(filename, 'r') as f:
                try:
                    lastrow = deque(csv.reader(f), 1)[0]
                    num = int(lastrow[0])
                except IndexError:  # empty file
                    lastrow = None
        if num != 0:
            fd = open(filename,'a')
            fd.write("\n{},\"{}\"".format(num+1, content))
            fd.close()
        # content_engine.train(filename)
        return {"message": "Success!", "success": 1}
    return {"message": "Failure", "success": 0}


# curl -X GET -H "X-API-TOKEN: FOOBAR1" -H "Content-Type: application/json; charset=utf-8" http://127.0.0.1:5000/train -d "{\"filename\": \"articles.csv\"}"
@app.route('/train')
@token_auth
def train():
    from engines import content_engine
    filename = request.data.get('filename', None)
    content_engine.train(filename)
    return {"message": "Success", "success": 1}


if __name__ == '__main__':
    app.debug = True
    app.run()
