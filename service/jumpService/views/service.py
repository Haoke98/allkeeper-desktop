# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/19
@Software: PyCharm
@disc:
======================================="""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.html import escapejs

from ..models import ServiceUser


@login_required
def get_users(request):
    # FIXME: 该方法返回内容涉及到敏感数据, 需要进行鉴权, 目前是可以公开访问的, 这是一个超严重的BUG
    serviceId = request.GET.get('serviceId')
    if serviceId is None:
        return HttpResponse("参数异常/参数缺漏", status=400)
    users = ServiceUser.objects.filter(service_id=serviceId).all()
    PASSWORD_PLACEHOLDER = '* * * * * * * * * *'
    html_str = '<table border="1">'
    html_str += "<thead><td>ID</td><td>用户名</td><td>密码</td><td>操作</td><td>备注</td></thead>"
    html_str += "<tbody>"
    for user in users:
        html_str += '''
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>
                <span id='password-display-%s'>%s</span>
                <span id='password-%s' style='display:none;'>%s</span>
            </td>
            <td>
                <button onclick='copyUsername(\"%s\")'>复制用户名</button>
                <button onclick='copyPassword(\"%s\")'>复制密码</button>
                <button onclick='togglePassword(\"%s\")'>预览密码</button>
            </td>
            <td>%s</td>
        </tr>''' % (
            user.id, escapejs(user.username), user.id, PASSWORD_PLACEHOLDER,user.id, escapejs(user.password), 
            escapejs(user.username),
            user.id,
            user.id,
            escapejs(user.remark))
    html_str += "</tbody></table>"
    html_str += """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        function copyPassword(userId) {
            const password = document.getElementById('password-' + userId).innerText;
            navigator.clipboard.writeText(password).then(() => {
                alert('密码已复制到剪贴板');
            }).catch(err => {
                console.error('复制失败:', err);
            });
        }

        function copyUsername(username) {
            navigator.clipboard.writeText(username).then(() => {
                alert('用户名已复制到剪贴板');
            }).catch(err => {
                console.error('复制失败:', err);
            });
        }

        function togglePassword(userId) {
            const passwordSpan = document.getElementById('password-display-' + userId);
            const currentDisplay = passwordSpan.innerText;
            if (currentDisplay === '%s') {
                passwordSpan.innerText = document.getElementById('password-' + userId).innerText;
            } else {
                passwordSpan.innerText = '%s';
            }
        }

        window.copyPassword = copyPassword;
        window.copyUsername = copyUsername;
        window.togglePassword = togglePassword;
    });
    </script>
    """ % (PASSWORD_PLACEHOLDER, PASSWORD_PLACEHOLDER)
    return HttpResponse(html_str)
