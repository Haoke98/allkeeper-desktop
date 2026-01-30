# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2026/01/30
@Software: PyCharm
@disc:
======================================="""
from django.contrib import admin
from simplepro.admin import BaseAdmin, FieldOptions
from ..models import VPNDevice, VPNService, VPNUser
from .net import IPAddressInlineAdmin, NetDeviceAdmin


@admin.register(VPNDevice)
class VPNDeviceAdmin(NetDeviceAdmin):
    list_display = ['code', 'webControlAddress','webControlUsername','webControlPassword', 'remark', 'hoster', 'updatedAt', 'id']
    inlines = [IPAddressInlineAdmin]

    fields_options = {
        'id': FieldOptions.UUID,
        'code': {'fixed': 'left', 'min_width': '100px', 'align': 'center'},
        'webControlAddress': {'min_width': '200px'},
        'remark': {'min_width': '200px'},
    }


@admin.register(VPNService)
class VPNServiceAdmin(BaseAdmin):
    list_display = ['vpn_type', 'server', 'port', 'protocol', 'subnet', 'public_host']
    list_filter = ['vpn_type', 'protocol']
    search_fields = ['server__code', 'server__remark', 'public_host']


@admin.register(VPNUser)
class VPNUserAdmin(BaseAdmin):
    list_display = ['username', 'service', 'owner', 'is_active', 'expired_at']
    list_filter = ['is_active', 'service__vpn_type']
    search_fields = ['username', 'owner', 'service__server__remark']
