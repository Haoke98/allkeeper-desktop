# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/28
@Software: PyCharm
@disc:
======================================="""
import os
import sys

import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Arguments passed:", sys.argv)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
    django.setup()
    execute_from_command_line(sys.argv)
