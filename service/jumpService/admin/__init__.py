# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
import sys

# 永久解决：如果是迁移相关命令，直接跳过 Admin 加载，避免触发数据库查询
if not any(arg in sys.argv for arg in ['makemigrations', 'migrate', 'inspectdb']):
    from .bt import BtAdmin
    from .dbService import DbServiceAdmin
    from .device import DeviceAdmin
    from .minio import MinIOAdmin
    from .net import NetWorkAdmin, NetDeviceAdmin, IPAddressAdmin
    from .router import RouterAdmin
    from .vpn import VPNDeviceAdmin, VPNServiceAdmin
    from .server import ServerAdmin
    from .service import ServiceAdmin, ServiceTypeAdmin
    from .operation_system import OperationSystemAdmin
    from .channel import ChannelAdmin
    from .port import PortMapAdmin, PortAdmin

from .user_system import UserSystemAdmin, UnifiedServiceUserAdmin
