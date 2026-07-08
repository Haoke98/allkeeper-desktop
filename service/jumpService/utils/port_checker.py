import requests
from django.utils import timezone
from ..models import Service

def check_port_status():
    services = Service.objects.all()
    for service in services:
        service.status = 'checking'
        service.save()
        
        ports_to_check = []
        if service.dashboardPort:
            ports_to_check.append(service.dashboardPort)
        if service.wafPort:
            ports_to_check.append(service.wafPort)
        
        all_ok = True
        for port in ports_to_check:
            try:
                # 实际检测逻辑需要根据具体服务调整
                response = requests.get(f"http://127.0.0.1:{port}/health", timeout=3)
                if response.status_code != 200:
                    all_ok = False
            except:
                all_ok = False
        
        service.status = 'ok' if all_ok else 'fail'
        service.lastChecked = timezone.now()
        service.save()