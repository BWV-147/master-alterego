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
import imghdr
import json
import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler

from PIL import Image
from flask import Flask, request, Response, redirect, jsonify, abort, send_from_directory

ROOT = os.getcwd()
if ROOT.endswith('modules'):
    # if server.py is run directly, cwd is "root/modules"
    ROOT = os.path.dirname(ROOT)
    os.chdir(ROOT)
    print(f'Change working directory to: {ROOT}')
if os.path.normpath(ROOT) not in [os.path.normpath(p) for p in sys.path]:
    sys.path.insert(0, ROOT)

# after add project root to paths, import will work normally
from util.config import config
from util.autogui import screenshot, compress_image

app = Flask('flask.app', root_path=os.path.join(ROOT, 'www'), static_folder='/', static_url_path='/')

# app.logger has default StreamHandler
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.addHandler(logging.StreamHandler())
_log_folder = os.path.join(ROOT, 'logs')
if not os.path.exists(_log_folder):
    os.mkdir(_log_folder)
for _logger in (werkzeug_logger, app.logger):  # type:logging.Logger
    _logger.setLevel(logging.DEBUG)
    fh = RotatingFileHandler(os.path.join(_log_folder, f'{_logger.name}.log'),
                             encoding='utf8', maxBytes=1024 * 1024, backupCount=2)
    fh.setFormatter(logging.Formatter(
        style='{',
        datefmt="%m-%d %H:%M:%S",
        fmt='{asctime} - {filename}[line:{lineno:>3d}] - {levelname:<5s}: [{threadName}] {message}'))
    _logger.addHandler(fh)


@app.route('/')
def index():
    return redirect('/html/index.html')


@app.route('/favicon.ico')
def favicon():
    return redirect('https://img.icons8.com/ultraviolet/40/000000/binoculars.png')


@app.route('/getId')
def get_id():
    return config.id


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
    for dir_path, dir_names, filenames in os.walk(img_folder):
        key = os.path.relpath(os.path.realpath(dir_path), img_folder)
        if key == '.':
            key = ''
        key = key.strip('\\/').replace('/', '\\')
        tree[key] = {'files': sorted(filenames, reverse='_drops' in key), 'folders': sorted(dir_names)}
    return jsonify(tree)


@app.route('/getFile')
def get_file():
    """Return text file or Image(compressed)"""
    filepath = request.args.get('path')
    monitor = request.args.get('mon')
    if monitor is None or monitor == '' or monitor.lower() == 'null':
        monitor = config.monitor
    else:
        monitor = int(monitor)
    if filepath.lower() == 'screenshot':
        image = screenshot(monitor=monitor)
    else:
        filepath = os.path.join('img', filepath)
        if not os.path.isfile(filepath):
            return abort(404)
        elif imghdr.what(filepath):
            image = Image.open(filepath)
        else:
            return send_from_directory('.', filepath)
    return Response(compress_image(image).getvalue(), mimetype="image/jpeg")


@app.route('/getTaskStatus')
def get_task_status():
    return repr(config.task_thread)


@app.route('/shutdownTask')
def shutdown_task():
    """Shutdown running task."""
    from util.addon import kill_thread
    force = request.args.get('force')
    if config.task_thread is threading.main_thread() and config.task_thread.is_alive():
        if force == '1':
            kill_thread(config.task_thread)
            # actually, won't return since server is killed.
            return f'Task has been terminated. Thread: {config.task_thread}'
        else:
            return 'Task run in main thread, check force stop to terminate it.'
    elif config.task_thread and config.task_thread.is_alive():
        kill_thread(config.task_thread)
        return f'Task has been terminated. Thread: {config.task_thread}'
    else:
        return f'No running task. Thread: {config.task_thread}'


@app.route('/putNewTask')
def put_new_task():
    if config.task_thread and config.task_thread.is_alive():
        return f'Task is still alive: {config.task_thread}'
    elif config.task_queue.full():
        return f'Task already in queue. Try or check again later.'
    else:
        config.task_queue.put_nowait(1)
        app.logger.info('put a new task to queue')
        return f'Put a task into queue, check it later'


@app.route('/toggleVisibility')
def toggle_visibility():
    import pyautogui as pag
    if config.is_wda:
        return 'invalid request for WDA', 403
    else:
        pag.hotkey(*config.hide_hotkey)
        return f'Toggle visibility: {config.hide_hotkey}'


@app.route('/switchTab')
def switch_tab():
    import pyautogui as pag
    if config.is_wda:
        return 'Invalid request for WDA', 403
    else:
        pag.hotkey(*config.switch_tab_hotkey)
        return f'Switch Tab: {config.switch_tab_hotkey}'


@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    if request.method == 'GET':
        return json.dumps(config.to_json(), ensure_ascii=False)
    else:
        # don't directly save to config file, since there may be errors.
        data = request.get_data().decode('utf8')
        config.from_json(json.loads(data))
        config.save()
        return json.dumps(config.to_json(), ensure_ascii=False)


# %%
if __name__ == '__main__':
    from util.base import check_sys_setting

    # from util.config import config

    config.load()
    check_sys_setting(False)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int)
    _port = parser.parse_known_intermixed_args()[0].port
    # debug mode must run in main thread and in terminal rather interactive interpreter
    app.debug = False
    app.run('0.0.0.0', _port)
