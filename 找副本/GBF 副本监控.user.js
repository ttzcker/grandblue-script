// ==UserScript==
// @name GBF 副本监控（全自动稳定版）
// @namespace http://tampermonkey.net/
// @version 11.3
// @match *://*.granbluefantasy.jp/*
// @run-at document-end
// @grant none
// ==/UserScript==

(function() {
    'use strict';

    // ===== 创建面板 =====
    function createPanel() {
        if (document.getElementById("gbf-panel")) return;
        const panel = document.createElement("div");
        panel.id = "gbf-panel";
        panel.style.position = "fixed";
        panel.style.top = localStorage.getItem("gbf_panel_top") || "10px";
        panel.style.left = localStorage.getItem("gbf_panel_left") || "10px";
        panel.style.width = "270px";
        panel.style.background = "rgba(0,0,0,0.85)";
        panel.style.color = "#0f0";
        panel.style.padding = "10px";
        panel.style.zIndex = 9999;
        panel.style.fontSize = "12px";
        panel.style.cursor = "move";
        panel.innerHTML = `
        <b>副本监控</b><br><br>
        最低血量: <input id="minHp" type="number" style="width:60px;"><br><br>
        最高血量: <input id="maxHp" type="number" placeholder="可不填" style="width:60px;"><br><br>
        <label>
            <input type="checkbox" id="autoStart">
            自动点击开始
        </label><br><br>
        <button id="findBtn">查找并进入</button>
        <button id="homeBtn">主页</button>
        <hr>
        <div id="list"></div>
        `;
        document.body.appendChild(panel);
    }

    // ===== 读取设置 =====
    function loadSettings() {
        const min = localStorage.getItem("gbf_minHp");
        const max = localStorage.getItem("gbf_maxHp");
        const auto = localStorage.getItem("gbf_autoStart");
        document.getElementById("minHp").value = min || 50;
        document.getElementById("maxHp").value = max || "";
        document.getElementById("autoStart").checked = auto !== null ? auto === "true" : true;
    }

    // ===== 保存设置 =====
    function saveSettings() {
        localStorage.setItem("gbf_minHp", document.getElementById("minHp").value);
        localStorage.setItem("gbf_maxHp", document.getElementById("maxHp").value);
        localStorage.setItem("gbf_autoStart", document.getElementById("autoStart").checked);
    }

    // ===== 拖动 =====
    function enableDrag() {
        const panel = document.getElementById("gbf-panel");
        let isDragging = false;
        let offsetX, offsetY;
        panel.addEventListener("mousedown", (e) => {
            isDragging = true;
            offsetX = e.clientX - panel.offsetLeft;
            offsetY = e.clientY - panel.offsetTop;
        });
        document.addEventListener("mousemove", (e) => {
            if (!isDragging) return;
            panel.style.left = (e.clientX - offsetX) + "px";
            panel.style.top = (e.clientY - offsetY) + "px";
        });
        document.addEventListener("mouseup", () => {
            if (isDragging) {
                isDragging = false;
                localStorage.setItem("gbf_panel_left", panel.style.left);
                localStorage.setItem("gbf_panel_top", panel.style.top);
            }
        });
    }

    // ===== 更新列表 =====
    function updateList() {
        const list = document.getElementById("list");
        if (!list) return;
        list.innerHTML = "";
        document.querySelectorAll('.btn-multi-raid').forEach(btn => {
            const name = btn.querySelector('.txt-raid-name')?.innerText;
            const people = btn.querySelector('.prt-flees-in')?.innerText;
            const gauge = btn.querySelector('.prt-raid-gauge-inner');
            if (gauge && gauge.style.width) {
                const hp = parseInt(gauge.style.width);
                list.innerHTML += `${name} | ${people} | ${hp}%<br>`;
            }
        });
    }

    // ===== 稳定点击函数 =====
    function safeClick(element, afterClick) {
        let attempts = 0;
        const timer = setInterval(() => {
            attempts++;
            if (!element || attempts > 6) {
                clearInterval(timer);
                return;
            }
            element.scrollIntoView({block: "center"});
            const rect = element.getBoundingClientRect();
            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;
            const target = document.elementFromPoint(x, y);
            if (target) {
                target.dispatchEvent(new MouseEvent("mousedown", {bubbles: true, clientX: x, clientY: y}));
                target.dispatchEvent(new MouseEvent("mouseup", {bubbles: true, clientX: x, clientY: y}));
                target.dispatchEvent(new MouseEvent("click", {bubbles: true, clientX: x, clientY: y}));
                clearInterval(timer);
                if (afterClick) setTimeout(afterClick, 1000);
            }
        }, 400);
    }

    // ===== 智能点击OK（成功点击后不再重复点击）=====
    let okClicked = false;   // 全局标记，防止重复点击

    function tryClickOK() {
        if (!document.getElementById("autoStart")?.checked || okClicked) return;

        let attempts = 0;
        const maxAttempts = 5;

        const checkInterval = setInterval(() => {
            if (okClicked) {
                clearInterval(checkInterval);
                return;
            }

            attempts++;
            const btn = document.querySelector('.btn-usual-ok.se-quest-start, .btn-usual-ok');

            if (btn) {
                console.log(`找到OK按钮并点击（第${attempts}次检查）`);
                okClicked = true;           // 标记已点击成功
                safeClick(btn);
                clearInterval(checkInterval);
                return;
            }

            if (attempts >= maxAttempts) {
                console.log("未找到OK按钮，已停止检查");
                clearInterval(checkInterval);
            }
        }, 1000);
    }

    // ===== 绑定事件 =====
    function bindEvents() {
        document.getElementById("minHp").addEventListener("input", saveSettings);
        document.getElementById("maxHp").addEventListener("input", saveSettings);
        document.getElementById("autoStart").addEventListener("change", saveSettings);

        document.getElementById("findBtn").onclick = () => {
            const min = parseInt(document.getElementById("minHp").value);
            const maxInput = document.getElementById("maxHp").value;
            const max = maxInput ? parseInt(maxInput) : null;

            let best = null;
            let bestDiff = Infinity;

            document.querySelectorAll('.btn-multi-raid').forEach(btn => {
                const gauge = btn.querySelector('.prt-raid-gauge-inner');
                if (gauge && gauge.style.width) {
                    const hp = parseInt(gauge.style.width);
                    if (hp >= min && (max === null || hp <= max)) {
                        const diff = hp - min;
                        if (diff < bestDiff) {
                            bestDiff = diff;
                            best = btn;
                        }
                    }
                }
            });

            if (best) {
                best.style.border = "3px solid yellow";
                okClicked = false;
                safeClick(best, tryClickOK);
            } else {
                console.log("没找到副本 → 自动刷新");
                const refreshBtn = document.querySelector('.btn-search-refresh');
                if (refreshBtn) safeClick(refreshBtn);
            }
        };

        document.getElementById("homeBtn").onclick = () => {
            localStorage.setItem("gbf_trigger_auto", "1");
            window.location.href = "https://game.granbluefantasy.jp/#quest/assist";
        };
    }

    function init() {
        createPanel();
        loadSettings();
        bindEvents();
        enableDrag();
    }

    setTimeout(init, 2000);
    setInterval(updateList, 2000);
})();
