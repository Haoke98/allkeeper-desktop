# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
from simplepro.components import fields

from .server import ServerNew


class Router(ServerNew):

    class Meta:
        verbose_name = "路由器"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.remark:
            return f"路由器({self.remark})"
        return f"路由器({self.id})"
