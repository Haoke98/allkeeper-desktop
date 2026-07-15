# _*_ codign:utf8 _*_
"""DRF Viewsets for AccessPod+KeyHub REST API — full CRUD support"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from jumpService.models import (
    ServerNew, OperationSystem, Service, ServiceURL,
    UserSystem, UnifiedServiceUser, Protocol,
    Net, IPAddress, ServiceType
)
from jumpService.serializers import (
    ServerSerializer, OperationSystemSerializer, ServiceSerializer,
    ServiceURLSerializer, UserSystemSerializer, UnifiedServiceUserSerializer,
    ProtocolSerializer, NetSerializer, IPAddressSerializer, ServiceTypeSerializer
)
from .api_pagination import ApiPagination


class ServerViewSet(viewsets.ModelViewSet):
    """Device CRUD API"""
    queryset = ServerNew.objects.prefetch_related('ips__net', 'systems__image', 'cabinet__room').order_by('-updatedAt').all()
    serializer_class = ServerSerializer
    pagination_class = ApiPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'remark', 'ips__ip', 'mac']

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def systems(self, request, pk=None):
        server = self.get_object()
        systems = server.systems.all()
        serializer = OperationSystemSerializer(systems, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """Service CRUD API"""
    queryset = Service.objects.prefetch_related(
        '_type', 'system__image', 'system__server__ips__net', 'urls__protocol'
    ).order_by('-updatedAt').all()
    serializer_class = ServiceSerializer
    pagination_class = ApiPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['_type__name', 'remark', 'port']

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def urls(self, request, pk=None):
        service = self.get_object()
        urls = service.urls.all()
        serializer = ServiceURLSerializer(urls, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        service = self.get_object()
        if not service.user_system:
            return Response([])
        users = UnifiedServiceUser.objects.filter(user_system=service.user_system)
        serializer = UnifiedServiceUserSerializer(users, many=True)
        return Response(serializer.data)


class UserSystemViewSet(viewsets.ModelViewSet):
    """User system CRUD API"""
    queryset = UserSystem.objects.prefetch_related('users').order_by('-updatedAt').all()
    serializer_class = UserSystemSerializer
    pagination_class = ApiPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'remark']

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        system = self.get_object()
        users = system.users.all()
        serializer = UnifiedServiceUserSerializer(users, many=True)
        return Response(serializer.data)


class UnifiedServiceUserViewSet(viewsets.ModelViewSet):
    """Credential user CRUD API"""
    queryset = UnifiedServiceUser.objects.order_by('-updatedAt').all()
    serializer_class = UnifiedServiceUserSerializer
    pagination_class = ApiPagination

    def perform_create(self, serializer):
        serializer.save()


class NetViewSet(viewsets.ModelViewSet):
    """Network segment CRUD API"""
    queryset = Net.objects.order_by('-updatedAt').all()
    serializer_class = NetSerializer
    pagination_class = ApiPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'remark']

    def perform_create(self, serializer):
        serializer.save()


class IPAddressViewSet(viewsets.ModelViewSet):
    """IP address CRUD API"""
    queryset = IPAddress.objects.select_related('net').order_by('-updatedAt').all()
    serializer_class = IPAddressSerializer
    pagination_class = ApiPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['ip']

    def perform_create(self, serializer):
        serializer.save()


class OperationSystemViewSet(viewsets.ModelViewSet):
    """Operating system CRUD API"""
    queryset = OperationSystem.objects.select_related('image', 'server').order_by('-updatedAt').all()
    serializer_class = OperationSystemSerializer
    pagination_class = ApiPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['image__name', 'server__code']

    def perform_create(self, serializer):
        serializer.save()


class ServiceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Service type list API"""
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
