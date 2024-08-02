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
import icloud.urls
import jumpService.urls
from django.conf.urls import include
from django.contrib import admin
from django.contrib.flatpages import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from proj import settings

from . import _STATIC_URL
from .secret import ADMIN_PATH
from .view import media

# 网站标签页名称
admin.site.site_title = "AllKeeper"
# 网站名称：显示在登录页和首页
admin.site.site_header = 'AllKeeper'

admin.autodiscover()
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', media),
    path(f"{ADMIN_PATH}/", admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path('^all-keeper/', include(accountSystem.urls)),
    re_path('^icloud/', include(icloud.urls)),
    path("favicon.ico", RedirectView.as_view(url=_STATIC_URL + 'favicon.ico')),
    re_path(r'^static/(?P<path>.*)$', serve, ({'document_root': settings.STATIC_ROOT})),
    path('sp/', include('simplepro.urls')),
    re_path('^jump_service/', include(jumpService.urls)),
]
