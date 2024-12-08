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
from platform import python_build

import click
import psutil
import requests
import webview

HOME_DIR = os.path.expanduser("~")
APP_HOME_DIR = os.path.join(HOME_DIR, 'all-keeper')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(APP_HOME_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    print('Created log directory: {}'.format(LOG_DIR))

# 用于存储webssh进程PID的字典
webssh_pids = {}
service_pids = []


def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait()  # 等待进程结束
    except psutil.NoSuchProcess:
        print("No such process")


def start_service(namespace: str = "WebSSH_Service", command: list = None):
    # 启动服务进程
    stdout_fp = os.path.join(LOG_DIR, f"{namespace}_stdout.txt")
    stderr_fp = os.path.join(LOG_DIR, f"{namespace}_stderr.txt")
    # 请根据实际情况替换webssh命令和参数
    with open(stdout_fp, "w") as stdout_f, open(stderr_fp, "w") as stderr_f:
        process = subprocess.Popen(command, stdout=stdout_f, stderr=stderr_f, text=True)
        pidPF = os.path.join(APP_HOME_DIR, f"{namespace}.pid")
        with open(pidPF, "w") as pid_f:
            pid_f.write(str(process.pid))
        print(f"{namespace} Service Started ... PID: {process.pid}, stdout: {stdout_f}, stderr: {stderr_f}")
        service_pids.append(process.pid)


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
    logs = ""
    while True:
        try:
            check_url = url
            response = requests.get(check_url, proxies={"http": "", "https": ""})
            log = "Checking status of Django server...({}) : {}".format(check_url, response.status_code)
            logs += log + "\n"
            print(log)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError as e:
            log = "Checking status of Django server...({}) : {}".format(url, e)
            logs += log + "\n"
            print(log)

        time.sleep(1)  # 每隔1秒检查一次
        tDlt = time.time() - start_time
        window.load_html(
            '<h1>Service is dynamically loaded!</h1><h2> loading ..... ({:0.2f} s)</h2><pre>{}</pre>'.format(tDlt,
                                                                                                             logs))
        print(f"Loading {url}...  ({tDlt} s)")

    print(f"Loading {url} after {time.time() - start_time} seconds.")
    window.load_url(url)


def on_closed():
    for pid in service_pids:
        kill_process(pid)
    print('pywebview window is closed')


def on_closing():
    print('pywebview window is closing')


def on_shown():
    print('pywebview window shown')


def on_minimized():
    print('pywebview window minimized')


def on_restored():
    print('pywebview window restored')


def on_maximized():
    print('pywebview window maximized')


def on_resized(width, height):
    print(
        'pywebview window is resized. new dimensions are {width} x {height}'.format(
            width=width, height=height
        )
    )


def on_moved(x, y):
    print('pywebview window is moved. new coordinates are x: {x}, y: {y}'.format(x=x, y=y))


def on_window_start(window: webview.Window, dev_mode: bool):
    port = 8000
    if dev_mode:
        start_service(namespace="WebSSH", command=['wssh', f'--port=9080', '--xsrf=False'])
        # FIXME: 这里的Python可执行文件的绝对位置得改成自动获取
        manage_script = os.path.join(BASE_DIR, 'service', 'manage.py')
        start_service(namespace="Django", command=[f'/Users/shadikesadamu/anaconda3/envs/django_async_admin/bin/python', manage_script, 'runserver', f'127.0.0.1:{port}'])
    else:
        # 检查操作系统是否为Windows
        if os.name == 'nt':
            print("当前系统是Windows")
            print("CWD:", os.getcwd())
            service_dir = os.path.join(BASE_DIR, "services")
            start_service(namespace="WebSSH",
                          command=[os.path.join(service_dir, 'wssh.exe'), f'--port=9080', '--xsrf=False'])
            start_service(namespace="Django",
                          command=[os.path.join(service_dir, 'allkeeper-django.exe'), 'runserver', f'127.0.0.1:{port}',
                                   '--noreload'])
        else:
            print("当前系统不是Windows")
            start_service(namespace="WebSSH", command=['./services/wssh', f'--port=9080', '--xsrf=False'])
            start_service(namespace="Django",
                          command=['./services/allkeeper-django', 'runserver', f'127.0.0.1:{port}', '--noreload'])
    url = f'http://127.0.0.1:{port}/admin/'
    navigate2after_wait(window, url)


@click.command()
@click.option('--port', default=8000, type=int, help='The port of the Django service')
# @click.option('--dev', default=False, type=bool, help='The port of the Django service')
@click.option('--dev', flag_value=True, default=False, help='Run the service in development mode')
def main(port, dev):
    window = webview.create_window('All-Keeper', "http://localhost:9080", width=1400, height=1000)
    window.events.closed += on_closed
    window.events.closing += on_closing
    window.events.shown += on_shown
    window.events.minimized += on_minimized
    window.events.maximized += on_maximized
    window.events.restored += on_restored
    window.events.resized += on_resized
    window.events.moved += on_moved
    webview.start(on_window_start, args=(window, dev), ssl=True)
    print("Command line arguments (after execute):", sys.argv)
    if dev:
        print("AllKeeperDesktop is now running on development mode !")
    else:
        print("AllKeeperDesktop is now running !")


if __name__ == '__main__':
    main()
