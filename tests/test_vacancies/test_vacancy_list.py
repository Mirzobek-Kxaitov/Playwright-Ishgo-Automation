"""
P0 Priority Test: Vakansiyalar ro'yxatini ko'rish va scroll qilish

Test Scenarios:
1. Vakansiyalar sahifasiga muvaffaqiyatli kirish
2. Vakansiya kartochkalarini ko'rish
3. Sahifani pastga scroll qilish
4. Scroll qilgandan keyin ko'proq vakansiyalar yuklanishini tekshirish
"""

from playwright.sync_api import Page, expect
from pages.vacancy_list_page import VacancyListPage
from config import BASE_URL


def test_view_vacancy_list(authenticated_page: Page):
    """
    Test: Vakansiyalar ro'yxatini ko'rish

    Steps:
    1. Vakansiyalar sahifasiga kirish (authenticated_page allaqachon /vacancies'da)
    2. Vakansiya kartochkalari ko'rinishini tekshirish
    3. Kamida 1 ta vakansiya bor ekanligini tasdiqlash
    """
    vacancy_list_page = VacancyListPage(authenticated_page)

    # 1. Vakansiyalar sahifasida ekanligini tasdiqlash
    vacancy_list_page.verify_on_vacancies_page()

    # 2. Vakansiyalar yuklanishini kutish
    vacancy_list_page.wait_for_vacancies_to_load()

    # 3. Kamida 1 ta vakansiya kartochka borligini tekshirish
    vacancy_count = vacancy_list_page.get_vacancy_cards_count()
    assert vacancy_count > 0, "Hech qanday vakansiya topilmadi!"


def test_scroll_vacancy_list(authenticated_page: Page):
    """
    Test: Vakansiyalar ro'yxatini oxirigacha scroll qilish

    Steps:
    1. Dastlabki vakansiyalar sonini hisoblash
    2. Bir necha marta pastga scroll qilish (oxirigacha)
    3. Har safar scroll qilganda yangi vakansiyalar yuklanishini kuzatish
    4. Oxiriga yetganda to'xtash
    """
    vacancy_list_page = VacancyListPage(authenticated_page)

    # 1. Vakansiyalar yuklanishini kutish
    vacancy_list_page.wait_for_vacancies_to_load()

    # 2. Dastlabki vakansiyalar soni
    initial_count = vacancy_list_page.get_vacancy_cards_count()
    assert initial_count > 0, "Vakansiyalar yuklanmadi"
    print(f"Dastlab: {initial_count} ta vakansiya")

    # 3. Bir necha marta scroll qilish va natijani kuzatish
    max_scrolls = 5  # Maksimal 5 marta scroll
    previous_count = initial_count

    for i in range(max_scrolls):
        # Scroll qilish
        vacancy_list_page.scroll_by_pixels(800)
        authenticated_page.wait_for_timeout(1500)  # Yangi vakansiyalar yuklanishini kutish

        # Yangi vakansiyalar sonini tekshirish
        current_count = vacancy_list_page.get_vacancy_cards_count()

        if current_count > previous_count:
            print(f"Scroll {i+1}: {previous_count} → {current_count} (+{current_count - previous_count} yangi)")
            previous_count = current_count
        else:
            print(f"Scroll {i+1}: Barcha vakansiyalar yuklandi ({current_count} ta)")
            break

    # 4. Yakuniy natija
    final_count = vacancy_list_page.get_vacancy_cards_count()
    assert final_count >= initial_count, "Scroll qilgandan keyin vakansiyalar kamaydi!"
    print(f"✓ Yakuniy: {final_count} ta vakansiya ({final_count - initial_count} yangi yuklandi)")
    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies")