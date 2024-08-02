# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel

from ..operation_system import OperationSystem


class SystemUser(BaseModel):
    id = models.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator)
    owner = models.CharField(verbose_name="使用者", max_length=50, null=True, blank=True)
    username = fields.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    password = fields.PasswordInputField(max_length=32, null=True, blank=False, verbose_name="密码", size="medium",
                                         style="width:600px;", pattern="123456789,.asdfgzxcvbnm")
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)
    system = models.ForeignKey(to=OperationSystem, on_delete=models.CASCADE, verbose_name="操作系统", null=True,
                               blank=False, db_index=True, related_name="users")
    userGroup = (
        (0, "root:x:0:"),
        (1, "bin:x:1:"),
        (2, "daemon:x:2:"),
        (3, "sys:x:3:"),
        (4, "adm:x:4:"),
        (5, "tty:x:5:"),
        (6, "disk:x:6:"),
        (7, "lp:x:7:"),
        (8, "mem:x:8:"),
        (9, "kmem:x:9:"),
        (10, "wheel:x:10:"),
        (11, "cdrom:x:11:"),
        (12, "mail:x:12:postfix"),
        (13, "man:x:15:"),
        (14, "dialout:x:18:"),
        (15, "floppy:x:19:"),
        (16, "games:x:20:"),
        (17, "tape:x:33:"))
    group = fields.IntegerField(verbose_name='用户组', choices=userGroup, null=True, blank=True)

    class Meta:
        verbose_name = "系统用户"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['system', 'username'], name="unique_judge_by_system")
        ]

    def __str__(self):
        res = f"{self.system}/{self.id}"
        if self.owner:
            res += " - " + self.owner
        return res
