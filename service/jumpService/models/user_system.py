# _*_ codign:utf8 _*_
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel


class UserSystem(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator, editable=False)
    name = fields.CharField(max_length=50, verbose_name="名称", unique=True)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    # Primary Service Relationship
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="主服务类型")
    object_id = models.CharField(max_length=48, null=True, blank=True, verbose_name="主服务ID")
    primary_service = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "用户体系"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.primary_service:
            return f"用户体系 - {self.primary_service}"
        return self.name or str(self.id)


class UnifiedServiceUser(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, default=pkHelper.uuid_generator, editable=False)
    user_system = models.ForeignKey(to=UserSystem, on_delete=models.CASCADE, verbose_name="所属用户体系",
                                    related_name="users")
    owner = models.CharField(verbose_name="使用者", max_length=50, null=True, blank=True)
    username = fields.CharField(max_length=32, null=True, blank=False, verbose_name="用户名")
    password = fields.PasswordInputField(max_length=32, null=True, blank=False, verbose_name="密码", size="medium",
                                         style="width:600px;", pattern="123456789,.asdfgzxcvbnm")
    hasRootPriority = models.BooleanField(default=False, verbose_name="拥有root权限", blank=True)
    remark = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

    # System User specific
    userGroup = (
        (0, "root:x:0:"),
        (1, "bin:x:1:"),
        (2, "daemon:x:2:"),
        (3, "sys:x:3:"),
        (4, "adm:x:4:"),
        (5, "tty:x:5:"),
        (6, "disk:x:6:"),
        (7, "lp:x:7:"),
        (8, "mem:x:8:"),
        (9, "kmem:x:9:"),
        (10, "wheel:x:10:"),
        (11, "cdrom:x:11:"),
        (12, "mail:x:12:postfix"),
        (13, "man:x:15:"),
        (14, "dialout:x:18:"),
        (15, "floppy:x:19:"),
        (16, "games:x:20:"),
        (17, "tape:x:33:"))
    group = fields.IntegerField(verbose_name='用户组', choices=userGroup, null=True, blank=True)

    # VPN User specific
    client_config = models.TextField(verbose_name="客户端配置", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    expired_at = models.DateTimeField(verbose_name="过期时间", null=True, blank=True)

    class Meta:
        verbose_name = "统一服务用户"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user_system', 'username'], name="unique_user_in_system")
        ]

    def __str__(self):
        system_name = str(self.user_system)
        return f"{self.username}@{system_name}"
