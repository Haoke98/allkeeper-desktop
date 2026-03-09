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
            width: 350px;
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
                </select>
            </div>
            <div style="margin-bottom: 20px;">
                <label style="display: flex; align-items: center; cursor: pointer;">
                    <input type="checkbox" id="new-window-check" style="margin-right: 8px;"> 
                    在新窗口打开 (New Window)
                </label>
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

        return modal;
    }

    window.openBrowserSelector = function(url) {
        const modal = createModal();
        const browserSelect = document.getElementById('browser-select');
        const newWindowCheck = document.getElementById('new-window-check');
        const openBtn = document.getElementById('open-btn');

        // Reset state
        browserSelect.value = 'default';
        newWindowCheck.checked = false;
        
        // Remove old listener to avoid duplicates
        const newBtn = openBtn.cloneNode(true);
        openBtn.parentNode.replaceChild(newBtn, openBtn);

        newBtn.addEventListener('click', () => {
            const browser = browserSelect.value;
            const newWindow = newWindowCheck.checked;
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
                    new_window: newWindow
                })
            })
            .then(response => response.json())
            .then(data => {
                newBtn.disabled = false;
                newBtn.innerText = '打开';
                if (data.status === 'success') {
                    modal.style.display = 'none';
                    // Optional: Show success toast
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
