"""
"Kirish" tugmasi bosilgandan keyin nima bo'lishini tekshirish.
"""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    page.context.clear_cookies()
    page.goto("https://dev.ishgo.uz")

    print("1. Login tugmasini bosish...")
    page.get_by_role("button", name="Login").click()
    time.sleep(2)

    print("2. Telefon raqamini kiritish: 935052025")
    phone_input = page.locator("input[type='tel']")
    phone_input.fill("935052025")
    time.sleep(1)

    print("3. 'Kirish' tugmasini bosish...")
    submit_btn = page.locator("xpath=/html/body/div[5]/div/div/div[2]/div/div/button[1]")
    submit_btn.click()

    print("\n4. 'Kirish' bosildi! 5 soniya kutamiz...")
    time.sleep(5)

    print("\n5. Hozirgi sahifa URL:")
    print(f"   URL: {page.url}")

    print("\n6. Hozirgi sahifadagi barcha heading'lar:")
    headings = page.locator("h1, h2, h3").all()
    for i, h in enumerate(headings[:10]):
        try:
            text = h.inner_text(timeout=500)
            if text.strip():
                print(f"   Heading {i+1}: '{text}'")
        except:
            pass

    print("\n7. SMS kod input bor mi?")
    sms_inputs = page.locator("input[type='text'], input[type='number'], input[inputmode='numeric']").all()
    print(f"   Topilgan input'lar soni: {len(sms_inputs)}")

    print("\n\n60 soniya kutish - browserda ko'ring nima bo'ldi...")
    time.sleep(60)
    browser.close()