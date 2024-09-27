from django.apps import AppConfig


class AccountSystemConfig(AppConfig):
    name = 'accountSystem'
    verbose_name = '账号管理系统'

    def ready(self):
        from .admin.account import AccountAdmin
        from .admin.breath import BreathInfoAdmin
        from .admin.email import EmailAdmin
        from .admin.human import HumanAdmin
        from .admin.market_subject import MarketSubjectAdmin
        from .admin.platform import PlatformAdmin, URLAdmin
        from .admin.scripts import ScriptAdmin
        from .admin.tel import TelAdmin
        from .admin.wechat import WechatAdmin