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
from simplepro.lib import pkHelper
from urllib.parse import urlparse

from ..services.service import Service, BaseAccountModel
from ..devices import ServerNew
from ..net import Net
from ..ip import IPAddress
from ..operation_system import OperationSystem, OperationSystemImage


class Protocol(BaseAccountModel):
    name = models.CharField(max_length=20, verbose_name="协议名称", unique=True)
    default_port = models.PositiveIntegerField(verbose_name="默认端口", null=True, blank=True)
    is_web_protocol = models.BooleanField(verbose_name="是否Web协议", default=False)
    description = models.CharField(max_length=200, verbose_name="描述", null=True, blank=True)

    class Meta:
        verbose_name = "协议"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class ServiceURL(BaseModel):
    """服务入口模型

    一个Service可以有多个入口URL，类似于Platform和URL的关系
    """
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="服务",
                                null=False, blank=False, related_name="urls")
    name = models.CharField(verbose_name="名称", max_length=50, null=True, blank=True)
    protocol = models.ForeignKey(to=Protocol, on_delete=models.PROTECT, verbose_name="协议", null=False, blank=False)
    host = models.CharField(verbose_name="主机", max_length=255, null=False, blank=False)
    port = models.PositiveIntegerField(verbose_name="端口", null=False, blank=False)
    path = models.CharField(verbose_name="路径", max_length=500, null=True, blank=True)
    is_default = models.BooleanField(verbose_name="默认入口", default=False)
    is_dashboard = models.BooleanField(verbose_name="是否面板", default=False)

    class Meta:
        verbose_name = "服务入口"
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-updatedAt']

    def __str__(self):
        return f"{self.service} - {self.name or self.get_full_url()}"

    def get_full_url(self):
        """获取完整的URL"""
        url = f"{self.protocol.name}://{self.host}:{self.port}"
        if self.path:
            url += "/" + self.path
        return url

    def save(self, *args, **kwargs):
        # 如果host是IP地址，自动创建相关资源
        try:
            ip = IPAddress.objects.get(ip=self.host)
            # 如果找到了IP地址，并且服务没有关联操作系统，尝试自动关联
            if ip.device and hasattr(ip.device, 'systems') and not self.service.system:
                systems = ip.device.systems.all()
                if systems.count() == 1:
                    # 如果只有一个操作系统，直接关联
                    self.service.system = systems.first()
                    self.service.save()
        except IPAddress.DoesNotExist:
            # 检查是否是有效的IP地址
            if self.host.replace('.', '').isdigit():
                # 创建网络
                net = Net.objects.create(
                    content=f"{self.host}/32",  # 假设是单个IP地址
                    remark="自动创建的网络"
                )
                # 创建IP地址
                ip = IPAddress.objects.create(
                    ip=self.host,
                    net=net,
                    remark="自动创建的IP地址"
                )
                # 创建服务器
                server = ServerNew.objects.create(
                    remark=f"自动创建服务器-{self.host}"
                )
                # 创建操作系统
                os_image = OperationSystemImage.objects.filter(name="CentOS", version="7").first()
                if os_image:
                    os = OperationSystem.objects.create(
                        server=server,
                        remark="自动创建的操作系统"
                    )
                    # 关联IP到服务器
                    server.ips.add(ip)
                    server.save()
                    # 如果服务没有关联操作系统，关联到新创建的操作系统
                    if not self.service.system:
                        self.service.system = os
                        self.service.save()

        super().save(*args, **kwargs)
