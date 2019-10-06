import os
import time
from PIL import Image
from flask import Flask, request, make_response

app = Flask(__name__, static_folder='img/')


@app.route('/')
def index():
    print('hello')
    return 'hello world'


@app.route('/log/<name>')
def read_log(name):
    print(name)
    try:
        resp = make_response(open(os.path.join('log', name)).read())
        resp.headers["Content-type"] = "text/plan;charset=UTF-8"
        return resp
    except e:
        print(f'error {e}')
        return '404 Not Found.'


@app.route('/lastdump')
def last_dump():
    fn = 'img/shot.png'
    print('find dump image')
    if os.path.exists(fn):
        return f'''Last change time  :{time.strftime('%m-%d %H:%M:%S', time.localtime(os.stat(fn).st_ctime))}
        <br>Last modified time:{time.strftime('%m-%d %H:%M:%S', time.localtime(os.stat(fn).st_mtime))}
        <br><img src="shot.png" width="80%"/>'''
    else:
        return 'No dump image found.'


if __name__ == '__main__':
    app.run(port=8080)
