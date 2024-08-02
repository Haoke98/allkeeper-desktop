from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter

from .views import ServerViewSet, collect, service, network_topology, ssh

router = DefaultRouter()
router.register(r'server', viewset=ServerViewSet)
# server_list = ServerViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# server_detail = ServerViewSet.as_view({
#     'get': 'retrieve'
# })
urlpatterns = [
                  path('server/collect', collect),
                  path('service/users', service.get_users),
                  path('net', network_topology),
                  path('op_sys/remote/control', ssh)
                  # path('getSubcribtionAccessToken', getSubcribtionsAccessToken),
                  # path('buyVIP<str:openid>', buyVIP)
              ] + router.urls
