import pytest
from playwright.sync_api import Page, expect
from pages.vacancies_page import VacanciesPage
from pages.login_page import LoginPage
from config import BASE_URL, PHONE_NUMBER

def test_navigate_to_my_vacancies(page: Page, login_page: LoginPage, vacancies_page: VacanciesPage):
    """
    Saytga login qilib, "Vakansiya joylashtirish" tugmasini bosganda
    "Mening vakansiyalarim" sahifasiga o'tishini tekshiradi.
    """
    # Himoya: .env faylidan telefon raqami yuklanganini tekshirish
    if not PHONE_NUMBER:
        pytest.fail("DIQQAT: Telefon raqami .env faylidan topilmadi. Iltimos, .env faylini tekshiring.")

    # 1. Saytga kirish (yoki tizimda ekanligini tasdiqlash)
    login_page.navigate() # Asosiy sahifaga o'tish
    login_page.login(PHONE_NUMBER)

    # Login/tasdiqlashdan so'ng "Vakansiyalar" sahifasida ekanligini tekshirish
    expect(page).to_have_url(f"{BASE_URL}/vacancies")

    # 2. "Vakansiya joylashtirish" tugmasini bosish
    vacancies_page.click_post_vacancy()

    # 3. "Mening vakansiyalarim" sahifasiga o'tganini tekshirish
    vacancies_page.verify_on_my_vacancies_page()

    # Qo'shimcha tekshiruv: URL manzilini tekshirish
    expected_url = f"{BASE_URL}/vacancies/my"
    expect(page).to_have_url(expected_url)
