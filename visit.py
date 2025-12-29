from playwright.sync_api import sync_playwright

def force_wake():
    with sync_playwright() as p:
        # 模拟真实的浏览器，带有合法的指纹
        browser = p.chromium.launch(headless=True)
        # 关键：使用特定的 User-Agent 和 Locale
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("正在模拟真实浏览器访问...")
        # 访问主页，这会自动处理所有的 Cookie 和重定向逻辑
        page.goto("https://aseava.streamlit.app/", wait_until="networkidle")
        
        # 寻找“Wake up”按钮并模拟真实点击
        # 这一步会产生你抓包看到的那个 POST /resume
        wake_button = page.get_by_text("Wake up", exact=False)
        if wake_button.is_visible():
            wake_button.click()
            print("成功点击唤醒按钮！")
            page.wait_for_timeout(5000) # 等待 5 秒确认状态
        else:
            print("未发现唤醒按钮，App 可能已在线。")
            
        browser.close()

force_wake()
