from playwright.sync_api import Page, expect
from pages.vacancies_page import VacanciesPage
from config import BASE_URL


def test_navigate_to_my_vacancies(authenticated_page: Page, vacancies_page: VacanciesPage):
    """
    Tizimga kirgan foydalanuvchi "Vakansiya joylashtirish" tugmasini bosganda
    "Mening vakansiyalarim" sahifasiga o'tishini tekshiradi.

    Pre-condition: Foydalanuvchi tizimga kirgan (authenticated_page fixture orqali)
    """
    # authenticated_page fixture allaqachon login qilgan, shuning uchun to'g'ridan-to'g'ri test qilamiz
    page = authenticated_page

    # 1. "Vakansiyalar" sahifasida ekanligini tasdiqlash
    expect(page).to_have_url(f"{BASE_URL}/vacancies")

    # 2. "Vakansiya joylashtirish" tugmasini bosish
    vacancies_page.click_post_vacancy()

    # 3. "Mening vakansiyalarim" sahifasiga o'tganini tekshirish
    vacancies_page.verify_on_my_vacancies_page()

    # 4. URL manzilini tekshirish
    expected_url = f"{BASE_URL}/vacancies/my"
    expect(page).to_have_url(expected_url)
