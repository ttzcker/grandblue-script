from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.firefox.launch_persistent_context(
        user_data_dir=r"C:\playwright_firefox_profile",
        headless=False
    )

    page = context.new_page()

    # ===== 初始进入 =====
    page.goto("https://game.granbluefantasy.jp/#mypage/")
    page.goto("https://game.granbluefantasy.jp/#quest/assist")
    page.wait_for_timeout(2000)

    print("开始自动流程...")

    while True:
        page.reload()
        page.goto("https://game.granbluefantasy.jp/#quest/assist")
        page.wait_for_timeout(2000)
        # ===== 找副本并点击 =====
        found = page.evaluate("""
        () => {
            const min = 5;
            const max = 15;

            let best = null;
            let bestDiff = Infinity;

            document.querySelectorAll('.btn-multi-raid').forEach(btn => {
                const gauge = btn.querySelector('.prt-raid-gauge-inner');
                if (gauge && gauge.style.width) {
                    const hp = parseInt(gauge.style.width);
                    if (hp >= min && hp <= max) {
                        const diff = hp - min;
                        if (diff < bestDiff) {
                            bestDiff = diff;
                            best = btn;
                        }
                    }
                }
            });

            if (best) {
                best.scrollIntoView({block: "center"});

                const rect = best.getBoundingClientRect();
                const x = rect.left + rect.width / 2;
                const y = rect.top + rect.height / 2;

                const target = document.elementFromPoint(x, y);

                if (target) {
                    target.dispatchEvent(new MouseEvent("mousedown", {bubbles: true, clientX: x, clientY: y}));
                    target.dispatchEvent(new MouseEvent("mouseup", {bubbles: true, clientX: x, clientY: y}));
                    target.dispatchEvent(new MouseEvent("click", {bubbles: true, clientX: x, clientY: y}));
                    return true;
                }
            }
            return false;
        }
        """)

        if not found:
            print("没找到副本 → 刷新")
            page.wait_for_timeout(2000)
            continue

        print("找到副本，已点击")
        page.wait_for_timeout(3000)

        # ===== 点击 OK =====
        page.evaluate("""
        () => {
            const btn = document.querySelector('.btn-usual-ok.se-quest-start, .btn-usual-ok');
            if (btn) {
                btn.scrollIntoView({block: "center", inline: "center"});

                const rect = btn.getBoundingClientRect();
                const x = rect.left + rect.width / 2;
                const y = rect.top + rect.height / 2;

                const target = document.elementFromPoint(x, y);

                if (target) {
                    target.dispatchEvent(new MouseEvent("mousedown", {bubbles: true, clientX: x, clientY: y}));
                    target.dispatchEvent(new MouseEvent("mouseup", {bubbles: true, clientX: x, clientY: y}));
                    target.dispatchEvent(new MouseEvent("click", {bubbles: true, clientX: x, clientY: y}));
                }
            }
        }
        """)

        print("尝试点击 OK")

        print("尝试点击 OK")
        page.wait_for_timeout(3000)

        # ===== 点 AUTO =====
        try:
            page.wait_for_selector(".btn-auto", timeout=5000)
            page.click(".btn-auto")
            print("已开启 AUTO")
        except:
            page.goto("https://game.granbluefantasy.jp/#quest/assist")
            page.reload()
            print("没找到 AUTO")
            continue
    

        # ===== 战斗中 =====
        print("战斗中...")
        page.wait_for_timeout(1000)
