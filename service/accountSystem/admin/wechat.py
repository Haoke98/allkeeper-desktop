from django.contrib import admin
from simplepro.admin import BaseAdmin

from accountSystem.models import Wechat


@admin.register(Wechat)
class WechatAdmin(BaseAdmin):
    list_display = ['_id', 'createdAt', 'updatedAt', 'deletedAt', '_tel', '_password', 'nickName', 'email', 'group',
                    'remark']
    list_display_links = ['_id', 'nickName', 'email']
    date_hierarchy = 'updatedAt'
    search_fields = ['id', 'nickName', 'remark', 'email', ]
    list_filter = ['tel', 'group', 'email']
    list_select_related = list_filter
    autocomplete_fields = list_filter
    list_per_page = 8
    actions = []
    fields_options = {
        '_id': {
            'width': '150px',
            'align': 'left'
        },
        'createdAt': {
            'width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'width': '180px',
            'align': 'left'
        },
        '_tel': {
            'width': '150px',
            'align': 'left'
        },
        '_password': {
            'width': '150px',
            'align': 'center'
        },
        'nickName': {
            'width': '120px',
            'align': 'left'
        },
        'email': {
            'width': '200px',
            'align': 'left'
        },
        'group': {
            'width': '150px',
            'align': 'left'
        },
        'remark': {
            'width': '240px',
            'align': 'left'
        },
    }

    def _id(self, obj):
        return BaseAdmin.username(obj.id)

    def _password(self, obj):
        return BaseAdmin.password(obj.pwd)

    def _tel(self, obj):
        return BaseAdmin.username(obj.tel.content)
