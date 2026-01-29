# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/8/2
@Software: PyCharm
@disc:
======================================="""

import html

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
    for ip_port in ips:
        if ip_port.net is not None:
            if ip_port.net.is_global():
                prefix = "公网"
            else:
                prefix = "内网"

    # FIXME:影响列表页的渲染, 增加延迟, 需要改成固定, 让用户在单个item的详情页里进行渲染, 在详情页中选入口/切换入口
    # TODO: 实现通过 lanproxy 的 API 实时创建端口映射关系.
    #  可以先查看有没有和当前服务器处在同一个网段的 lanproxy客户端, 也就是有没有可用的channels
    port_maps = obj.server.right_ports.all()
    host_port_map = {}
    for i,ip_port in enumerate(ips):
        host_port_map[str(ip_port.ip)]=ssh_port
    for i, port_map in enumerate(port_maps):
        if port_map.rightPort == ssh_port:
            # print(" " * 10, "|", "-" * 10, f"{i}.", port_map)
            _ips = port_map.left.ips.all()
            for ip in _ips:
                host_port_map[str(ip.ip)]=port_map.leftPort
    IPOptions = ""
    for i, (host, port) in enumerate(host_port_map.items()):
        selected = "selected" if i == 0 else ""
        # 窗口标题：备注 + IP
        remark = obj.server.remark if obj.server.remark else obj.server.code
        title = f"{remark} { host }".strip()
        _id = str(host)+":"+str(port)
        safe_id = html.escape(_id)
        safe_host = html.escape(str(host))
        safe_port = html.escape(str(port))
        safe_title = html.escape(title)
        IPOptions += f'<option value="{safe_id}" data-ip="{safe_host}" data-port="{safe_port}" data-title="{safe_title}" {selected}>{safe_id}</option>'

    UserOptions = ""
    for i,_user in enumerate(users):
        selected = "selected" if i==0 else ""
        # 使用 html.escape 确保所有字符在 HTML data 属性中安全
        safe_username = html.escape(_user.username)
        safe_password = html.escape(_user.password)
        UserOptions += f'<option value="{_user.id}" data-username="{safe_username}" data-password="{safe_password}" {selected}>{safe_username}</option>'

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
                        const port = selectedHost.getAttribute('data-port');
                        const title = selectedHost.getAttribute('data-title');
                        const username = selectedUser.getAttribute('data-username');
                        const password = selectedUser.getAttribute('data-password');
                        
                        openSsh(host, port, username, password, title);
                    }
                </script>
            </body>
            </html>
               ''' % (IPOptions, UserOptions)
    return HttpResponse(html_txt)
