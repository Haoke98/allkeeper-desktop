from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from jumpService.models.services.service import Service, ServiceUser
from jumpService.models.services.ssh import SystemUser
from jumpService.models.services.db import DbService, DbServiceUser
from jumpService.models.services.vpn import VPNService, VPNUser
from jumpService.models.user_system import UserSystem, UnifiedServiceUser
from jumpService.models.operation_system import OperationSystem

class Command(BaseCommand):
    help = 'Migrate existing user models to the new UnifiedServiceUser system'

    def handle(self, *args, **options):
        self.stdout.write('Starting migration to UnifiedServiceUser system...')
        
        try:
            with transaction.atomic():
                self.migrate_service_users()
                self.migrate_system_users()
                self.migrate_db_service_users()
                self.migrate_vpn_users()
            
            self.stdout.write(self.style.SUCCESS('Migration completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {str(e)}'))
            # Re-raise to rollback transaction
            raise e

    def get_or_create_user_system(self, instance, name_suffix):
        if instance.user_system:
            return instance.user_system
        
        name = f"{str(instance)} - {name_suffix}"
        if len(name) > 50:
            name = name[:47] + "..."
            
        # Try to find existing system by name to avoid unique constraint error
        user_system = UserSystem.objects.filter(name=name).first()
        if not user_system:
            # Get ContentType for the instance
            content_type = ContentType.objects.get_for_model(instance)
            
            user_system = UserSystem.objects.create(
                name=name,
                remark=f"Auto-generated for {instance}",
                content_type=content_type,
                object_id=instance.id,
            )
        instance.user_system = user_system
        instance.save()
        self.stdout.write(f"Created/Found UserSystem: {user_system.name}")
        return user_system

    def migrate_service_users(self):
        self.stdout.write("Migrating ServiceUsers...")
        for service in Service.objects.all():
            users = ServiceUser.objects.filter(service=service)
                
            if not users.exists():
                continue
                
            user_system = self.get_or_create_user_system(service, "服务用户")
            
            for user in users:
                self.create_unified_user(user_system, user)

    def migrate_system_users(self):
        self.stdout.write("Migrating SystemUsers...")
        for system in OperationSystem.objects.all():
            users = system.users.all()
                
            if not users.exists():
                continue
                
            user_system = self.get_or_create_user_system(system, "系统用户")
            
            for user in users:
                unified = self.create_unified_user(user_system, user)
                unified.group = user.group
                unified.save()

    def migrate_db_service_users(self):
        self.stdout.write("Migrating DbServiceUsers...")
        for service in DbService.objects.all():
            users = DbServiceUser.objects.filter(service=service)
                
            if not users.exists():
                continue
                
            user_system = self.get_or_create_user_system(service, "DB用户")
            
            for user in users:
                self.create_unified_user(user_system, user)

    def migrate_vpn_users(self):
        self.stdout.write("Migrating VPNUsers...")
        for service in VPNService.objects.all():
            users = service.vpn_users.all()
                
            if not users.exists():
                continue
                
            user_system = self.get_or_create_user_system(service, "VPN用户")
            
            for user in users:
                unified = self.create_unified_user(user_system, user)
                unified.client_config = user.client_config
                unified.is_active = user.is_active
                unified.expired_at = user.expired_at
                unified.save()

    def create_unified_user(self, user_system, original_user):
        # Check if user already exists
        existing = UnifiedServiceUser.objects.filter(user_system=user_system, username=original_user.username).first()
        if existing:
            return existing
            
        unified = UnifiedServiceUser(
            user_system=user_system,
            username=original_user.username,
            password=original_user.password,
            owner=original_user.owner,
            hasRootPriority=original_user.hasRootPriority
        )
        unified.save()
        self.stdout.write(f"  Migrated user: {unified.username}")
        return unified
