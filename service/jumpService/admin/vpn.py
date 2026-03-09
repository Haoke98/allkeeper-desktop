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

from accountSystem.admin.base import BaseAccountAdmin
from ..models import VPNDevice, VPNService
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
class VPNServiceAdmin(BaseAccountAdmin):
    list_display = ['id', 'server', 'port', 'vpn_type', 'protocol', 'subnet', 'public_host', 'updatedAt', 'createdAt']
    search_fields = ['server__name', 'server__ip', 'public_host', 'remark']
    list_filter = ['vpn_type', 'protocol', 'server']
