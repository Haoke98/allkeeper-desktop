# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/8/2
@Software: PyCharm
@disc:
======================================="""
import base64

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import OperationSystem


@csrf_exempt
def ssh(request):
    print("Method:", request.method)
    print("GET:", request.GET)
    print("POST:", request.POST)
    _id = request.GET.get('id')
    obj = OperationSystem.objects.get(id=_id)
    ips = obj.server.ips.all()
    users = obj.users.all()
    # FIXME 这里需要先判断是否是Linux内核系统, 如果是Windows内核系统还得要用 远程桌面
    ssh_port = obj.sshPort
    for _ip in ips:

        if _ip.net is not None:
            if _ip.net.is_global():
                prefix = "公网"
            else:
                prefix = "内网"

    # FIXME:影响列表页的渲染, 增加延迟, 需要改成固定, 让用户在单个item的详情页里进行渲染, 在详情页中选入口/切换入口
    # TODO: 实现通过 lanproxy 的 API 实时创建端口映射关系.
    #  可以先查看有没有和当前服务器处在同一个网段的 lanproxy客户端, 也就是有没有可用的channels
    port_maps = obj.server.right_ports.all()
    for i, port_map in enumerate(port_maps):
        if i == 0:
            # print("port_map:")
            pass
        if port_map.rightPort == ssh_port:
            # print(" " * 10, "|", "-" * 10, f"{i}.", port_map)
            _ips = port_map.left.ips.all()
            for ip in _ips:
                # generate_modal(ip, port_map.leftPort)
                pass
    IPOptions = ""
    for i,_ip in enumerate(ips):
        selected = "selected" if i == 0 else ""
        IPOptions += f'<option value="{_ip.id}" data-ip="{_ip.ip}" {selected}>{_ip.ip}</option>'

    UserOptions = ""
    for i,_user in enumerate(users):
        selected = "selected" if i==0 else ""
        # 对密码进行转义防止 HTML 属性截断
        safe_pwd = _user.password.replace('"', '&quot;').replace("'", "&#39;")
        UserOptions += f'<option value="{_user.id}" data-username="{_user.username}" data-password="{safe_pwd}" {selected}>{_user.username}</option>'

    html_txt = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body { display: flex; flex-direction: column; padding: 20px; font-family: sans-serif; }
                    .controls { margin-bottom: 20px; display: flex; gap: 10px; align-items: center; }
                    select, button { padding: 8px; border-radius: 4px; border: 1px solid #ccc; }
                    .btn-ssh { background-color: #2196F3; color: white; border: none; cursor: pointer; }
                    .btn-ssh:hover { background-color: #0b7dda; }
                </style>
            </head>
            <body>
                <div class="controls">
                    <form method="post" action="" style="display: flex; gap: 10px;">
                        <select name="hostname">
                            %s
                        </select>
                        <select name="user">
                            %s
                        </select>
                    </form>
                    <button type="button" class="btn-ssh" onclick="handleOpenSsh()">打开 SSH 客户端</button>
                </div>
                <script src="/static/js/SSH-utils.js"></script>
                <script>
                    function handleOpenSsh() {
                        const hostSelect = document.getElementsByName('hostname')[0];
                        const userSelect = document.getElementsByName('user')[0];
                        
                        const selectedHost = hostSelect.options[hostSelect.selectedIndex];
                        const selectedUser = userSelect.options[userSelect.selectedIndex];
                        
                        if (!selectedHost || !selectedUser) {
                            alert("请先选择主机和用户");
                            return;
                        }
                        
                        const host = selectedHost.getAttribute('data-ip');
                        const username = selectedUser.getAttribute('data-username');
                        const password = selectedUser.getAttribute('data-password');
                        const port = %s;
                        
                        openSSH(host, port, username, password);
                    }
                </script>
            </body>
            </html>
               ''' % (IPOptions, UserOptions, ssh_port)
    return HttpResponse(html_txt)
