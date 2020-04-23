"""
A simple server to review logs/img and screenshot.

To expose to public network, the following oprations are needed.
 - add firewall rules
 - if there's no public network address, consider using "port mapping" on NAT device which has public address
   or NAT traversal tools(e.g. ngrok) to expose local web server.

On windows, host="::" ony bind ipv6, and host="0.0.0.0" only bind ipv4.
"""
__all__ = ['run_server']

import argparse
import io
import os
import sys

from PIL import Image
from flask import Flask, request, Response, redirect, jsonify

from util.autogui import screenshot
from util.gui import check_sys_admin

check_sys_admin()
root = os.getcwd()
filename = os.path.split(os.path.realpath(__file__))[1]
if root.endswith('modules') and filename == 'server.py':
    # if server.py is run directly, cwd is "root/modules"
    root = os.path.dirname(root)
    os.chdir(root)
    sys.path.append(root)
    print(f'Change working directory to: {root}')
app = Flask(__name__, root_path=f'{root}/www', static_folder=os.path.join(root, 'www'), static_url_path='/')


@app.route('/')
def index():
    return 'hello world'


@app.route('/favicon.ico')
def favicon():
    return redirect('https://img.icons8.com/ultraviolet/40/000000/binoculars.png')


@app.route('/getLogList')
def get_log_list():
    log_dir = 'logs'
    filenames = [f for f in os.listdir(log_dir) if f.endswith('.log')]
    return jsonify(filenames)


@app.route('/getRecentLog')
def get_recent_log():
    log_name = request.args.get('name', 'log.log')
    log_num = request.args.get('num', 1000, type=int)
    if log_num <= 0:
        log_num = 1000
    fp = os.path.join('logs', log_name)
    if not os.path.exists(fp):
        return ''
    with open(fp, 'r', encoding='utf8') as fd:
        lines = fd.readlines()
        text = ''.join(lines[-min(len(lines), log_num):])
    return text


def compress_image(image: Image.Image, scale=0.75, quality=60):
    """compress image to io buffer"""
    buffer = io.BytesIO()
    img = image.resize((int(image.width * scale), int(image.height * scale)))
    img.save(buffer, format='jpeg', quality=quality)
    return buffer


@app.route('/getImageFolderTree')
def get_image_folder_tree():
    tree = {}
    img_folder = os.path.join(root, 'img')
    start = os.path.realpath('.')
    for dirpath, dirnames, filenames in os.walk(img_folder):
        key = os.path.relpath(os.path.realpath(dirpath), start)
        key = key.strip('\\/').replace('/', '\\')
        tree[key] = {'files': sorted(filenames, reverse='_drops' in key), 'folders': sorted(dirnames)}
    return jsonify(tree)


@app.route('/getImage')
def get_image():
    filepath = request.args.get('path')
    if filepath == 'screenshot':
        image = screenshot()
    elif not os.path.exists(filepath):
        return Response('404 Not found.', 404)
    else:
        image = Image.open(filepath)
    return Response(compress_image(image).getvalue(), mimetype="image/jpeg")


def run_server(port=8080):
    app.run(host='0.0.0.0', port=port, debug=False)


# %%
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int)
    _port = parser.parse_known_intermixed_args()[0].port
    run_server(_port)
