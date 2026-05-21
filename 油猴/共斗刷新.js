// ==UserScript==
// @name         GBF 自动显示 Invite + 自动切换
// @namespace    http://tampermonkey.net/
// @version      2.2
// @match        https://game.granbluefantasy.jp/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    let scriptEnabled = false;   // 默认

    function triggerTouch(el) {
        if (!el) return;
        ['touchstart', 'touchend', 'mousedown', 'mouseup', 'click'].forEach(type => {
            el.dispatchEvent(new Event(type, { bubbles: true, cancelable: true }));
        });
    }

    function toggleInvite() {
        if (!scriptEnabled) return;

        const offChecked = document.querySelector('.btn-invite-check.checked[data-invite="off"]');
        const onBtn = document.querySelector('.btn-invite-check[data-invite="on"]');
        const onChecked = document.querySelector('.btn-invite-check.checked[data-invite="on"]');

        if (offChecked && onBtn) {
            console.log('Invite 当前关闭 → 切换为开启');
            triggerTouch(onBtn);
        }
        else if (onChecked) {
            console.log('Invite 当前开启 → 切换为关闭');
            const offBtn = offChecked || document.querySelector('.btn-invite-check[data-invite="off"]');
            triggerTouch(offBtn);
        }
    }

    // ==================== 控制面板 ====================
    function createControlPanel() {
        const panel = document.createElement('div');
        panel.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 999999;
            border: 2px solid #e0b070;
            box-shadow: 0 0 10px rgba(0,0,0,0.8);
            user-select: none;
            display: flex;
            align-items: center;
            gap: 10px;
        `;

        const label = document.createElement('span');
        label.textContent = 'Invite 自动切换';
        label.style.fontWeight = 'bold';

        const toggleBtn = document.createElement('button');
        toggleBtn.textContent = scriptEnabled ? 'ON' : 'OFF';
        toggleBtn.style.cssText = `
            padding: 6px 14px;
            border-radius: 6px;
            border: none;
            font-weight: bold;
            cursor: pointer;
            background: ${scriptEnabled ? '#4caf50' : '#f44336'};
            color: white;
        `;

        toggleBtn.addEventListener('click', () => {
            scriptEnabled = !scriptEnabled;
            toggleBtn.textContent = scriptEnabled ? 'ON' : 'OFF';
            toggleBtn.style.background = scriptEnabled ? '#4caf50' : '#f44336';
            console.log(`Invite 自动切换脚本已 ${scriptEnabled ? '启用' : '禁用'}`);
        });

        panel.appendChild(label);
        panel.appendChild(toggleBtn);
        document.body.appendChild(panel);

        // 可拖动
        let isDragging = false;
        let offsetX, offsetY;
        panel.addEventListener('mousedown', e => {
            if (e.target === toggleBtn) return;
            isDragging = true;
            offsetX = e.clientX - panel.offsetLeft;
            offsetY = e.clientY - panel.offsetTop;
        });

        document.addEventListener('mousemove', e => {
            if (isDragging) {
                panel.style.right = 'auto';
                panel.style.left = (e.clientX - offsetX) + 'px';
                panel.style.top = (e.clientY - offsetY) + 'px';
            }
        });

        document.addEventListener('mouseup', () => isDragging = false);
    }

    // ==================== 启动 ====================
    setInterval(toggleInvite, 600);

    // 页面加载后创建面板并首次执行
    window.addEventListener('load', () => {
        setTimeout(() => {
            createControlPanel();
            toggleInvite();
        }, 1500);
    });

    // 兼容 SPA 页面切换
    let lastUrl = location.href;
    new MutationObserver(() => {
        if (location.href !== lastUrl) {
            lastUrl = location.href;
            setTimeout(toggleInvite, 1000);
        }
    }).observe(document, { subtree: true, childList: true });

})();
