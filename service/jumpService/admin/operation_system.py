# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/12/11
@Software: PyCharm
@disc:
======================================="""
import base64

from django.contrib import admin
from django.forms import ModelForm
from simplepro.admin import FieldOptions, BaseAdmin
from simplepro.dialog import ModalDialog, MultipleCellDialog

from ..models import OperationSystem, OperationSystemImage, IPAddress, SystemUser


@admin.register(OperationSystemImage)
class OperationSystemImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'version', 'arch', 'isLTS', 'updatedAt', 'createdAt', 'deletedAt']
    list_filter = ['name', 'arch', 'isLTS', 'updatedAt', 'createdAt']
    search_fields = ['version', 'remark']
    ordering = ['-updatedAt']
    fields = ['name', 'version', 'isLTS', 'arch', 'iso', 'remark']
    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'name': {
            'min_width': '280px',
            'align': 'left'
        },
        'version': {
            'min_width': '180px',
            'align': 'left'
        },
        'arch': {
            'min_width': '100px',
            'align': 'left'
        },
    }


class UserForm(ModelForm):
    class Meta:
        model = SystemUser
        # fields = ['username', 'password', 'owner', 'hasRootPriority', 'group', 'remark']
        fields = ['username', 'password', 'owner', 'remark']


class UserInlineAdmin(admin.TabularInline):
    model = SystemUser
    form = UserForm
    min_num = 0
    extra = 0


@admin.register(OperationSystem)
class OperationSystemAdmin(BaseAdmin):
    list_display = ['id', 'image', 'server', 'open_webssh', 'sshPort',
                    'updatedAt', 'createdAt', 'deletedAt']
    list_filter = ['server', 'image', 'server__remark']
    search_fields = ['server__code', 'server__remark', 'server__ips__ip']
    ordering = ('-updatedAt',)
    inlines = [UserInlineAdmin]

    def open_webssh(self, obj: OperationSystem):
        modals = []
        modal = ModalDialog()
        modal.width = "92%"
        modal.height = "70vh"
        # 这个是单元格显示的文本
        modal.cell = f'<el-link type="primary">连接</el-link>'
        modal.title = obj.__str__()
        # 是否显示取消按钮
        modal.show_cancel = True
        modal.url = f"/jump_service/op_sys/remote/control?id={obj.id}"
        # print("正在连接SSH", modal.url)
        modals.append(modal)
        return MultipleCellDialog(modals)

    open_webssh.short_description = "远程桌面/SSH"

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "ip":
            if value:
                return BaseAdmin.username(obj.ip)
        if field_name == 'rootPassword':
            if value:
                return BaseAdmin.password(obj.rootPassword)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'server': {
            'min_width': '280px',
            'align': 'left'
        },
        'sshPort': {
            'min_width': '140px',
            'align': 'center'
        },
        'image': {
            'min_width': '160px',
            'align': 'left',
            "show_overflow_tooltip": True
        },
        'rootUsername': FieldOptions.USER_NAME,
        'rootPassword': FieldOptions.PASSWORD,
        'open_webssh': {
            'min_width': '120px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': {
            'min_width': '200px',
            'align': 'left'
        },

        'bios': {
            'min_width': '180',
            'align': 'center'
        },
        'cabinet': {
            'min_width': '180',
            'align': 'center'
        },
        'mac': {
            'min_width': '220px',
            'align': 'left'
        }
    }
