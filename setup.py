# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/8
@Software: PyCharm
@disc:
======================================="""
import os

from setuptools import setup


def tree(src):
    resp = []
    for (_root, dirs, files) in os.walk(os.path.normpath(src)):
        fps = []
        for f in files:
            fp = os.path.join(_root, f)
            fps.append(fp)
        resp.append((_root, fps))
    return resp


ENTRY_POINT = ['main.py']

DATA_FILES = tree('common-static') + tree('utils')
OPTIONS = {
    'argv_emulation': False,
    'strip': True,
    # 'iconfile': 'icon.icns', # uncomment to include an icon
    'includes': ['WebKit', 'Foundation', 'webview'],
}

setup(
    name="AllKeeper",
    app=ENTRY_POINT,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)