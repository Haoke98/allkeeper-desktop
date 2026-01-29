# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/11
@Software: PyCharm
@disc:
======================================="""
from django.db import models
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel

from .devices import ServerNew


class OperationSystemImage(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, editable=False, default=pkHelper.uuid_generator)

    # Basic OS Info
    name = fields.CharField(max_length=50, verbose_name="系统分类",
                            placeholder="例如: Ubuntu, CentOS, Windows, MacOS")
    series = fields.CharField(max_length=50, verbose_name="系列",
                              placeholder="例如: Windows 10, CentOS 7, Ubuntu 24.04",
                              null=True)
    version = fields.CharField(max_length=50, verbose_name="版本号",
                               placeholder="例如: 22H2, 7, 24.04")

    # Additional Version Info
    build_number = fields.CharField(max_length=50, verbose_name="内部版本号",
                                    placeholder="例如: 19045.5011, 3.10.0-1160.108.1.el7.x86_64",
                                    null=True, blank=True)
    code_name = fields.CharField(max_length=50, verbose_name="版本代号",
                                 placeholder="例如: Noble Numbat, Core",
                                 null=True, blank=True)

    # System Architecture
    arch = fields.CharField(max_length=50, verbose_name="架构",
                            placeholder="例如: x86_64, amd64, arm64",
                            null=True, blank=True)

    # LTS Status
    isLTS = models.BooleanField(default=False, verbose_name="LTS")

    # Installation Media
    iso = models.FileField(verbose_name="安装镜像", upload_to='system_images',
                           null=True, blank=True)

    class Meta:
        verbose_name = "操作系统镜像"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'series', 'version', 'build_number', 'arch'],
                name="operation_system_unique"
            )
        ]

    def __str__(self):
        components = [self.name]
        if self.series:
            components.append(self.series)
        if self.version:
            components.append(self.version)
        if self.build_number:
            components.append(f"({self.build_number})")
        if self.arch:
            components.append(f"[{self.arch}]")
        return " ".join(components)


class OperationSystem(BaseModel):
    image = fields.ForeignKey(to=OperationSystemImage, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name="系统镜像")
    server = fields.ForeignKey(to=ServerNew, on_delete=models.CASCADE, null=True, blank=False, verbose_name="服务器",
                               related_name="systems")
    remoteAccessPort = models.PositiveSmallIntegerField(verbose_name="远程登录/控制/访问端口", blank=True, null=True)

    class Meta:
        verbose_name = "操作系统"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.server}/{self.image}"
