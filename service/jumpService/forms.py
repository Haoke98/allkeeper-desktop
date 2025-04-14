# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/15
@Software: PyCharm
@disc:
======================================="""
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import IPAddress, ServiceURL


class ServiceURLForm(forms.ModelForm):
    host = forms.CharField(
        label="主机",
        widget=forms.TextInput(attrs={
            'class': 'el-input__inner',
            'list': 'host-list',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = ServiceURL
        fields = ['name', 'protocol', 'host', 'port', 'path', 'is_default', 'is_dashboard']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取所有已存在的IP地址
        self.fields['host'].widget.attrs['datalist'] = self.get_host_choices()

    def get_host_choices(self):
        """获取主机选项列表"""
        # 从IP地址表中获取所有IP
        ips = IPAddress.objects.values_list('ip', flat=True)
        # 从已有的ServiceURL中获取所有主机地址
        hosts = ServiceURL.objects.values_list('host', flat=True).distinct()
        # 合并并去重
        return list(set(list(ips) + list(hosts))) 