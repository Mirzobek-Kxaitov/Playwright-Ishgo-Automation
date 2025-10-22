import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config import BASE_URL, PHONE_NUMBER


def test_login_success(page: Page, login_page: LoginPage):
    """
    Login funksiyasini tekshirish.
    Telefon raqami bilan tizimga muvaffaqiyatli kirish.
    """
    # Himoya: .env faylidan telefon raqami yuklanganini tekshirish
    if not PHONE_NUMBER:
        pytest.fail("DIQQAT: Telefon raqami .env faylidan topilmadi. Iltimos, .env faylini tekshiring.")

    # 1. Asosiy sahifaga o'tish
    login_page.navigate()

    # 2. Login qilish
    login_page.login(PHONE_NUMBER)


    # 3. Login muvaffaqiyatli bo'lganini tekshirish - "/vacancies" sahifasiga o'tganini tasdiqlash
    expect(page).to_have_url(f"{BASE_URL}/vacancies")