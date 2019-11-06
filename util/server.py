import io
import os
import time

from PIL import Image
from flask import Flask, make_response, Response

PROJECT_NAME = 'master-alterego'
project_dir = os.path.join(os.getcwd().split(sep=PROJECT_NAME)[0], PROJECT_NAME)
print(f'Project dir: {project_dir}')

app = Flask(__name__, static_folder=os.path.join(project_dir, 'img'), static_url_path='/static')


@app.route('/')
def index():
    print('hello')
    return 'hello world'


@app.route('/logs')
def logs():
    lines = []
    for f in os.listdir(os.path.join(project_dir, 'logs')):
        if not f.startswith('.'):
            lines.append(f'<li><a href="/log/{f}">{f}</a></li>')
    return '\n'.join(lines)


@app.route('/log/<log_name>')
def show_log(log_name):
    print(log_name)
    try:
        with open(os.path.join(project_dir, 'logs', log_name)) as fd:
            lines = fd.readlines()
            n = len(lines)
            recent_records = lines[n + 1 - min(50, n):n + 1]
        resp = make_response(f'recent logs(max 50 records):\n{chr(10).join(recent_records)}')
        resp.headers["Content-type"] = "text/plan;charset=UTF-8"
        return resp
    except Exception as e:
        print(f'error {e}')
        return f'"{log_name}" Not Found.\n{e}'


@app.route('/drops')
def drops():
    lines = []
    for f in os.listdir(os.path.join(project_dir, 'img/_drops')):
        if not f.startswith('.'):
            lines.append(f'<li><a href="/drop/{f}">{f}</a></li>')
    lines.sort(reverse=True)
    return '\n'.join(lines)


@app.route('/drop/<img_name>')
def show_drop_img(img_name):
    print(f'access drop img: {img_name}')
    drop_dir = 'img/_drops'
    img: Image.Image = Image.open(os.path.join(project_dir, drop_dir, img_name))
    img_file = io.BytesIO()
    img.resize((1920 // 2, 1080 // 2)).save(img_file, format='jpeg', quality=40)
    try:
        resp = Response(img_file.getvalue(), mimetype="image/jpeg")
        return resp
    except Exception as e:
        print(f'error {e}')
        return f'"{img_name}" Not Found.\n{e}'


@app.route('/last_crash')
def last_crash():
    fn = os.path.join(project_dir, 'img/crash.jpg')
    if os.path.exists(fn):
        return f'''Last change time  :{time.strftime('%m-%d %H:%M:%S', time.localtime(os.stat(fn).st_ctime))}
        <br>Last modified time:{time.strftime('%m-%d %H:%M:%S', time.localtime(os.stat(fn).st_mtime))}
        <br><img src="static/crash.jpg"/>'''
    else:
        return 'No dump image found.'


if __name__ == '__main__':
    app.run(port=8080)
