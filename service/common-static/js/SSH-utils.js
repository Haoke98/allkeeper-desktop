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

/**
 * 复制文本到剪贴板
 * @param {string} text 
 */
function copyToClipboard(text) {
    if (!text) return;
    
    // 优先使用现代 Clipboard API
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('密码已成功复制到剪贴板');
        }).catch(err => {
            console.error('无法复制代码到剪贴板: ', err);
        });
    } else {
        // 兜底方案：使用传统的 textarea 方式
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            console.log('密码已成功复制到剪贴板 (兜底方案)');
        } catch (err) {
            console.error('无法复制代码到剪贴板 (兜底方案): ', err);
        }
        document.body.removeChild(textArea);
    }
}

/**
 * 触发远程桌面 (RDP) 协议跳转
 * 根据当前客户端操作系统环境选择不同的处理方式
 * @param {string} host 主机 IP
 * @param {number} port 端口
 * @param {string} username 用户名
 * @param {string} password 密码
 * @param {string} title 窗口标题
 */
function openRdp(host, port, username, password, title) {
    // 自动将密码复制到剪贴板，方便用户在客户端弹出框中直接粘贴
    copyToClipboard(password);
    
    const userAgent = window.navigator.userAgent.toLowerCase();
    const isMac = userAgent.includes('macintosh') || userAgent.includes('mac os x');

    if (isMac) {
        // 如果是 macOS 环境，调用后端接口生成 .rdp 文件并执行 open 命令
        console.log("检测到 macOS 环境，正在通过后端生成 RDP 文件并打开...");
        
        const formData = new URLSearchParams();
        formData.append('host', host);
        formData.append('port', port);
        formData.append('username', username);
        formData.append('password', password);

        fetch('/jump_service/op_sys/rdp/open', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData.toString()
        }).then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            console.log("RDP 文件已成功在 macOS 上打开");
        }).catch(error => {
            console.error("无法打开 RDP 连接:", error);
            alert("无法打开 RDP 连接: " + error.message);
        });
    } else {
        // 如果是 Windows 环境，继续使用标准的 rdp:// 协议唤醒
        console.log("检测到 Windows 环境，正在通过 rdp:// 协议唤醒...");
        
        // 格式: rdp://full%20address=s:host:port&username=s:user
        const encodedUser = encodeURIComponent(username);
        const rdpUrl = `rdp://full%20address=s:${host}:${port}&username=s:${encodedUser}`;

        console.log("正在尝试通过标准协议唤醒 RDP:", rdpUrl);
        window.location.href = rdpUrl;
    }
}
