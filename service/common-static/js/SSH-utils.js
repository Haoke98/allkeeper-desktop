/**
 * 更加严格的编码函数（用于查询参数，如 title）
 * 确保所有在 URI 中具有特殊含义的字符都被百分比编码
 */
function strictEncodeURIComponent(str) {
    return encodeURIComponent(str).replace(/[!'()*,.]/g, function (c) {
        return '%' + c.charCodeAt(0).toString(16).toUpperCase();
    });
}

/**
 * 最小化编码函数（用于用户名和密码）
 * 绝大多数 SSH 客户端（如 Electerm）不会对 URI 的 user:pass 部分进行解码。
 * 因此我们只编码那些绝对会破坏 URI 结构的字符，而保留 . 和 , 等安全字符。
 */
function minimalEncode(str) {
    if (!str) return '';
    // 只编码: % (转义符), @ (分隔符), : (用户名密码分隔符), ? (查询参数开始), # (片段开始) 以及空格
    return str.replace(/[%@:?#\s]/g, function (c) {
        return encodeURIComponent(c);
    });
}

/**
 * 触发 SSH 协议跳转
 * @param {string} host 主机 IP
 * @param {number} port 端口
 * @param {string} username 用户名
 * @param {string} password 密码
 * @param {string} title 窗口标题
 */
function openSsh(host, port, username, password, title) {
    // 1. 对用户名和密码进行最小化编码，确保兼容不具备解码能力的客户端
    const encodedUser = minimalEncode(username);
    const encodedPassword = minimalEncode(password);
    
    // 2. 构造认证部分 [user[:pass]@]
    const authPart = encodedPassword ? `${encodedUser}:${encodedPassword}@` : `${encodedUser}@`;
    
    // 3. 构造标题（使用标准严格编码，因为 Electerm 会对查询参数进行解码）
    const displayTitle = title || `Server-${host}`;
    const sshUrl = `ssh://${authPart}${host}:${port}?title=${strictEncodeURIComponent(displayTitle)}`;
    // 调试日志（对密码脱敏）
    console.log("正在尝试打开兼容性链接:", sshUrl.replace(encodedPassword, '******'));

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
