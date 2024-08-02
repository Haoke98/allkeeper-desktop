from django.contrib import admin
from django.db import IntegrityError
from simplepro.admin import BaseAdmin, FieldOptions

from ..models import SystemUser, SSHService, OperationSystem


@admin.register(SSHService)
class SSHServiceAdmin(BaseAdmin):
    list_display = ['id', 'server', 'port', 'updatedAt', 'createdAt']
    list_filter = ['server', 'port']
    autocomplete_fields = ['server']
    search_fields = ['server', 'port', 'remark']
    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'server': {
            'min_width': '280px',
            'align': 'left'
        },
        'port': {
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


@admin.register(SystemUser)
class SystemUserAdmin(BaseAdmin):
    list_display = ['id', 'system', 'username', 'password', 'group', 'owner', 'updatedAt', 'createdAt']
    list_filter = ['hasRootPriority', 'system', 'owner', 'group']
    fields = ['owner', 'system', 'username', 'password', 'group', 'info']
    search_fields = ['username', 'password']
    actions = ['migrate_service2server']

    def migrate_service2server(self, request, queryset):
        for qs in queryset:
            if qs.server is None:
                print(qs, "(跳过)")
                continue
            op_systems = OperationSystem.objects.filter(server=qs.server).all()
            print(qs, "({})".format(len(op_systems)), end=" ")
            if qs.system is not None:
                print("(跳过)")
                continue
            if len(op_systems) == 1:
                # TODO
                try:
                    qs.system = op_systems[0]
                    qs.save()
                    print("(迁移成功!)")
                except IntegrityError as e:
                    print(f"(用户名[{qs.username}]和系统[{qs.system}]出现了重复,跳过)")
                continue
            print()
            for op in op_systems:
                print(" " * 10, "|")
                print(" " * 10, "+", "-" * 10, op)

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
            'min_width': '300px',
            'align': 'left'
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
