"""
Xarita sahifasini tekshirish - filterlar qanday ishlashini aniqlash
"""

from playwright.sync_api import Page
from pages.vacancy_map_page import VacancyMapPage


def test_inspect_map_filters(authenticated_page: Page):
    """
    Xarita sahifasidagi filter elementlarini tekshirish va screenshot olish
    """
    page = authenticated_page
    map_page = VacancyMapPage(page)

    print("\n" + "="*60)
    print("XARITA FILTER STRUKTURASINI TEKSHIRISH")
    print("="*60)

    # Xaritaga o'tish
    map_page.open_map_view()
    page.wait_for_timeout(3000)  # Xarita to'liq yuklanishini kutish

    # Screenshot 1: Dastlabki holat
    page.screenshot(path="map_initial.png")
    print("✓ Dastlabki screenshot saqlandi: map_initial.png")

    # Vakansiyalar sonini tekshirish
    try:
        vacancy_count = map_page.get_filtered_vacancies_count()
        print(f"\n📊 Xaritada vakansiyalar soni: {vacancy_count}")
    except Exception as e:
        print(f"\n⚠️ Vakansiyalar sonini hisoblashda xatolik: {e}")
        vacancy_count = 0

    # Filterlarni ochish
    print("\n📂 Filterlarni ochish...")
    try:
        map_page.open_filters()
        page.wait_for_timeout(2000)
        page.screenshot(path="map_filters_opened.png")
        print("✓ Filterlar ochildi, screenshot: map_filters_opened.png")
    except Exception as e:
        print(f"✗ Filterlarni ochishda xatolik: {e}")

    # Barcha dropdown'larni topish
    print("\n🔍 Dropdown elementlarni qidirish...")

    # 1. Bandlik turi dropdown - BU ISHLAMAGAN
    print("\n2️⃣ BANDLIK TURI DROPDOWN (ISHLAMAGAN):")
    try:
        bandlik_dropdown = page.get_by_text("Bandlik turi", exact=True).first
        if bandlik_dropdown.is_visible(timeout=3000):
            print("  ✓ Bandlik turi dropdown topildi")
            print(f"    - Is enabled: {bandlik_dropdown.is_enabled()}")
            print(f"    - Is editable: {bandlik_dropdown.is_editable()}")

            bandlik_dropdown.click()
            page.wait_for_timeout(1000)
            page.screenshot(path="map_bandlik_opened.png")
            print("  ✓ Screenshot: map_bandlik_opened.png")

            # Birinchi variantni tanlash
            try:
                toliq_bandlik = page.get_by_text("To'liq bandlik", exact=True)
                count = toliq_bandlik.count()
                print(f"  📊 'To'liq bandlik' elementlari soni: {count}")

                if count > 0:
                    first = toliq_bandlik.first
                    print(f"    - Is visible: {first.is_visible(timeout=2000)}")
                    print(f"    - Is enabled: {first.is_enabled()}")

                    # Tanlashga harakat
                    first.click()
                    page.wait_for_timeout(1000)
                    page.screenshot(path="map_bandlik_selected.png")
                    print("  ✓ 'To'liq bandlik' tanlandi, screenshot: map_bandlik_selected.png")

                    # Natijalarni kutish
                    page.wait_for_timeout(2000)
                    page.screenshot(path="map_bandlik_result.png")
                    print("  ✓ Natija screenshot: map_bandlik_result.png")

                    # Vakansiyalar sonini tekshirish
                    try:
                        new_count = map_page.get_filtered_vacancies_count()
                        print(f"  📊 Filter qo'llanganidan keyin vakansiyalar: {new_count}")
                    except Exception as e:
                        print(f"  ⚠️ Vakansiyalar sonini hisoblashda xatolik: {e}")

                else:
                    print("  ✗ 'To'liq bandlik' varianti topilmadi")
            except Exception as e:
                print(f"  ✗ Variant tekshirishda xatolik: {e}")

        else:
            print("  ✗ Bandlik turi dropdown ko'rinmaydi")
    except Exception as e:
        print(f"  ✗ Xatolik: {e}")

    page.wait_for_timeout(2000)

    # 2. Saralash dropdown - BU HAM ISHLAMAGAN
    print("\n3️⃣ SARALASH DROPDOWN (ISHLAMAGAN):")
    try:
        saralash_dropdown = page.get_by_text("Saralash", exact=True).first
        if saralash_dropdown.is_visible(timeout=3000):
            print("  ✓ Saralash dropdown topildi")
            print(f"    - Is enabled: {saralash_dropdown.is_enabled()}")

            saralash_dropdown.click()
            page.wait_for_timeout(1000)
            page.screenshot(path="map_saralash_opened.png")
            print("  ✓ Screenshot: map_saralash_opened.png")

            # Birinchi variantni tekshirish
            try:
                yangi = page.get_by_text("Joylangan sana bo'yicha (Yangi)", exact=True)
                count = yangi.count()
                print(f"  📊 'Joylangan sana bo'yicha (Yangi)' elementlari soni: {count}")

                if count > 0:
                    first = yangi.first
                    print(f"    - Is visible: {first.is_visible(timeout=2000)}")
                    print(f"    - Is enabled: {first.is_enabled()}")

                    # Tanlashga harakat
                    first.click()
                    page.wait_for_timeout(1000)
                    page.screenshot(path="map_saralash_selected.png")
                    print("  ✓ 'Joylangan sana bo'yicha (Yangi)' tanlandi")
                else:
                    print("  ✗ Variant topilmadi")
            except Exception as e:
                print(f"  ✗ Variant tekshirishda xatolik: {e}")

        else:
            print("  ✗ Saralash dropdown ko'rinmaydi")
    except Exception as e:
        print(f"  ✗ Xatolik: {e}")

    # Final screenshot
    page.screenshot(path="map_final.png", full_page=True)
    print("\n✓ Final screenshot (full page): map_final.png")

    print("\n" + "="*60)
    print("TEKSHIRISH TUGADI")
    print("="*60)
    print("\n📁 Yaratilgan screenshot'lar:")
    print("  - map_initial.png")
    print("  - map_filters_opened.png")
    print("  - map_bandlik_opened.png")
    print("  - map_bandlik_selected.png (agar tanlangan bo'lsa)")
    print("  - map_bandlik_result.png (natija)")
    print("  - map_saralash_opened.png")
    print("  - map_saralash_selected.png (agar tanlangan bo'lsa)")
    print("  - map_final.png")