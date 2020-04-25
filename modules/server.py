"""
A simple server to review logs/img and screenshot.

To expose to public network, the following operations are needed.
 - add firewall rules
 - if there's no public network address, consider using "port mapping" on NAT device which has public address
   or NAT traversal tools(e.g. ngrok) to expose local web server.

On windows, host="::" ony bind ipv6, and host="0.0.0.0" only bind ipv4.
"""
__all__ = ['app']

import argparse
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from PIL import Image
from flask import Flask, request, Response, redirect, jsonify

from util.autogui import screenshot, compress_image
from util.log import LOG_FORMATTER


def get_root_path():
    _root = os.getcwd()
    if _root.endswith('modules'):
        # if server.py is run directly, cwd is "root/modules"
        _root = os.path.dirname(_root)
        os.chdir(_root)
        sys.path.append(_root)
        print(f'Change working directory to: {_root}')
    return _root


def config_server_logger(flask_app):
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addHandler(logging.StreamHandler())
    for _logger in (werkzeug_logger, flask_app.logger):  # type:logging.Logger
        _logger.setLevel(logging.DEBUG)
        fh = RotatingFileHandler(os.path.join(ROOT, 'logs', f'{_logger.name}.log'),
                                 encoding='utf8', maxBytes=1024 * 1024, backupCount=2)
        fh.setFormatter(LOG_FORMATTER)
        _logger.addHandler(fh)


def create_app():
    www_root = os.path.join(ROOT, 'www')
    _app = Flask('flask.app', root_path=www_root, static_folder='/', static_url_path='/')
    config_server_logger(_app)
    return _app


ROOT = get_root_path()
app = create_app()


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
    return Response(text, mimetype='text/plain')


@app.route('/getImageFolderTree')
def get_image_folder_tree():
    tree = {}
    img_folder = os.path.join(ROOT, 'img')
    start = os.path.realpath('.')
    for dir_path, dir_names, filenames in os.walk(img_folder):
        key = os.path.relpath(os.path.realpath(dir_path), start)
        key = key.strip('\\/').replace('/', '\\')
        tree[key] = {'files': sorted(filenames, reverse='_drops' in key), 'folders': sorted(dir_names)}
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
    return Response(compress_image(image, 0.75).getvalue(), mimetype="image/jpeg")


# %%
if __name__ == '__main__':
    from util.addon import check_sys_setting
    from util.config import config

    config.load()
    check_sys_setting(False)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int)
    _port = parser.parse_known_intermixed_args()[0].port
    # debug mode must run in main thread and in terminal rather interactive interpreter
    app.debug = False
    app.run('0.0.0.0', _port)
