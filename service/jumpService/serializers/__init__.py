# _*_ codign:utf8 _*_
"""DRF Serializers for AccessPod+KeyHub REST API
Field names MUST match the Django model attribute names exactly.
SimplePro BaseModel uses camelCase (createdAt, updatedAt).
Service/URL models use a mix of camelCase and snake_case.
"""
from rest_framework import serializers
from jumpService.models import (
    ServerNew, OperationSystem, OperationSystemImage,
    Service, ServiceType, ServiceURL, Protocol,
    UserSystem, UnifiedServiceUser,
    IPAddress, Net, ServerRoom, ServerCabinet,
)


class NetSerializer(serializers.ModelSerializer):
    is_global = serializers.SerializerMethodField()

    class Meta:
        model = Net
        fields = ['id', 'content', 'gatewayIP', 'remark', 'is_global']

    def get_is_global(self, obj):
        return obj.is_global()


class IPAddressSerializer(serializers.ModelSerializer):
    net = NetSerializer(read_only=True)

    class Meta:
        model = IPAddress
        fields = ['id', 'ip', 'net']


class ServerRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerRoom
        fields = ['id', 'code']


class ServerCabinetSerializer(serializers.ModelSerializer):
    room = ServerRoomSerializer(read_only=True)

    class Meta:
        model = ServerCabinet
        fields = ['id', 'code', 'room']


class OperationSystemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationSystemImage
        fields = ['id', 'name', 'series', 'version', 'build_number',
                  'code_name', 'arch', 'isLTS']


class OperationSystemSerializer(serializers.ModelSerializer):
    image = OperationSystemImageSerializer(read_only=True)
    server_id = serializers.ReadOnlyField()
    server_code = serializers.SerializerMethodField()
    server_remark = serializers.SerializerMethodField()

    class Meta:
        model = OperationSystem
        fields = ['id', 'image', 'server_id', 'server_code', 'server_remark',
                  'remoteAccessPort', 'user_system', 'createdAt', 'updatedAt']

    def get_server_code(self, obj):
        return obj.server.code if obj.server else None

    def get_server_remark(self, obj):
        return obj.server.remark if obj.server else None


class ServerSerializer(serializers.ModelSerializer):
    ips = IPAddressSerializer(many=True, read_only=True)
    cabinet = ServerCabinetSerializer(read_only=True)
    systems = OperationSystemSerializer(many=True, read_only=True)
    system_count = serializers.SerializerMethodField()
    hosterDisplay = serializers.CharField(source='get_hoster_display', read_only=True)

    class Meta:
        model = ServerNew
        fields = ['id', 'code', 'hoster', 'hosterDisplay', 'bios', 'cabinet',
                  'remark', 'mac', 'ips', 'systems', 'system_count',
                  'webControlAddress', 'webControlUsername', 'webControlPassword',
                  'createdAt', 'updatedAt']

    def get_system_count(self, obj):
        return obj.systems.count()


class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = ['id', 'name', 'default_port', 'is_web_protocol', 'description']


class ServiceURLSerializer(serializers.ModelSerializer):
    protocol = ProtocolSerializer(read_only=True)

    class Meta:
        model = ServiceURL
        fields = ['id', 'name', 'protocol', 'domain', 'host', 'port', 'path',
                  'is_default', 'is_dashboard']


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'port', 'defaultSuperUsername', 'doc', 'official']


class ServiceSerializer(serializers.ModelSerializer):
    _type = ServiceTypeSerializer(read_only=True)
    system = OperationSystemSerializer(read_only=True)
    urls = ServiceURLSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', '_type', 'system', 'port', 'sslOn', 'dashboardPort',
                  'dashboardPath', 'wafPort', 'user_system', 'remark', 'urls',
                  'createdAt', 'updatedAt']


class UnifiedServiceUserSerializer(serializers.ModelSerializer):
    groupDisplay = serializers.CharField(source='get_group_display', read_only=True)

    class Meta:
        model = UnifiedServiceUser
        fields = ['id', 'user_system', 'username', 'password', 'owner',
                  'hasRootPriority', 'remark', 'group', 'groupDisplay',
                  'is_active', 'expired_at']


class UserSystemSerializer(serializers.ModelSerializer):
    users = UnifiedServiceUserSerializer(many=True, read_only=True)

    class Meta:
        model = UserSystem
        fields = ['id', 'name', 'remark', 'users', 'createdAt', 'updatedAt']
