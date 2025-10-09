from playwright.sync_api import Page, expect, TimeoutError
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_button = self.page.get_by_role("button", name="Kirish")
        self.phone_input = self.page.get_by_placeholder("99 123 45 67")
        self.get_code_button = self.page.get_by_role("button", name="Kodni olish")
        self.vacancies_header = self.page.get_by_role("heading", name="Vakansiyalar")

    def login(self, phone_number: str):
        """
        Saytga login qiladi. Agar foydalanuvchi allaqachon tizimga kirgan bo'lsa,
        login qadamlarini o'tkazib yuboradi.
        """
        try:
            # "Vakansiyalar" sarlavhasi 5 soniyada topilmasa, AssertionError xatosi yuz beradi
            expect(self.vacancies_header).to_be_visible(timeout=5000)
            print("Foydalanuvchi allaqachon tizimga kirgan. Login qadamlari o'tkazib yuborildi.")
            return
        except AssertionError:
            # Bu xato biz tizimga kirmaganimizni anglatadi
            print("Foydalanuvchi tizimga kirmagan. Login jarayoni boshlanmoqda.")

        # Login jarayonini bajarish
        try:
            self.login_button.click(timeout=10000)
            self.phone_input.fill(phone_number)
            self.get_code_button.click()
        except TimeoutError as e:
            print(f"Login jarayonida xatolik: {e}")
            raise

        # Login muvaffaqiyatli bo'lgach, "Vakansiyalar" sarlavhasini kutish
        expect(self.vacancies_header).to_be_visible(timeout=15000)
