# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/14
@Software: PyCharm
@disc:
======================================="""
import multiprocessing
import os
import subprocess
import sys
import threading
import time

from flask_socketio import SocketIO
from flask import Flask, render_template

import click
import django
import webview

from proj.settings import BASE_DIR

LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    print('Created log directory: {}'.format(LOG_DIR))
# 用于存储webssh进程PID的字典
webssh_pids = {}
app = Flask(__name__)
socketio = SocketIO(app)


# @app.route('/')
# def index():
#     return render_template('index.html')
# @socketio.on('connect', namespace='/output')
# def handle_connect():
#     thread = threading.Thread(target=stream_output, args=(request.namespace, ))
#     thread.start()

def start_service(namespace: str = "WebSSH_Service", command: list = None):
    # 启动服务进程
    stdout_fp = os.path.join(LOG_DIR, f"{namespace}_stdout.txt")
    stderr_fp = os.path.join(LOG_DIR, f"{namespace}_stderr.txt")
    # 请根据实际情况替换webssh命令和参数
    with open(stdout_fp, "w") as stdout_f, open(stderr_fp, "w") as stderr_f:
        process = subprocess.Popen(command, stdout=stdout_f, stderr=stderr_f, text=True)
        print(f"{namespace} Service Started ... PID: {process.pid}")

    # 获取并记录PID
    # webssh_pids[namespace] = process.pid
    # # TODO: 写入到文件中进行持久化记录
    # for line in iter(process.stdout.readline, ''):
    #     socketio.emit('output', line, namespace=namespace)


def start_django(port: int, namespace: str = "django_service"):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    print("Command line arguments:", sys.argv)
    django_args = ['manage.py', 'runserver', str(port)]
    print("Django arguments:", django_args)
    django.setup()
    execute_from_command_line(django_args)


def start_webview(port: int):
    url = f'http://127.0.0.1:{port}/bupt2018213267@Sdm98/'
    print(f"Starting webview...{url}")
    webview.create_window('All-Keeper', url, width=1400, height=1000)
    webview.start(debug=True)


@click.command()
@click.option('--port', default=8000, type=int, help='The port of the Django service')
def main(port):
    start_service(namespace="WebSSH", command=['wssh', '--port=9080', '--xsrf=False'])
    start_service(namespace="Django", command=['python', 'manage.py', 'runserver', f'0.0.0.0:{port}'])
    time.sleep(5)
    start_webview(port)
    print("Command line arguments (after execute):", sys.argv)
    print("AllKeeperDesktop is now running!")


if __name__ == '__main__':
    main()
