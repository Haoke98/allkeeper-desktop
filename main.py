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
#example  this  is test.

HOME_DIR = os.path.expanduser("~")
APP_HOME_DIR = os.path.join(HOME_DIR, 'all-keeper')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(APP_HOME_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    print('Created log directory: {}'.format(LOG_DIR))


service_pids = []


def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait()  # 等待进程结束
    except psutil.NoSuchProcess:
        print("No such process")


def start_service(namespace: str = "Service", command: list = None):
    # 启动服务进程
    stdout_fp = os.path.join(LOG_DIR, f"{namespace}_stdout.txt")
    stderr_fp = os.path.join(LOG_DIR, f"{namespace}_stderr.txt")
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
            response = requests.get(check_url, proxies={"http": "", "https": ""}, verify=False)
            log = "Checking status of Django server...({}) : {}".format(check_url, response.status_code)
            logs += log + "\n"
            print(log)
            if response.status_code == 200:
                break
        except requests.exceptions.SSLError as e:
            pass
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


def on_window_start(window: webview.Window, dev_mode: bool, lan_access: bool, port: int = 8000):
    # 根据是否允许局域网访问设置host
    host = '0.0.0.0' if lan_access else '127.0.0.1'
    print("Lan Access:", lan_access, "Host:", host)

    if dev_mode:
        manage_script = os.path.join(BASE_DIR, 'service', 'manage.py')
        start_service(namespace="Django",
                      command=[sys.executable,
                               manage_script, 'run_secure',
                               f'{host}:{port}'])
    else:
        if os.name == 'nt':
            print("当前系统是Windows")
            print("CWD:", os.getcwd())
            service_dir = os.path.join(BASE_DIR, "services")
            start_service(namespace="Django",
                          command=[os.path.join(service_dir, 'allkeeper-django.exe'),
                                   'run_secure', f'{host}:{port}', '--noreload'])
        else:
            print("当前系统不是Windows")
            start_service(namespace="Django",
                          command=['./services/allkeeper-django', 'run_secure',
                                   f'{host}:{port}', '--noreload'])

    url = f'https://127.0.0.1:{port}/admin/'
    navigate2after_wait(window, url)


@click.command()
@click.option('--port', default=8000, type=int, help='The port of the Django service')
@click.option('--dev', flag_value=True, default=False, help='Run the service in development mode')
@click.option('--lan', flag_value=True, default=False, help='允许局域网访问')
def main(port, dev, lan):
    # PyWebView 6.x Optimizations
    webview.settings['ALLOW_DOWNLOADS'] = True # 允许文件下载
    webview.settings['ALLOW_FILE_URLS'] = True # 允许加载本地文件 URL
    webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = True # 提升用户体验，外部链接直接在默认浏览器打开
    webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False # 调试模式下自动打开开发者工具
    
    # Enable High DPI support usually handled automatically, but vibrancy adds nice touch on macOS
    window = webview.create_window(
        'All-Keeper', 
        "http://localhost:9080", 
        width=1400, 
        height=1000,
        vibrancy=True, # macOS visual effect
        zoomable=True, # Allow zooming
        text_select=True # Allow text selection
    )
    
    window.events.closed += on_closed
    window.events.closing += on_closing
    window.events.shown += on_shown
    window.events.minimized += on_minimized
    window.events.maximized += on_maximized
    window.events.restored += on_restored
    window.events.resized += on_resized
    window.events.moved += on_moved
    
    # Note: ssl=True in start() enables SSL for the internal server (if used). 
    # Since we use external Django server, this mainly affects local file serving if any.
    webview.start(on_window_start, args=(window, dev, lan, port), ssl=True, debug=dev)
    
    print("Command line arguments (after execute):", sys.argv)
    if dev:
        print("AllKeeperDesktop is now running on development mode !")
    else:
        print("AllKeeperDesktop is now running !")
    if lan:
        print("局域网访问已启用！")


if __name__ == '__main__':
    main()
