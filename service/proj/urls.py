"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import accountSystem.urls
import jumpService.urls
from jumpService.views.api import ServerViewSet, ServiceViewSet, UserSystemViewSet, NetViewSet, IPAddressViewSet, UnifiedServiceUserViewSet, OperationSystemViewSet, ServiceTypeViewSet
from rest_framework.routers import DefaultRouter

# DRF Router for API endpoints
api_router = DefaultRouter()
api_router.register(r'servers', ServerViewSet, basename='api-server')
api_router.register(r'services', ServiceViewSet, basename='api-service')
api_router.register(r'user-systems', UserSystemViewSet, basename='api-user-system')
api_router.register(r'credentials', UnifiedServiceUserViewSet, basename='api-credential')
api_router.register(r'nets', NetViewSet, basename='api-net')
api_router.register(r'ips', IPAddressViewSet, basename='api-ip')
api_router.register(r'systems', OperationSystemViewSet, basename='api-system')
api_router.register(r'service-types', ServiceTypeViewSet, basename='api-servicetype')
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.flatpages import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.contrib.sites.models import Site
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from proj import settings

from . import _STATIC_URL
from .view import media

# 网站标签页名称
admin.site.site_title = "AccessPod+KeyHub"
# 网站名称：显示在登录页和首页
admin.site.site_header = 'AccessPod+KeyHub'
# 取消注册 Sites 模型
admin.site.unregister(Site)

# 取消注册 Group 模型
admin.site.unregister(Group)
admin.site.unregister(User)

admin.autodiscover()
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', media),
    path(f"admin/", admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path('^all-keeper/', include(accountSystem.urls)),
    path("favicon.ico", RedirectView.as_view(url=_STATIC_URL + 'favicon.ico')),
    re_path(r'^static/(?P<path>.*)$', serve, ({'document_root': settings.STATIC_ROOT})),
    path('sp/', include('simplepro.urls')),
    re_path('^jump_service/', include(jumpService.urls)),
    path('api/', include(api_router.urls)),
    re_path(r'^static/(?P<path>.*)$', serve, ({'document_root': settings.STATIC_ROOT})),
    re_path(r'^media/(?P<path>.*)$', media)
]
