# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/14
@Software: PyCharm
@disc:
======================================="""
import os
import subprocess
import sys
import threading
import time

import click
import requests
import webview

HOME_DIR = os.path.expanduser("~")
APP_HOME_DIR = os.path.join(HOME_DIR, 'all-keeper')

LOG_DIR = os.path.join(APP_HOME_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    print('Created log directory: {}'.format(LOG_DIR))

# 用于存储webssh进程PID的字典
webssh_pids = {}


def start_service(namespace: str = "WebSSH_Service", command: list = None):
    # 启动服务进程
    stdout_fp = os.path.join(LOG_DIR, f"{namespace}_stdout.txt")
    stderr_fp = os.path.join(LOG_DIR, f"{namespace}_stderr.txt")
    # 请根据实际情况替换webssh命令和参数
    with open(stdout_fp, "w") as stdout_f, open(stderr_fp, "w") as stderr_f:
        process = subprocess.Popen(command, stdout=stdout_f, stderr=stderr_f, text=True)
        print(f"{namespace} Service Started ... PID: {process.pid}, stdout: {stdout_f}, stderr: {stderr_f}")


def check_django_status(target: str):
    try:
        response = requests.get(target)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    return False


def navigate_after_delay(window: webview.Window, url, delay):
    def navigate():
        time.sleep(delay)
        print(f"Loading {url}...")
        window.load_url(url)

    th = threading.Thread(target=navigate)
    th.daemon = True
    th.start()
    print(f"Loading {url} after {delay} seconds.")


def navigate2after_wait(window: webview.Window, url):
    start_time = time.time()
    while not check_django_status(target=url):
        time.sleep(1)  # 每隔1秒检查一次
        print(f"Loading {url}...  ({time.time()-start_time} s)")

    print(f"Loading {url} after {time.time()-start_time} seconds.")
    window.load_url(url)


def on_window_start(window: webview.Window):
    port = 8000
    start_service(namespace="WebSSH", command=['./services/wssh', f'--port=9080', '--xsrf=False'])
    start_service(namespace="Django",
                  command=['./services/allkeeper-django', 'runserver', f'0.0.0.0:{port}', '--noreload'])
    url = f'http://127.0.0.1:{port}/bupt2018213267@Sdm98/'
    navigate2after_wait(window, url)


@click.command()
@click.option('--port', default=8000, type=int, help='The port of the Django service')
def main(port):
    window = webview.create_window('All-Keeper', "http://localhost:9080", width=1400, height=1000)
    webview.start(on_window_start, args=(window,), ssl=True, debug=True)
    print("Command line arguments (after execute):", sys.argv)
    print("AllKeeperDesktop is now running!")


if __name__ == '__main__':
    main()
