import os

service_file = 'service/jumpService/models/services/service.py'

with open(service_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
if 'from ..user_system import UserSystem' not in content:
    content = content.replace('from ..operation_system import OperationSystem', 'from ..operation_system import OperationSystem\nfrom ..user_system import UserSystem')

# Add user_system field to Service
if 'user_system =' not in content:
    content = content.replace('system = fields.ForeignKey(to=OperationSystem, on_delete=models.CASCADE, verbose_name="操作系统", null=True,\n                               blank=True)', 'system = fields.ForeignKey(to=OperationSystem, on_delete=models.CASCADE, verbose_name="操作系统", null=True,\n                               blank=True)\n    user_system = models.ForeignKey(to=UserSystem, on_delete=models.CASCADE, verbose_name="所属用户体系", null=True, blank=True)')
    # Handle the case where blank=False in older version
    content = content.replace('system = fields.ForeignKey(to=OperationSystem, on_delete=models.CASCADE, verbose_name="操作系统", null=True,\n                               blank=False)', 'system = fields.ForeignKey(to=OperationSystem, on_delete=models.CASCADE, verbose_name="操作系统", null=True,\n                               blank=False)\n    user_system = models.ForeignKey(to=UserSystem, on_delete=models.CASCADE, verbose_name="所属用户体系", null=True, blank=True)')

# Add user_system field to AbstractBaseServiceModel
if 'user_system =' not in content[content.find('class AbstractBaseServiceModel'):]:
    content = content.replace('server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,\n                               blank=False, db_index=True, related_name="%(class)s_services")', 'server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,\n                               blank=False, db_index=True, related_name="%(class)s_services")\n    user_system = models.ForeignKey(to=UserSystem, on_delete=models.CASCADE, verbose_name="所属用户体系", null=True, blank=True)')
    # Handle related_name="services" case (older version)
    content = content.replace('server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,\n                               blank=False, db_index=True, related_name="services")', 'server = models.ForeignKey(to=ServerNew, on_delete=models.CASCADE, verbose_name="服务器", null=True,\n                               blank=False, db_index=True, related_name="services")\n    user_system = models.ForeignKey(to=UserSystem, on_delete=models.CASCADE, verbose_name="所属用户体系", null=True, blank=True)')

# Remove ServiceUser
start_marker = 'class ServiceUser(BaseModel):'
if start_marker in content:
    start_idx = content.find(start_marker)
    # Find the end of the class (next class definition or end of file)
    next_class = content.find('class ', start_idx + len(start_marker))
    if next_class != -1:
        content = content[:start_idx] + content[next_class:]
    else:
        content = content[:start_idx]

# Remove AbstractBaseServiceUserModel
start_marker = 'class AbstractBaseServiceUserModel(BaseModel):'
if start_marker in content:
    start_idx = content.find(start_marker)
    next_class = content.find('class ', start_idx + len(start_marker))
    if next_class != -1:
        content = content[:start_idx] + content[next_class:]
    else:
        content = content[:start_idx]

with open(service_file, 'w', encoding='utf-8') as f:
    f.write(content)
