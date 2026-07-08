# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/8
@Software: PyCharm
@disc:
======================================="""
import logging

from setuptools import setup

from setup_utils import parse_version_file, _parse_requirements, tree_replace

# 获取版本信息
file_version, product_version, copyright_text = parse_version_file('version.txt')
print("File version({}): {}".format(type(file_version), file_version))
print("Product version({}): {}".format(type(product_version), product_version))
print("Copyright text({}): {}".format(type(copyright_text), copyright_text))

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
    'iconfile': 'AccessPodKeyHub.icns',  # 桌面应用图标
    'includes': ['django', 'webssh'],
    'excludes': ['_pytest', 'pdb', 'unittest', 'doctest'],
    'plist': {
        'CFBundleName': 'AccessPod+KeyHub',
        'CFBundleDisplayName': 'AccessPod+KeyHub',
        'CFBundleGetInfoString': "AccessPod+KeyHub",
        'CFBundleIdentifier': 'com.0p.AccessPodKeyHub',
        'CFBundleVersion': file_version,  # 使用从 version.txt 中解析的 FileVersion
        'CFBundleShortVersionString': product_version,  # 使用从 version.txt 中解析的 ProductVersion
        'NSHumanReadableCopyright': copyright_text,  # 使用从 version.txt 中解析的版权信息
    }
}

setup(
    name="AccessPodKeyHub",
    app=ENTRY_POINT,
    packages=['service', ],
    include_package_data=True,
    data_files=[] + tree_replace("services", "services"),
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
