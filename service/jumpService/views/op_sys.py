# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/8/2
@Software: PyCharm
@disc:
======================================="""

import binascii
import html
import os
import re
import platform
import subprocess
import tempfile
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
    # 判断是否为 Windows 系统
    is_windows = obj.image and "Windows" in obj.image.name
    # 如果是 Windows 默认 RDP 端口 3389，否则使用 SSH 端口
    conn_port = 3389 if is_windows else obj.remoteAccessPort
    
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
        host_port_map[str(ip_port.ip)]=conn_port
    for i, port_map in enumerate(port_maps):
        if port_map.rightPort == conn_port:
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
                    <button type="button" class="btn-ssh" onclick="handleOpenSsh()">
                        %s
                    </button>
                </div>
                <script src="/static/js/SSH-utils.js"></script>
                <script>
                    const IS_WINDOWS = %s;
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
                        
                        if (IS_WINDOWS) {
                            openRdp(host, port, username, password, title);
                        } else {
                            openSsh(host, port, username, password, title);
                        }
                    }
                </script>
            </body>
            </html>
               ''' % (IPOptions, UserOptions, "打开远程桌面" if is_windows else "打开 SSH 客户端", "true" if is_windows else "false")
    return HttpResponse(html_txt)


@csrf_exempt
def rdp_open(request):
    """
    针对 macOS 客户端，生成 .rdp 文件并使用 open 命令打开
    """
    if request.method == 'POST':
        host = request.POST.get('host')
        port = request.POST.get('port')
        username = request.POST.get('username')
        password = request.POST.get('password')
        title = request.POST.get('title', 'connection')

        # 清理 title 确保其作为文件名是安全的
        safe_title = re.sub(r'[\\/*?:"<>|]', '_', title)

        # 针对 password 51:b: 格式，需要将密码转换为 UTF-16LE 编码的二进制，再转为 Hex 字符串
        password_bytes = password.encode('utf-16-le')
        hex_password = binascii.hexlify(password_bytes).decode('ascii')

        # 构造 .rdp 文件内容
        rdp_content = f"full address:s:{host}:{port}\n" \
                      f"username:s:{username}\n" \
                      f"password 51:b:{hex_password}\n" \
                      f"prompt for credentials:i:0\n" \
                      f"authentication level:i:0\n"

        # 创建带有特定名称的临时文件
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"{safe_title}.rdp")
        
        with open(temp_path, 'wb') as f:
            f.write(rdp_content.encode('utf-8'))

        try:
            current_os = platform.system()
            if current_os == 'Darwin':
                # macOS 使用 open 命令
                subprocess.run(['open', temp_path], check=True)
            elif current_os == 'Windows':
                # Windows 环境下如果也想用这种方式，可以使用 mstsc
                subprocess.run(['mstsc', temp_path], check=True)
            else:
                return HttpResponse(f"Unsupported OS: {current_os}", status=400)
            
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(str(e), status=500)

    return HttpResponse(status=405)
