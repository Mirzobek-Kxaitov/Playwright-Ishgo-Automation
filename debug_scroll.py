"""
Scroll funksiyasini tekshirish va to'g'ri scroll usulini topish.
"""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # Login qilish
    page.context.clear_cookies()
    page.goto("https://dev.ishgo.uz")

    print("1. Login qilish...")
    page.get_by_role("button", name="Login").click()
    time.sleep(1)

    page.locator("input[type='tel']").fill("935052025")
    time.sleep(1)

    page.locator("xpath=/html/body/div[5]/div/div/div[2]/div/div/button[1]").click()
    time.sleep(3)

    print("2. Vakansiyalar sahifasiga o'tildi")
    print(f"   Current URL: {page.url}")

    # Vakansiyalar yuklanishini kutish
    print("\n2.5. Vakansiyalar yuklanishini 5 soniya kutish...")
    time.sleep(5)

    # Barcha elementlarni tekshirish
    print("\n2.6. Sahifadagi barcha link'larni tekshirish:")
    all_links = page.locator("a").all()
    vacancy_links = []
    for link in all_links[:20]:  # Faqat birinchi 20 ta
        href = link.get_attribute("href")
        if href and "vacancy" in href:
            vacancy_links.append(href)
            print(f"   Topildi: {href}")

    print(f"\n   Jami {len(vacancy_links)} ta vakansiya link topildi")

    # Scroll qilishdan oldin
    print("\n3. SCROLL QILISHDAN OLDIN:")
    scroll_position_before = page.evaluate("window.pageYOffset")
    print(f"   Scroll pozitsiyasi: {scroll_position_before}px")

    viewport_height = page.evaluate("window.innerHeight")
    page_height = page.evaluate("document.body.scrollHeight")
    print(f"   Viewport balandligi: {viewport_height}px")
    print(f"   Sahifa balandligi: {page_height}px")

    # Method 1: window.scrollBy()
    print("\n4. METHOD 1: window.scrollBy(0, 500)")
    page.evaluate("window.scrollBy(0, 500)")
    time.sleep(2)

    scroll_after_method1 = page.evaluate("window.pageYOffset")
    print(f"   Scroll pozitsiyasi: {scroll_after_method1}px")
    print(f"   O'zgardi: {scroll_after_method1 > scroll_position_before}")

    # Method 2: window.scrollTo() - oxiriga
    print("\n5. METHOD 2: window.scrollTo(0, document.body.scrollHeight)")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

    scroll_after_method2 = page.evaluate("window.pageYOffset")
    print(f"   Scroll pozitsiyasi: {scroll_after_method2}px")
    print(f"   Sahifa oxiriga yetdi: {scroll_after_method2 > scroll_after_method1}")

    # Method 3: Smooth scroll
    print("\n6. METHOD 3: Smooth scroll")
    page.evaluate("window.scrollTo(0, 0)")  # Qaytadan yuqoriga
    time.sleep(1)
    page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
    time.sleep(3)

    scroll_after_method3 = page.evaluate("window.pageYOffset")
    print(f"   Scroll pozitsiyasi: {scroll_after_method3}px")

    # Infinite scroll bormi tekshirish
    print("\n7. INFINITE SCROLL tekshirish:")
    print("   3 marta scroll qilish va har safar vakansiyalar sonini tekshirish...")

    for i in range(3):
        cards_count = page.locator("a[href*='/vacancy/']").count()
        print(f"   Iteratsiya {i+1}: {cards_count} ta kartochka")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

    final_cards = page.locator("a[href*='/vacancy/']").count()
    print(f"\n   Final: {final_cards} ta kartochka")

    print("\n\n30 soniya kutish - browserda ko'ring...")
    time.sleep(30)
    browser.close()