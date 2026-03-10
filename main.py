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

try:
    if sys.platform == 'darwin':
        import AppKit
except ImportError:
    pass
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


def on_loaded(window):
    # Inject JS patch for handling Django Admin popups (e.g. ForeignKey add button)
    # This simulates window.open behavior using an iframe modal, enabling window.opener communication
    # Updated to handle SimpleUI iframes and avoid null reference errors
    js_popup_patch = r"""
    (function() {
        // Function to patch a specific window instance
        function patchWindow(targetWindow) {
            if (!targetWindow) return;
            try {
                // Check access (same-origin check)
                const _ = targetWindow.location.href;
                if (targetWindow.pywebview_popup_patch_injected) return;
            } catch (e) { return; }

            targetWindow.pywebview_popup_patch_injected = true;
            console.log('PyWebView Popup Patch Injected for:', targetWindow.location.href);

            const originalOpen = targetWindow.open;
            targetWindow.open = function(url, name, specs) {
                console.log('Intercepted window.open:', url, name, specs);
                const urlString = String(url);
                
                // Check for Django Admin popup indicators
                // Django admin popups usually have '_popup=1' in query string
                // name can be 'RelatedObjectLookups' or 'id_field_name'
                if ((urlString && urlString.includes('_popup=1')) || name === 'RelatedObjectLookups' || (specs && specs.includes('resizable'))) {
                    // Use top window for modal to ensure it covers everything visually
                    const topDoc = window.top.document;
                    
                    const modal = topDoc.createElement('div');
                    Object.assign(modal.style, {
                        position: 'fixed', top: '0', left: '0', width: '100%', height: '100%',
                        backgroundColor: 'rgba(0,0,0,0.5)', zIndex: '99999',
                        display: 'flex', justifyContent: 'center', alignItems: 'center'
                    });
                    
                    const iframe = topDoc.createElement('iframe');
                    iframe.src = urlString;
                    Object.assign(iframe.style, {
                        width: '90%', height: '90%', backgroundColor: 'white',
                        border: 'none', borderRadius: '5px', boxShadow: '0 0 10px rgba(0,0,0,0.5)'
                    });
                    
                    const closeBtn = topDoc.createElement('button');
                    closeBtn.textContent = '×';
                    Object.assign(closeBtn.style, {
                        position: 'absolute', top: '20px', right: '20px',
                        fontSize: '24px', background: 'none', border: 'none',
                        color: 'white', cursor: 'pointer', fontWeight: 'bold'
                    });
                    
                    // Mock window object to return immediately
                    // This prevents "null is not an object" error when calling win.focus()
                    const mockWindow = {
                        focus: function() { console.log('Mock window focused'); },
                        close: function() { if(modal.parentNode) modal.parentNode.removeChild(modal); },
                        closed: false
                    };

                    closeBtn.onclick = function() { 
                        mockWindow.close();
                    };
                    
                    modal.appendChild(iframe);
                    modal.appendChild(closeBtn);
                    topDoc.body.appendChild(modal);
                    
                    // Setup opener relationship when iframe loads
                    iframe.onload = function() {
                        try {
                            const childWin = iframe.contentWindow;
                            // CRITICAL: The opener must be the window that called open()
                            // In this closure, 'targetWindow' is the window being patched (e.g. the iframe window)
                            childWin.opener = targetWindow; 
                            childWin.originalClose = childWin.close;
                            childWin.close = function() {
                                mockWindow.close();
                            };
                            // Also patch the new popup window itself, just in case it opens more popups
                            patchWindow(childWin);
                        } catch (e) { console.error('Cannot access iframe content:', e); }
                    };
                    
                    return mockWindow;
                }
                return originalOpen.apply(targetWindow, arguments);
            };
        }

        // 1. Patch top window
        patchWindow(window);

        // 2. Helper to process iframes
        function processIframes(rootNode) {
            const iframes = rootNode.getElementsByTagName('iframe');
            for (let i = 0; i < iframes.length; i++) {
                const iframe = iframes[i];
                try {
                    // Try to patch immediately
                    patchWindow(iframe.contentWindow);
                    // Also listen for load (for dynamic src changes)
                    iframe.addEventListener('load', function() {
                        patchWindow(this.contentWindow);
                    });
                } catch(e) {}
            }
        }

        // Process existing iframes
        processIframes(document);

        // 3. Observe for new iframes (MutationObserver)
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                for (let i = 0; i < mutation.addedNodes.length; i++) {
                    const node = mutation.addedNodes[i];
                    if (node.tagName === 'IFRAME') {
                        node.addEventListener('load', function() {
                            patchWindow(this.contentWindow);
                        });
                    } else if (node.getElementsByTagName) {
                        // Check if added node contains iframes
                        processIframes(node);
                    }
                }
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    })();
    """
    window.evaluate_js(js_popup_patch)


def on_window_start(window: webview.Window, dev_mode: bool, lan_access: bool, port: int = 8000):
    # Set dock icon on macOS
    if sys.platform == 'darwin' and 'AppKit' in sys.modules:
        icon_path = os.path.join(BASE_DIR, 'allkeeper.icns')
        if os.path.exists(icon_path):
            image = AppKit.NSImage.alloc().initByReferencingFile_(icon_path)
            if image:
                AppKit.NSApplication.sharedApplication().setApplicationIconImage_(image)

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
    
    # Determine icon path for window
    icon_file = None
    if sys.platform == 'darwin':
        p = os.path.join(BASE_DIR, 'allkeeper.icns')
        if os.path.exists(p):
            icon_file = p
    elif sys.platform == 'win32' or os.name == 'nt':
        p = os.path.join(BASE_DIR, 'allkeeper.ico')
        if os.path.exists(p):
            icon_file = p

    # Enable High DPI support usually handled automatically, but vibrancy adds nice touch on macOS
    window = webview.create_window(
        'All-Keeper', 
        "http://localhost:9080", 
        width=1400, 
        height=1000,
        vibrancy=True, # macOS visual effect
        zoomable=True, # Allow zooming
        text_select=True, # Allow text selection
    )
    
    window.events.closed += on_closed
    window.events.closing += on_closing
    window.events.shown += on_shown
    window.events.minimized += on_minimized
    window.events.maximized += on_maximized
    window.events.restored += on_restored
    window.events.resized += on_resized
    window.events.moved += on_moved
    window.events.loaded += on_loaded
    
    # Note: ssl=True in start() enables SSL for the internal server (if used). 
    # Since we use external Django server, this mainly affects local file serving if any.
    webview.start(on_window_start, args=(window, dev, lan, port), ssl=True, debug=dev, icon=icon_file)
    
    print("Command line arguments (after execute):", sys.argv)
    if dev:
        print("AllKeeperDesktop is now running on development mode !")
    else:
        print("AllKeeperDesktop is now running !")
    if lan:
        print("局域网访问已启用！")


if __name__ == '__main__':
    main()
