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
from .service import AbstractBaseServiceModel, AbstractBaseServiceUserModel


class VPNService(AbstractBaseServiceModel):
    TYPE_CHOICES = (
        ('openvpn', 'OpenVPN'),
        ('wireguard', 'WireGuard'),
        ('ipsec', 'IPSec'),
        ('l2tp', 'L2TP'),
        ('pptp', 'PPTP'),
        ('sstp', 'SSTP'),
    )
    vpn_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="VPN类型", default='openvpn')
    protocol = models.CharField(max_length=10, choices=(('udp', 'UDP'), ('tcp', 'TCP')), default='udp', verbose_name="协议")
    subnet = models.CharField(max_length=50, verbose_name="虚拟网段", placeholder="例如: 10.8.0.0/24", null=True, blank=True)
    public_host = models.CharField(max_length=255, verbose_name="公网连接地址", placeholder="IP或域名", null=True, blank=True)
    config_template = models.TextField(verbose_name="配置模板", null=True, blank=True)

    class Meta:
        verbose_name = "VPN服务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_vpn_type_display()}服务({self.server}:{self.port})"


class VPNUser(AbstractBaseServiceUserModel):
    service = models.ForeignKey(to=VPNService, on_delete=models.CASCADE, verbose_name="所属VPN服务", related_name="vpn_users")
    client_config = models.TextField(verbose_name="客户端配置", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    expired_at = models.DateTimeField(verbose_name="过期时间", null=True, blank=True)

    class Meta:
        verbose_name = "VPN用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"VPN用户({self.username}@{self.service})"
