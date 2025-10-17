"""
Filter sahifasini tekshirish - to'g'ri locator'larni topish
"""

from playwright.sync_api import Page
from config import BASE_URL


def test_inspect_filter_structure(authenticated_page: Page):
    """
    Sahifadagi filter elementlarini tekshirish va screenshot olish
    """
    page = authenticated_page

    print("\n" + "="*60)
    print("FILTER STRUKTURASINI TEKSHIRISH")
    print("="*60)

    # Screenshot olish - dastlabki holat
    page.screenshot(path="filter_initial.png")
    print("✓ Dastlabki screenshot saqlandi: filter_initial.png")

    # 1-usul: "Vakansiyalarni qidirish" field orqali
    print("\n1-USUL: 'Vakansiyalarni qidirish' field")
    try:
        search_field_xpath = "/html/body/div[2]/main/div[1]/div[2]/div[1]/div[1]/div[1]"
        search_field = page.locator(f"xpath={search_field_xpath}")

        if search_field.is_visible(timeout=5000):
            print(f"  ✓ Field topildi")
            print(f"  - Text: {search_field.inner_text()}")

            # Click qilib ko'ramiz
            search_field.click()
            page.wait_for_timeout(2000)
            page.screenshot(path="filter_after_search_click.png")
            print("  ✓ Field bosildi, screenshot: filter_after_search_click.png")
    except Exception as e:
        print(f"  ✗ Xatolik: {e}")

    # Sahifani refresh qilish
    page.reload()
    page.wait_for_timeout(2000)

    # 2-usul: "Filter" button orqali
    print("\n2-USUL: 'Filter' button")
    try:
        filter_button_xpath = "/html/body/div[2]/main/div[1]/div[2]/div[1]/div[1]/button"
        filter_button = page.locator(f"xpath={filter_button_xpath}")

        if filter_button.is_visible(timeout=5000):
            print(f"  ✓ Button topildi")
            print(f"  - Text: {filter_button.inner_text()}")

            # Click qilib ko'ramiz
            filter_button.click()
            page.wait_for_timeout(2000)
            page.screenshot(path="filter_after_button_click.png")
            print("  ✓ Button bosildi, screenshot: filter_after_button_click.png")

            # Filterlar ochilganidan keyin nima bor tekshiramiz
            print("\n  OCHILGAN FILTERLAR:")

            # Barcha filter elementlarni topishga harakat
            filter_containers = page.locator("[class*='filter'], [role='button']")
            count = filter_containers.count()
            print(f"  - Jami {count} ta filter elementi topildi")

            for i in range(min(count, 10)):  # Birinchi 10 tasini ko'rsatamiz
                try:
                    element = filter_containers.nth(i)
                    text = element.inner_text()[:50]  # Birinchi 50 ta belgisi
                    print(f"    [{i}]: {text}")
                except:
                    pass

    except Exception as e:
        print(f"  ✗ Xatolik: {e}")

    # Final screenshot
    page.screenshot(path="filter_final.png")
    print("\n✓ Final screenshot: filter_final.png")

    print("\n" + "="*60)
    print("TEKSHIRISH TUGADI")
    print("="*60)