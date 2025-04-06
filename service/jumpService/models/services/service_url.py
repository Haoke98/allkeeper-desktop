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
from simplepro.models import BaseModel

from ..services.service import Service, BaseAccountModel


class ServiceURL(BaseModel):
    """服务入口URL模型

    一个Service可以有多个入口URL，类似于Platform和URL的关系
    """
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="服务",
                                null=False, blank=False, related_name="urls")
    name = models.CharField(verbose_name="名称", max_length=50, null=True, blank=True)
    url = models.URLField(verbose_name="访问地址", null=False, blank=False)
    is_default = models.BooleanField(verbose_name="默认入口", default=False)

    class Meta:
        verbose_name = "服务入口"
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-updatedAt']

    def __str__(self):
        return f"{self.service} - {self.name or self.url}"