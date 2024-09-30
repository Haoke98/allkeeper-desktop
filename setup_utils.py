# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/9/30
@Software: PyCharm
@disc:
======================================="""
import os
import re

from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements


# 从version.txt读取并解析版本信息
def parse_version_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式提取版本信息
    file_version_match = re.search(r'FileVersion\', u\'([0-9.]+)\'', content)
    product_version_match = re.search(r'ProductVersion\', u\'([0-9.]+)\'', content)
    copyright_match = re.search(r'LegalCopyright\', u\'(.*?)\'', content)

    file_version = file_version_match.group(1) if file_version_match else None
    product_version = product_version_match.group(1) if product_version_match else None
    copyright_text = copyright_match.group(1) if copyright_match else None

    return file_version, product_version, copyright_text


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
