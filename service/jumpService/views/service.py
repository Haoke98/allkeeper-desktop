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
    html_str += """
    <style>
        table {
            width: 100%;  /* 使表格宽度自适应 */
            border-collapse: collapse;  /* 合并边框 */
        }
        th, td {
            padding: 10px;  /* 添加内边距 */
            text-align: left;  /* 左对齐 */
            border: 1px solid #ddd;  /* 添加边框 */
            overflow: hidden;  /* 隐藏溢出内容 */
            white-space: nowrap;  /* 不换行 */
            text-overflow: ellipsis;  /* 超出部分用省略号表示 */
        }
        th {
            background-color: #f2f2f2;  /* 表头背景色 */
        }
        .password-column {
            width: 200px;  /* 设置密码列的固定宽度 */
            text-align: center;
        }
        .toast {
            visibility: hidden;  /* 默认隐藏 */
            min-width: 250px;  /* 最小宽度 */
            margin-left: -125px;  /* 居中 */
            background-color: #333;  /* 背景色 */
            color: #fff;  /* 字体颜色 */
            text-align: center;  /* 中间对齐 */
            border-radius: 2px;  /* 圆角 */
            padding: 16px;  /* 内边距 */
            position: fixed;  /* 固定位置 */
            z-index: 1;  /* 层级 */
            left: 50%;  /* 居中 */
            bottom: 30px;  /* 距离底部 */
        }
        .toast.show {
            visibility: visible;  /* 显示 */
            animation: fadein 0.5s, fadeout 0.5s 2.5s;  /* 动画效果 */
        }
        @keyframes fadein {
            from {bottom: 0; opacity: 0;}  /* 从底部渐变 */
            to {bottom: 30px; opacity: 1;}  /* 到达目标位置 */
        }
        @keyframes fadeout {
            from {bottom: 30px; opacity: 1;}  /* 从目标位置渐变 */
            to {bottom: 0; opacity: 0;}  /* 到达底部 */
        }
    </style>
    """
    html_str += "<tbody>"
    for user in users:
        html_str += '''
        <tr>
            <td title="%s">%s</td>
            <td title="%s">%s</td>
            <td class="password-column">
                <span id='password-display-%s'>%s</span>
                <span id='password-%s' style='display:none;'>%s</span>
            </td>
            <td>
                <button onclick='copyUsername(\"%s\")'>复制用户名</button>
                <button onclick='copyPassword(\"%s\")'>复制密码</button>
                <button onclick='togglePassword(\"%s\")'>预览密码</button>
            </td>
            <td title="%s">%s</td>
        </tr>''' % (
            user.id, user.id, user.username, user.username, 
            user.id, PASSWORD_PLACEHOLDER, user.id, user.password, 
            user.username, user.id, user.id, escapejs(user.remark), escapejs(user.remark))
    html_str += "</tbody></table>"
    html_str += """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        function showToast(message) {
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerText = message;
            document.body.appendChild(toast);
            setTimeout(() => {
                toast.className = 'toast show';
            }, 100);
            setTimeout(() => {
                toast.className = 'toast';
                document.body.removeChild(toast);
            }, 3000);
        }

        function copyPassword(userId) {
            const password = document.getElementById('password-' + userId).innerText;
            navigator.clipboard.writeText(password).then(() => {
                showToast('密码已复制到剪贴板');
            }).catch(err => {
                console.error('复制失败:', err);
            });
        }

        function copyUsername(username) {
            navigator.clipboard.writeText(username).then(() => {
                showToast('用户名已复制到剪贴板');
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
