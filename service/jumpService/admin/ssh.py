from django.contrib import admin
from simplepro.admin import BaseAdmin, FieldOptions

from ..models import SystemUser


@admin.register(SystemUser)
class SystemUserAdmin(BaseAdmin):
    list_display = ['id', 'system', 'username', 'password', 'group', 'owner', 'updatedAt', 'createdAt']
    list_filter = ['hasRootPriority', 'system', 'owner', 'group']
    ordering = ['-updatedAt']
    fields = ['owner', 'system', 'username', 'password', 'group', 'info']
    search_fields = ['username', 'password']
    actions = ['migrate_service2server']

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "username":
            if value:
                return BaseAdmin.username(obj.username)
        if field_name == 'password':
            if value:
                return BaseAdmin.password(obj.password)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        if field_name == "url":
            if value:
                return f"""<a href="{value}" target="_blank">点击跳转</a>"""
        if field_name == "name":
            if value:
                return f'''<el-button type="info" onclick="goToDetail(this)" round>{value}</el-button>'''
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'system': {
            'min_width': '360px',
            'align': 'left',
            "show_overflow_tooltip": True
        },
        'server': {
            'min_width': '300px',
            'align': 'left'
        },
        'username': {
            'min_width': '200px',
            'align': 'center'
        },
        'password': {
            'min_width': '180px',
            'align': 'left'
        },
        'group': {
            'min_width': '200px',
            'align': 'center'
        },
        'owner': {
            'min_width': '280px',
            'align': 'left'
        }
    }


class ServerUserInlineAdmin(admin.TabularInline):
    model = SystemUser
    autocomplete_fields = ['server', 'owner']
    min_num = 0
    extra = 0
