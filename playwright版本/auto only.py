from playwright.sync_api import sync_playwright

#a="https://game.granbluefantasy.jp/#quest/supporter/943321/1"
a="https://game.granbluefantasy.jp/#quest/supporter/943331/1/0/10652"

with sync_playwright() as p:
    context = p.firefox.launch_persistent_context(
        user_data_dir=r"C:\playwright_firefox_profile",
        headless=False
    )

    page = context.new_page()

    # ===== 初始进入 =====
    page.goto("https://game.granbluefantasy.jp/#mypage/")
    page.goto(a)
    page.wait_for_timeout(3000)
    print("开始自动流程...")

    while True:
        page.goto(a)
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
        print("点击ok")
        
        # ===== 点 AUTO =====
        try:
            page.wait_for_selector(".btn-auto", timeout=10000)
            page.click(".btn-auto")
            print("已开启 AUTO")
            page.wait_for_timeout(1000)
            page.goto(a)
            print("跳转")
            page.wait_for_timeout(1000)
            page.goto(a)
            print("跳转")
            page.wait_for_timeout(1000)
            continue



  
        except:
            print("没找到 AUTO")
            continue        

