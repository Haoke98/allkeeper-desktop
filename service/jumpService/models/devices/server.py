from django.db import models
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel

from .net_device import NetDevice

__all__ = ['ServerRoom', 'ServerCabinet', 'ServerNew', 'ServerStatus', 'CPU']


class ServerRoom(BaseModel):
    code = fields.CharField(verbose_name="编号", max_length=50, null=True, unique=True, blank=False)

    class Meta:
        verbose_name = "机房"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"机房{self.code}"


class ServerCabinet(BaseModel):
    code = fields.CharField(verbose_name="编号", max_length=50, null=True, blank=False)
    room = fields.ForeignKey(to=ServerRoom, on_delete=models.CASCADE, verbose_name="所属机房")

    class Meta:
        verbose_name = "机柜"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['code', 'room'], name="server_cabinet_room_unique")
        ]

    def __str__(self):
        return f"{self.room}-{self.code}"


class ServerNew(NetDevice):
    code = fields.CharField(verbose_name="编号", max_length=50, null=True, unique=True, blank=True)
    hosterOptions = (
        (1, '阿里云'),
        (2, '腾讯云'),
        (3, '哈密市希望科技有限公司'),
        (4, '新疆丝路融创网络科技有限公司（局域网）')
    )
    hoster = models.PositiveSmallIntegerField(choices=hosterOptions, null=True, blank=True, verbose_name="托管方")
    bios = fields.PasswordInputField(verbose_name="BIOS", max_length=32, null=True, blank=True)
    cabinet = fields.ForeignKey(to=ServerCabinet, on_delete=models.CASCADE, verbose_name="机柜", null=True, blank=True)

    def system_count(self):
        return self.systems.count()

    system_count.short_description = "承载系统数量"

    class Meta:
        verbose_name = "物理服务器"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 获取所有子类模型
        for related_object in self._meta.related_objects:
            if related_object.one_to_one and related_object.field.remote_field.parent_link:
                try:
                    concrete_instance = getattr(self, related_object.name)
                    if concrete_instance:
                        return str(concrete_instance)
                except related_object.related_model.DoesNotExist:
                    continue
        if self.code:
            if self.remark:
                return f"服务器({self.code},{self.remark})"
            else:
                return f"服务器({self.code})"
        else:
            if self.remark:
                return f"服务器({self.id},{self.remark})"
            else:
                return f"服务器({self.id})"


class ServerStatus(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator)
    server = models.ForeignKey(ServerNew, on_delete=models.CASCADE, null=True, blank=True, verbose_name="所属设备")
    ip = fields.CharField(verbose_name="IP地址", max_length=50, null=True, blank=True)
    cpuUsage = fields.IntegerField(verbose_name="CPU使用率", null=True, blank=True)
    memoryUsage = fields.IntegerField(verbose_name="内存使用率", null=True, blank=True)
    diskUsage = fields.IntegerField(verbose_name="磁盘使用率", null=True, blank=True)

    class Meta:
        verbose_name = "服务器状态"
        verbose_name_plural = verbose_name
        ordering = ('-createdAt',)


class CPU(BaseModel):
    brand = fields.ForeignKey(to="Brand", on_delete=models.CASCADE, null=True, blank=True, verbose_name="品牌")
    model = fields.CharField(max_length=50, unique=True)
    name = fields.CharField(max_length=50, unique=True)
    frequency = fields.IntegerField(verbose_name="频率(Ghz)", null=True, blank=True)
