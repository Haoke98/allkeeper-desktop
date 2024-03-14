# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/14
@Software: PyCharm
@disc:
======================================="""
import subprocess

import click
import webview

# 用于存储webssh进程PID的字典
webssh_pids = {}


def start_webssh(session_name):
    # 启动webssh进程
    webssh_command = ['wssh', '--port=9080', '--xsrf=False']  # 请根据实际情况替换webssh命令和参数
    process = subprocess.Popen(webssh_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 获取并记录PID
    webssh_pids[session_name] = process.pid
    # TODO: 写入到文件中进行持久化记录
    print(f"Started webssh for session '{session_name}'. PID: {process.pid}")


@click.command()
def main():
    start_webssh('default')
    webview.create_window('All-Keeper', 'http://127.0.0.1:8001/bupt2018213267@Sdm98/', width=1400, height=1000)
    webview.start()


if __name__ == '__main__':
    main()
