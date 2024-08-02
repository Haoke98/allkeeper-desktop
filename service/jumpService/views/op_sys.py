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
    ssh_services = obj.server.SSHServices.all()
    users = obj.users.all()
    # FIXME 这里需要先判断是否是Linux内核系统, 如果是Windows内核系统还得要用 远程桌面
    # print("ssh_services:", ssh_services)
    ssh_port = 22
    if ssh_services.__len__() > 0:
        ssh_port = ssh_services[0].port

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
    submit_txt = "连接"
    iframe = ""
    selectedHostId = request.POST.get('hostname')
    selectedUserId = request.POST.get('user')
    if request.method == 'POST':
        _ip = ips.filter(id=request.POST.get('hostname')).first()
        # FIXME: 记得及时修复, 从SystemUser选择进行
        hostname = _ip.ip
        user = users.filter(id=request.POST.get('user')).first()
        username = user.username
        # FIXME: 部分root账户会有密钥登录方式, 密码登录无法成功
        password = user.password
        print(username, password)
        # Base64编码
        encoded_pwd = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        # FIXME: [高危敏感信息泄漏漏洞] 必须即使改成后端创建session后,再从前端通过session访问.
        # 这里的url可以写死，也可以用django的反向获取url，可以根据model的数据，传到url中
        web_ssh_url = "http://localhost:9080?hostname={}&port={}&username={}&password={}".format(hostname, ssh_port,
                                                                                                 username,
                                                                                                 encoded_pwd)
        iframe = f'''<iframe src="{web_ssh_url}" style="width:100%;height:92vh;"/>'''
        submit_txt = "重新连接"
    IPOptions = ""
    for _ip in ips:
        IPOptions += "<option value='" + str(_ip.id)
        if _ip.id == selectedHostId:
            IPOptions += "' selected>"
        else:
            IPOptions += "' >"
        IPOptions += str(_ip.ip) + "</option>"
    UserOptions = ""
    for _user in users:
        UserOptions += "<option value='" + str(_user.id)
        if _user.id == selectedUserId:
            UserOptions += "' selected>"
        else:
            UserOptions += "' >"
        UserOptions += str(_user.username) + "</option>"
    html_txt = f'''
            <!DOCTYPE html>
            <body style="display=flex;">
                <form method="post" action="">
                    <div>
                        <select name="hostname">
                            {IPOptions}
                        </select>
                        <select name="user">
                            {UserOptions}
                        </select>
                        <button type="submit">{submit_txt}</button>
                    <div>
                </form>
                {iframe}
            <body>
               '''
    return HttpResponse(html_txt)
