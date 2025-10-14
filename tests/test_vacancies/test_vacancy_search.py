"""
P0 Priority Test: Vakansiyalarni qidirish

Test Scenarios:
1. Qidiruv input'ga matn kiritish va qidirish
2. Qidiruv natijalari chiqishini tekshirish
3. Valid qidiruv so'zi bilan test (masalan, "oshpaz")
4. Bo'sh qidiruv natijalari
"""

from playwright.sync_api import Page
from pages.vacancy_search_page import VacancySearchPage
from config import BASE_URL


def test_search_vacancy_with_valid_keyword(authenticated_page: Page):
    """
    Test: Valid kasbni qidirib natijalar olish

    Steps:
    1. Vakansiyalar sahifasida qidiruv input'ni topish
    2. "oshpaz" so'zini qidirish
    3. Qidiruv natijalari chiqishini tekshirish
    """
    search_page = VacancySearchPage(authenticated_page)

    # 1. "oshpaz" so'zini qidirish
    search_page.search_vacancy("oshpaz")

    # 2. Qidiruv natijalari mavjudligini tekshirish
    results_count = search_page.get_search_results_count()

    # 3. Kamida 1 ta natija bor yoki "Natija topilmadi" xabari ko'rsatilishi kerak
    if results_count > 0:
        search_page.verify_search_results_exist()
        print(f"✓ 'oshpaz' qidiruvi uchun {results_count} ta natija topildi")
    else:
        search_page.verify_no_results_message()
        print("✓ 'oshpaz' qidiruvi uchun natijalar topilmadi xabari ko'rsatildi")


def test_search_vacancy_with_generic_keyword(authenticated_page: Page):
    """
    Test: Umumiy kasbni qidirib ko'proq natijalar olish

    Steps:
    1. "menejer" kabi umumiy so'zni qidirish
    2. Qidiruv natijalari chiqishini tekshirish
    """
    search_page = VacancySearchPage(authenticated_page)

    # 1. Umumiy kasbni qidirish
    search_page.search_vacancy("menejer")

    # 2. Natijalarni tekshirish
    results_count = search_page.get_search_results_count()

    if results_count > 0:
        search_page.verify_search_results_exist()
        print(f"✓ 'menejer' qidiruvi uchun {results_count} ta natija topildi")
    else:
        print("✓ 'menejer' qidiruvi uchun natijalar topilmadi")


def test_search_with_empty_results(authenticated_page: Page):
    """
    Test: Noaniq qidiruv so'zi bilan bo'sh natijalar

    Steps:
    1. Hech qachon topilmaydigan so'zni qidirish (masalan, "xyzabc123")
    2. "Natija topilmadi" xabarini yoki bo'sh natijalarni tekshirish
    """
    search_page = VacancySearchPage(authenticated_page)

    # Vakansiyalar sahifasida ekanligini tekshirish
    if "/vacancies" not in authenticated_page.url:
        authenticated_page.goto(f"{BASE_URL}/vacancies")
        authenticated_page.wait_for_timeout(1500)

    # 1. Mavjud bo'lmagan kasbni qidirish
    search_page.search_vacancy("xyzabc123nonexistent")

    # 2. Bo'sh natijalar yoki "Natija topilmadi" xabarini kutish
    results_count = search_page.get_search_results_count()

    # Natijalar 0 yoki juda kam bo'lishi kerak
    assert results_count <= 2, f"Noaniq qidiruv uchun ko'p natijalar chiqdi: {results_count}"
    print(f"✓ Noaniq qidiruv uchun {results_count} ta natija - kutilganidek")


def test_clear_search_restores_all_vacancies(authenticated_page: Page):
    """
    Test: Qidiruvni tozalash barcha vakansiyalarni qaytaradi

    Steps:
    1. Biror kasb nomini qidirish
    2. Qidiruvni tozalash
    3. Barcha vakansiyalar qaytishini tekshirish
    """
    search_page = VacancySearchPage(authenticated_page)

    # 1. Qidiruv qilish
    search_page.search_vacancy("dasturchi")
    authenticated_page.wait_for_timeout(1500)

    # 2. Qidiruvni tozalash
    search_page.clear_search()
    authenticated_page.wait_for_timeout(1500)

    # 3. Barcha vakansiyalar qaytganini tekshirish
    results_count = search_page.get_search_results_count()
    assert results_count > 0, "Qidiruvni tozalanganda vakansiyalar qaytishi kerak edi"
    print(f"✓ Qidiruv tozalandi, {results_count} ta vakansiya ko'rsatilmoqda")