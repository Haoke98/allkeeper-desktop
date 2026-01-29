1. **更新 SSH-utils.js**:

   * 将 `openRdp` 中的协议从 `ms-rd://` 更换为官方支持的 `rdp://`。

   * 采用 `rdp://full%20address=s:host:port&username=s:user` 格式。

   * 保留 `strictEncodeURIComponent` 用于对用户名进行安全编码。

2. **更新 op\_sys.py**:

   * 保持现有的 `is_windows` 判断逻辑。

   * 确保 `conn_port` 在 Windows 下默认为 3389。

   * 确保 HTML 模板中正确传递了系统类型标识。

3. **用户告知**:

   * 说明由于微软安全策略，RDP 协议不支持在 URL 中直接传递密码，点击后需手动输入密码。

