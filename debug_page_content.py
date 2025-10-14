"""
Sahifa HTML va screenshot olish
"""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    page.context.clear_cookies()
    page.goto("https://dev.ishgo.uz")

    # Login
    page.get_by_role("button", name="Login").click()
    time.sleep(1)
    page.locator("input[type='tel']").fill("935052025")
    time.sleep(1)
    page.locator("xpath=/html/body/div[5]/div/div/div[2]/div/div/button[1]").click()
    time.sleep(5)

    print(f"URL: {page.url}")

    # Screenshot
    page.screenshot(path="screenshots/vacancies_page.png", full_page=True)
    print("Screenshot saqlandi: screenshots/vacancies_page.png")

    # HTML dump
    html_content = page.content()
    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML saqlandi: debug_page.html")

    # Barcha div'larni tekshirish
    print("\nBarcha div'lar ichida 'vacan' so'zi borlarini qidirish:")
    divs = page.locator("div").all()
    found_count = 0
    for i, div in enumerate(divs[:100]):  # Faqat birinchi 100 ta
        try:
            class_name = div.get_attribute("class", timeout=100)
            if class_name and ("vacan" in class_name.lower() or "card" in class_name.lower()):
                print(f"  Div {i}: class='{class_name}'")
                found_count += 1
                if found_count >= 5:
                    break
        except:
            pass

    time.sleep(60)
    browser.close()