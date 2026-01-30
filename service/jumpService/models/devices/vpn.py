# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2026/01/30
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from .server import ServerNew


class VPNDevice(ServerNew):

    class Meta:
        verbose_name = "VPN设备"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.remark:
            return f"VPN设备({self.remark})"
        if self.code:
            return f"VPN设备({self.code})"
        return f"VPN设备({self.id})"
