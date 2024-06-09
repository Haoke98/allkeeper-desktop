# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/8
@Software: PyCharm
@disc:
======================================="""
import logging
import os

import pip
import pkg_resources
from setuptools import setup
from setuptools.config.expand import find_packages


def _parse_requirements(file_path):
    pip_ver = pkg_resources.get_distribution('pip').version
    pip_version = list(map(int, pip_ver.split('.')[:2]))
    if pip_version >= [6, 0]:
        raw = pip.req.parse_requirements(file_path,
                                         session=pip.download.PipSession())
    else:
        raw = pip.req.parse_requirements(file_path)
    return [str(i.req) for i in raw]


def tree(src):
    resp = []
    for (_root, dirs, files) in os.walk(os.path.normpath(src)):
        fps = []
        for f in files:
            fp = os.path.join(_root, f)
            fps.append(fp)
        resp.append((_root, fps))
    return resp


# parse_requirements() returns generator of pip.req.InstallRequirement objects
try:
    install_reqs = _parse_requirements("requirements.txt")
except Exception:
    logging.warning('Fail load requirements file, so using default ones.')
    install_reqs = []

ENTRY_POINT = ['main.py']

DATA_FILES = tree('service') + tree('assets')
OPTIONS = {
    'argv_emulation': False,
    'strip': True,
    'iconfile': 'cooperation_puzzle_icon_262690.icns',  # uncomment to include an icon
    'includes': ['WebKit', 'Foundation', 'webview', 'elasticsearch', 'django'],
}

setup(
    name="AllKeeper",
    app=ENTRY_POINT,
    packages=['service', 'assets'],
    install_requires=install_reqs,
    include_package_data=True,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
