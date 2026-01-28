
/**
 * 触发 SSH 协议跳转
 * @param {string} host 主机 IP
 * @param {number} port 端口
 * @param {string} username 用户名
 * @param {string} password 密码
 * @param {string} title 窗口标题
 */
function openSsh(host, port, username, password, title) {
    const encodedPassword = password ? encodeURIComponent(password) : '';
    const authPart = encodedPassword ? `${username}:${encodedPassword}@` : `${username}@`;
    
    // 如果没有传入 title，则使用默认的
    const displayTitle = title || `Server-${host}`;
    const sshUrl = `ssh://${authPart}${host}:${port}?title=${encodeURIComponent(displayTitle)}`;
    // alert(sshUrl);
    console.log("正在尝试打开链接:", sshUrl);

    // 使用 <a> 标签模拟点击，并设置 target 为 _top
    // 这样浏览器会将其视为顶级窗口的导航，绕过对 iframe 内部 "嵌入凭据的子资源请求" 的拦截
    const link = document.createElement('a');
    link.href = sshUrl;
    link.target = '_top';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();

    // 延迟移除，确保点击事件已触发
    setTimeout(() => {
        if (link.parentNode) {
            document.body.removeChild(link);
        }
    }, 100);
}
