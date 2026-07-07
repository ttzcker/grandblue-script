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
    context.close()