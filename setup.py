# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/8
@Software: PyCharm
@disc:
======================================="""

from setuptools import setup

from utils import tree

ENTRY_POINT = ['main.py']

DATA_FILES = tree('service')
OPTIONS = {
    'argv_emulation': False,
    'strip': True,
    'iconfile': 'cooperation_puzzle_icon_262690.icns',  # uncomment to include an icon
    'includes': ['WebKit', 'Foundation', 'webview'],
}

setup(
    name="AllKeeper",
    app=ENTRY_POINT,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
