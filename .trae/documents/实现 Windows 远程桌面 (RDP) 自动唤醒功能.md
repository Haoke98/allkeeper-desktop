1. **修改 op\_sys.py**:

   * 在视图函数中通过 `obj.image.name` 判断是否为 Windows 系统。

   * 根据系统类型动态设置 `default_port`（Windows 默认为 3389，Linux 默认为 SSH 端口）。

   * 在 HTML 模板中注入 `is_windows` 标识，并根据该标识切换按钮文字和点击事件。

2. **修改 SSH-utils.js**:

   * 新增 `openRdp` 函数。

   * 使用 `ms-rd://cmd?v=host:port&u=username&p=password` 格式构造远程桌面协议链接。

   * 保持与 `openSsh` 一致的安全跳转逻辑（使用隐藏 `<a>` 标签并设置 `target="_top"`）。

3. **前端调用逻辑**:

   * 在 `handleOpenSsh`（可重命名为更通用的名称）中，根据后端传入的 `os_type` 决定调用 `openSsh` 还是 `openRdp`。

