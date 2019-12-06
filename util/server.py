import html
import io
import math
import os
import re
import sys
import time

from PIL import Image
from flask import Flask, request, Response

PROJECT_NAME = 'master-alterego'
project_dir = os.path.join(os.getcwd().split(sep=PROJECT_NAME)[0], PROJECT_NAME)
print(f'Project dir: {project_dir}')
os.chdir(project_dir)
print(f'cwd: {os.getcwd()}\n')

# change cwd before import custom packages
from util.autogui import screenshot

app = Flask(__name__, static_folder=os.path.join(project_dir, 'img'), static_url_path='/static')


@app.route('/')
def index():
    return 'hello world'


@app.route('/pages')
def pages():
    page_names = ['logs', 'drops', 'screenshot']
    return '\n'.join([f'<li><a href="/{p}">{p}</a></li>' for p in page_names])


@app.route('/screenshot')
def get_screenshot():
    img: Image.Image = screenshot()
    img_file = io.BytesIO()
    img.resize((1920 // 2, 1080 // 2)).save(img_file, format='jpeg', quality=40)
    resp = Response(img_file.getvalue(), mimetype="image/jpeg")
    return resp


@app.route('/logs')
def logs():
    log_dir = 'logs'
    lines = []
    for f in os.listdir(os.path.join(project_dir, log_dir)):
        if not f.startswith('.') and os.path.isfile(os.path.join(project_dir, log_dir, f)):
            lines.append(f'<li><a href="/log/{f}">{f}</a></li>')
    return f'Back to <a href="/pages">pages</a><br>' \
           f'Logs:<br>' \
           f'{"".join(lines)}'


@app.route('/log/<log_name>')
def show_log(log_name):
    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 50, type=int)
    log_fp = os.path.join(project_dir, 'logs', log_name)
    if not os.path.exists(log_fp):
        return f'404. No such log "{log_name}".'
    try:
        with open(log_fp, encoding='utf8') as fd:
            all_log = fd.readlines()
            num = len(all_log)
            page_num = math.ceil(num / size)
            page = min(page_num - 1, page)
            start = max(-num, -(page + 1) * size)
            end = -page * size
            if end == 0:
                end = None
            records = [f'<p>{html.escape(r)}</p>' for r in all_log[start:end]]
        page_link_html = '&nbsp;&nbsp;'.join(
            [f'<a href="/log/{log_name}?page={i}&size={size}">{i}</a>' for i in range(min(page_num, 20))])
        resp = f'Back to <a href="/logs">logs</a><br>' \
               f'Recent logs: Page {page}, {size} logs per page.<br>' \
               f'{page_link_html}<hr>' \
               f'<div>{"".join(records)}</div>' \
               f'<hr>{page_link_html}'
        return resp
    except Exception as e:
        print(f'error {e}')
        return f'Error reading log "{log_name}".\n{e}'


@app.route('/drops')
def drops():
    drops_dir = 'img/_drops'
    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 50, type=int)
    filter_drop = request.args.get('drop', 0, type=int)
    lines = []
    img_files = os.listdir(os.path.join(project_dir, drops_dir))
    img_files = [f for f in img_files if os.path.isfile(os.path.join(project_dir, drops_dir, f))]
    img_files.sort(key=lambda f: (re.findall(r'-([\d\-]+)[^\-\d]', f) or [''])[0], reverse=True)
    page_num = math.ceil(len(img_files) / size)
    page = min(page_num - 1, page)
    page_links = [f'&nbsp<a href="/drops?page={i}&size={size}">{i}</a>&nbsp;' for i in range(page_num)]
    page_link_html = f'&nbsp<a href="/drops?drop=1">drop</a>&nbsp;{" ".join(page_links)}'
    if filter_drop:
        start = 0
        lines = [f'<li><a href="/drop/{f}">{f}</a></li>' for f in img_files if 'drop' in f]
    else:
        start = page * size
        end = min((page + 1) * size, len(img_files))
        for i in range(start, end):
            f = img_files[i]
            if not f.startswith('.'):
                lines.append(f'<li><a href="/drop/{f}">{f}</a></li>')
    return f'Back to <a href="/pages">pages</a><br>' \
           f'Page: {"drops" if filter_drop else page}<br>' \
           f'{page_link_html}<hr>' \
           f'<ol start="{start}">{chr(10).join(lines)}</ol>' \
           f'<hr>{page_link_html}'


@app.route('/drop/<img_name>')
def show_drop_img(img_name):
    print(f'access drop img: {img_name}')
    drop_dir = 'img/_drops'
    try:
        img: Image.Image = Image.open(os.path.join(project_dir, drop_dir, img_name))
        img_file = io.BytesIO()
        img.resize((1920 // 2, 1080 // 2)).save(img_file, format='jpeg', quality=40)
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


def run_server(port=8080):
    app.run(host='::', port=port)


if __name__ == '__main__':
    if len(sys.argv) > 1 and str(sys.argv[1]).isdigit():
        _port = int(sys.argv[1])
    else:
        _port = 8080
    run_server(_port)
