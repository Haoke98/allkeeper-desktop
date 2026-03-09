# _*_ codign:utf8 _*_
from django.contrib import admin
from simplepro.admin import BaseAdmin

from ..models import UserSystem, UnifiedServiceUser


@admin.register(UserSystem)
class UserSystemAdmin(BaseAdmin):
    list_display = ('name', 'remark', 'id')
    search_fields = ('name', 'remark')


@admin.register(UnifiedServiceUser)
class UnifiedServiceUserAdmin(BaseAdmin):
    list_display = ('username', 'user_system', 'owner', 'hasRootPriority', 'is_active', 'expired_at')
    search_fields = ('username', 'owner', 'remark')
    list_filter = ('user_system', 'hasRootPriority', 'is_active')
    autocomplete_fields = ('user_system',)
