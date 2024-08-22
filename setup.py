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
from importlib.metadata import version

from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
from setuptools import setup


def _parse_requirements(file_path):
    # 获取pip的版本
    pip_ver = version('pip')
    pip_version = list(map(int, pip_ver.split('.')[:2]))

    # 根据pip的版本选择不同的方法来解析requirements
    if pip_version >= [20, 0]:  # 这里的版本号需要根据实际情况调整
        requirements = parse_requirements(
            file_path,
            session=PipSession()
        )
    else:
        requirements = parse_requirements(file_path)

    # 返回requirements列表
    return [str(req.requirement) for req in requirements]


def tree(src):
    resp = []
    for (_root, dirs, files) in os.walk(os.path.normpath(src)):
        fps = []
        for f in files:
            fp = os.path.join(_root, f)
            fps.append(fp)
        resp.append((_root, fps))
    return resp


def tree_replace(src_folder, dst_folder):
    resp = []
    for (_root, dirs, files) in os.walk(os.path.normpath(src_folder)):
        fps = []
        for f in files:
            fp = os.path.join(_root, f)
            fps.append(fp)
        resp.append((dst_folder, fps))
    return resp


# parse_requirements() returns generator of pip.req.InstallRequirement objects
try:
    install_reqs = _parse_requirements("requirements.txt")
except Exception:
    logging.warning('Fail load requirements file, so using default ones.')
    install_reqs = []

ENTRY_POINT = ['main.py']

OPTIONS = {
    'argv_emulation': True,
    'strip': True,
    'iconfile': 'cooperation_puzzle_icon_262690.icns',  # uncomment to include an icon
    'includes': ['django', 'webssh'],
    'excludes': ['_pytest', 'pdb', 'unittest', 'doctest'],
    'plist': {
        'CFBundleName': 'AllKeeper',
        'CFBundleDisplayName': 'AllKeeper',
        'CFBundleGetInfoString': "AllKeeper",
        'CFBundleIdentifier': 'com.yourcompany.AllKeeper',
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': 'Copyright © 2023 Your Company. All rights reserved.',
    }
}

setup(
    name="AllKeeper",
    app=ENTRY_POINT,
    packages=['service', ],
    include_package_data=True,
    data_files=[] + tree_replace("dist/services", "services"),
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
