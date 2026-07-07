from playwright.sync_api import sync_playwright
import time
a="https://game.granbluefantasy.jp/#quest/supporter/943771/1/0/10116"


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
            page.wait_for_selector(".btn-attack-start", timeout=10000)
            print("找到攻击按钮，开始监控状态...")
            start_time = time.time()

            
            while True:
                status = page.evaluate("""
                () => {
                    const btn = document.querySelector('.btn-attack-start');
                    if (!btn) return null;
                    return btn.className;
                }   
                """)
                if status and "display-off" in status:
                    print("攻击按钮已变为 display-off → 执行下一步")

                    break     
                page.wait_for_timeout(500)  # 每0.5秒检查一次 

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

