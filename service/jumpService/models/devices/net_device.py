# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/8
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.models import BaseModel
from simplepro.components import fields

from .device import Device


class NetDevice(Device):
    """
    默认当所有的网络设备基本上都是单用户
    """
    mac = models.CharField(max_length=17, verbose_name="MAC地址", blank=True, null=True)
    webControlAddress = fields.CharField(slot_text="URL", slot="prepend", max_length=255, verbose_name="WEB管理页面访问地址",
                                    style="width:600px;",blank=True, null=True)
    webControlUsername = fields.CharField(max_length=32,verbose_name="管理员用户名", blank=True, null=True)
    webControlPassword = fields.PasswordInputField(max_length=32, verbose_name="管理页密码", blank=True, null=True)

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 获取所有子类模型
        for related_object in self._meta.related_objects:
            if related_object.one_to_one and related_object.field.remote_field.parent_link:
                try:
                    concrete_instance = getattr(self, related_object.name)
                    if concrete_instance:
                        return str(concrete_instance)
                except related_object.related_model.DoesNotExist:
                    continue

        # 如果没有找到子类实例，使用默认的字符串格式
        if self.remark:
            return f"网络设备({self.id},{self.remark})"
        return f"网络设备({self.id})"


class Port(BaseModel):
    host = fields.ForeignKey(to=NetDevice, on_delete=models.CASCADE, related_name="ports")
    num = fields.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['host', 'num'], name='unique_host_port')
        ]
        verbose_name = "端口"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.host}:{str(self.num)}"
