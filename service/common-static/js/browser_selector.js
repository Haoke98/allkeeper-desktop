// Browser Selector Logic
(function() {
    function createModal() {
        const modalId = 'browser-selector-modal';
        if (document.getElementById(modalId)) return document.getElementById(modalId);

        const modal = document.createElement('div');
        modal.id = modalId;
        modal.style.cssText = `
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
            justify-content: center;
            align-items: center;
        `;

        const content = document.createElement('div');
        content.style.cssText = `
            background-color: #fefefe;
            margin: auto;
            padding: 20px;
            border: 1px solid #888;
            width: 400px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            font-family: Arial, sans-serif;
        `;

        content.innerHTML = `
            <h3 style="margin-top:0; margin-bottom: 15px; text-align: center;">选择浏览器打开</h3>
            <div style="margin-bottom: 15px;">
                <label style="display:block; margin-bottom:5px; font-weight: bold;">目标浏览器:</label>
                <select id="browser-select" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                    <option value="default">默认浏览器 (Default)</option>
                    <option value="chrome">Google Chrome</option>
                    <option value="safari">Safari</option>
                    <option value="firefox">Firefox</option>
                    <option value="edge">Microsoft Edge</option>
                    <option value="opera">Opera</option>
                    <option value="brave">Brave</option>
                </select>
            </div>
            <div style="margin-bottom: 20px;" id="window-select-container">
                <label style="display:block; margin-bottom:5px; font-weight: bold;">目标窗口:</label>
                <select id="window-select" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
                    <option value="new">新窗口 (New Window)</option>
                </select>
                <div id="window-loading" style="display:none; color: #666; font-size: 12px; margin-top: 4px;">正在获取窗口列表...</div>
            </div>
            <div style="text-align: right; border-top: 1px solid #eee; padding-top: 15px;">
                <button id="cancel-btn" style="margin-right: 10px; padding: 6px 12px; cursor: pointer; background: #fff; border: 1px solid #ddd; border-radius: 4px;">取消</button>
                <button id="open-btn" style="padding: 6px 15px; background-color: #409EFF; color: white; border: none; border-radius: 4px; cursor: pointer;">打开</button>
            </div>
        `;

        modal.appendChild(content);
        document.body.appendChild(modal);

        // Close when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.style.display = 'none';
        });

        document.getElementById('cancel-btn').addEventListener('click', () => {
            modal.style.display = 'none';
        });
        
        // Browser change event
        document.getElementById('browser-select').addEventListener('change', function() {
            const browser = this.value;
            fetchWindows(browser);
        });

        return modal;
    }

    function fetchWindows(browser) {
        const windowSelect = document.getElementById('window-select');
        const loadingDiv = document.getElementById('window-loading');
        
        // Reset options
        windowSelect.innerHTML = '<option value="new">新窗口 (New Window)</option>';
        
        if (browser === 'default' || browser === 'firefox') {
            // Default browser or Firefox (no window list support) just shows "New Window" (or implicit default)
            if (browser === 'default') {
                 // For default, "new" means force new window, otherwise it's standard open
                 windowSelect.innerHTML = '<option value="">当前/默认行为 (Default)</option><option value="new">新窗口 (New Window)</option>';
            }
            return;
        }

        loadingDiv.style.display = 'block';
        windowSelect.disabled = true;

        fetch(`/jump_service/service/browser/windows?browser=${browser}`)
            .then(response => response.json())
            .then(data => {
                loadingDiv.style.display = 'none';
                windowSelect.disabled = false;
                
                if (data.status === 'success' && data.windows) {
                    data.windows.forEach(win => {
                        const option = document.createElement('option');
                        option.value = win.id;
                        // Limit title length
                        let title = win.title || 'Untitled';
                        if (title.length > 50) title = title.substring(0, 47) + '...';
                        option.text = `窗口: ${title}`;
                        windowSelect.appendChild(option);
                    });
                } else if (data.status === 'error' && data.code === 'PERMISSION_DENIED') {
                    const option = document.createElement('option');
                    option.disabled = true;
                    option.text = '需要自动化权限 (Need Permission)';
                    windowSelect.appendChild(option);
                    alert("需要授予应用自动化控制浏览器的权限，请在系统偏好设置 > 安全性与隐私 > 自动化 中勾选。");
                }
            })
            .catch(err => {
                console.error('Failed to fetch windows', err);
                loadingDiv.style.display = 'none';
                loadingDiv.innerText = '获取失败';
                loadingDiv.style.display = 'block';
                windowSelect.disabled = false;
            });
    }

    function fetchInstalledBrowsers() {
        const browserSelect = document.getElementById('browser-select');
        // Keep default option if not already cleared
        let defaultOption = browserSelect.querySelector('option[value="default"]');
        if (!defaultOption) {
             defaultOption = document.createElement('option');
             defaultOption.value = 'default';
             defaultOption.text = '默认浏览器 (Default)';
        }
        
        fetch('/jump_service/service/browser/list')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' && data.browsers) {
                    // Rebuild options based on install status
                    browserSelect.innerHTML = '';
                    browserSelect.appendChild(defaultOption);
                    
                    const browsers = [
                        { key: 'chrome', label: 'Google Chrome' },
                        { key: 'safari', label: 'Safari' },
                        { key: 'firefox', label: 'Firefox' },
                        { key: 'edge', label: 'Microsoft Edge' },
                        { key: 'opera', label: 'Opera' },
                        { key: 'brave', label: 'Brave' }
                    ];
                    
                    browsers.forEach(b => {
                        // Check if browser exists in the returned list
                        if (data.browsers.hasOwnProperty(b.key)) {
                            const isInstalled = data.browsers[b.key];
                            const option = document.createElement('option');
                            option.value = b.key;
                            option.text = isInstalled ? b.label : `${b.label} (未安装/Not Installed)`;
                            if (!isInstalled) {
                                option.disabled = true;
                                option.style.color = '#999';
                            }
                            browserSelect.appendChild(option);
                        }
                    });
                    
                    // Restore selection if possible, else default
                    browserSelect.value = 'default';
                }
            })
            .catch(err => console.error('Failed to fetch installed browsers', err));
    }

    window.openBrowserSelector = function(url) {
        const modal = createModal();
        const browserSelect = document.getElementById('browser-select');
        const windowSelect = document.getElementById('window-select');
        const openBtn = document.getElementById('open-btn');

        // Fetch installed browsers status
        fetchInstalledBrowsers();

        // Reset state
        browserSelect.value = 'default';
        fetchWindows('default'); // Reset window list
        
        // Remove old listener to avoid duplicates
        const newBtn = openBtn.cloneNode(true);
        openBtn.parentNode.replaceChild(newBtn, openBtn);

        newBtn.addEventListener('click', () => {
            const browser = browserSelect.value;
            const windowId = windowSelect.value;
            const urlToOpen = url;

            // Show loading state
            newBtn.disabled = true;
            newBtn.innerText = '打开中...';

            // Call Backend API
            fetch('/jump_service/service/open', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    url: urlToOpen,
                    browser: browser,
                    window_id: windowId
                })
            })
            .then(response => response.json())
            .then(data => {
                newBtn.disabled = false;
                newBtn.innerText = '打开';
                if (data.status === 'success') {
                    modal.style.display = 'none';
                } else {
                    alert('打开失败: ' + data.message);
                }
            })
            .catch(error => {
                newBtn.disabled = false;
                newBtn.innerText = '打开';
                console.error('Error:', error);
                alert('请求失败，请检查网络或后端服务');
            });
        });

        modal.style.display = 'flex';
    };

    // Helper to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Event delegation for dynamically added links
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('browser-selector')) {
            e.preventDefault();
            const url = e.target.getAttribute('data-url');
            if (url) {
                window.openBrowserSelector(url);
            }
        }
    });
})();
