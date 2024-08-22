# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/8/22
@Software: PyCharm
@disc:
======================================="""
import sys
from webssh import main

if __name__ == "__main__":
    # 将命令行参数添加到sys.argv中，以模拟命令行调用
    print("Sys.Argv:", sys.argv)
    # 调用webssh模块的主函数
    main.main()
