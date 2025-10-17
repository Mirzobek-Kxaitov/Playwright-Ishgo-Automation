"""Debug test - Sahifani tekshirish"""

from playwright.sync_api import Page


def test_debug_page_elements(authenticated_page: Page):
    """Debug: Sahifadagi elementlarni tekshirish"""

    # Sahifa yuklanishini kutish
    authenticated_page.wait_for_load_state("networkidle")
    authenticated_page.wait_for_timeout(3000)

    print("\n" + "="*60)
    print("SAHIFA DEBUG MA'LUMOTLARI")
    print("="*60)

    # URL
    print(f"\nURL: {authenticated_page.url}")

    # Vakansiyalar kartochkalarini topish
    print("\n--- Vakansiyalar kartochkalari ---")
    vacancy_selectors = [
        "[class*='vacancy_card']",
        "[class*='vacancy-card']",
        "[class*='VacancyCard']",
        "div[class*='card']",
    ]

    for selector in vacancy_selectors:
        count = authenticated_page.locator(selector).count()
        print(f"  {selector}: {count} ta")

    # Button'larni topish
    print("\n--- Button'lar ---")
    all_buttons = authenticated_page.locator("button").all()
    print(f"  Jami buttonlar: {len(all_buttons)}")

    for i, btn in enumerate(all_buttons):  # BARCHA buttonlar
        try:
            text = btn.inner_text(timeout=1000)
            if text:
                print(f"  Button {i+1}: '{text[:50]}'")  # Birinchi 50 belgi
        except:
            pass

    # "Filter" tugmasini qidirish
    print("\n--- 'Filter' tugmasi ---")
    filter_button = authenticated_page.locator("button").filter(has_text="Filter")
    if filter_button.is_visible(timeout=2000):
        print("  ✓ 'Filter' tugmasi topildi!")
        # Filter tugmasini bosish
        filter_button.click()
        authenticated_page.wait_for_timeout(2000)
        print("  ✓ Filter tugmasi bosildi")

        # Endi qayta buttonlarni sanash
        all_buttons_after = authenticated_page.locator("button").all()
        print(f"\n  Filterdan keyin buttonlar: {len(all_buttons_after)}")

        for i, btn in enumerate(all_buttons_after):
            try:
                text = btn.inner_text(timeout=1000)
                if text:
                    print(f"    Button {i+1}: '{text[:50]}'")
            except:
                pass
    else:
        print("  ✗ 'Filter' tugmasi topilmadi")

    # Screenshot
    authenticated_page.screenshot(path="debug_page.png")
    print("\nScreenshot saqlandi: debug_page.png")

    print("\n" + "="*60)