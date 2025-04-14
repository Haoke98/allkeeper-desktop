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

    一个Service可以有多个入口URL，支持IP形式和域名形式
    IP形式：host(IP) + 端口 + 路径
    域名形式：domain + 路径
    """
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="服务",
                              null=False, blank=False, related_name="urls")
    name = models.CharField(verbose_name="名称", max_length=50, null=True, blank=True)
    protocol = models.ForeignKey(to=Protocol, on_delete=models.PROTECT, verbose_name="协议", null=False, blank=False)
    domain = models.CharField(verbose_name="域名", max_length=255, null=True, blank=True)
    host = models.CharField(verbose_name="主机", max_length=255, null=True, blank=True)
    port = models.PositiveIntegerField(verbose_name="端口", null=True, blank=True)
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
        if self.domain:
            url = f"{self.protocol.name}://{self.domain}"
            if self.path:
                url += self.path
        else:
            url = f"{self.protocol.name}://{self.host}"
            if self.port:
                url += f":{self.port}"
            if self.path:
                url += self.path
        return url

    def resolve_domain(self):
        """解析域名获取IP地址"""
        if not self.domain:
            return None
        
        import socket
        try:
            return socket.gethostbyname(self.domain)
        except socket.gaierror:
            return None

    def save(self, *args, **kwargs):
        # 如果提供了域名，尝试解析获取IP
        if self.domain:
            resolved_ip = self.resolve_domain()
            if resolved_ip:
                self.host = resolved_ip
                self.try_match_or_create_resources(resolved_ip)
        
        # 如果提供了IP地址，尝试匹配或创建资源
        if self.host and not self.domain:
            self.try_match_or_create_resources(self.host)
            
        super().save(*args, **kwargs)

    def try_match_or_create_resources(self, ip_address):
        """尝试匹配或创建相关资源"""
        try:
            # 尝试查找已存在的IP地址记录
            ip = IPAddress.objects.get(ip=ip_address)
            # 如果找到了IP地址，并且服务没有关联操作系统，尝试自动关联
            if ip.device and hasattr(ip.device, 'systems') and not self.service.system:
                systems = ip.device.systems.all()
                if systems.count() == 1:
                    # 如果只有一个操作系统，直接关联
                    self.service.system = systems.first()
                    self.service.save()
        except IPAddress.DoesNotExist:
            # 检查是否是有效的IP地址
            if ip_address.replace('.', '').isdigit():
                # 创建网络
                net = Net.objects.create(
                    content=f"{ip_address}/32",  # 假设是单个IP地址
                    remark="自动创建的网络"
                )
                # 创建IP地址
                ip = IPAddress.objects.create(
                    ip=ip_address,
                    net=net,
                    remark="自动创建的IP地址"
                )
                # 创建服务器
                server = ServerNew.objects.create(
                    remark=f"自动创建服务器-{ip_address}"
                )
                # 创建操作系统
                os_image = OperationSystemImage.objects.filter(name="CentOS", version="7").first()
                if os_image:
                    os = OperationSystem.objects.create(
                        image=os_image,
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
