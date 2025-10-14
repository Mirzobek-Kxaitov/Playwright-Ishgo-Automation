from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class VacanciesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.post_vacancy_button = self.page.get_by_role("button", name="Vakansiya joylashtirish")
        self.my_vacancies_header = self.page.get_by_role("heading", name="Mening vakansiyalarim")

    def click_post_vacancy(self):
        """'Vakansiya joylashtirish' tugmasini bosish"""
        self.logger.info("'Vakansiya joylashtirish' tugmasi bosilmoqda...")
        try:
            self.post_vacancy_button.click()
            self.logger.info("'Vakansiya joylashtirish' tugmasi muvaffaqiyatli bosildi")
        except Exception as e:
            self.logger.error(f"'Vakansiya joylashtirish' tugmasini bosishda xatolik: {e}")
            raise

    def verify_on_my_vacancies_page(self):
        """'Mening vakansiyalarim' sahifasida ekanligini tekshirish"""
        self.logger.info("'Mening vakansiyalarim' sahifasida ekanligini tekshirish...")
        try:
            expect(self.my_vacancies_header).to_be_visible()
            self.logger.info("'Mening vakansiyalarim' sahifasi tasdiqlandi")
        except AssertionError as e:
            self.logger.error("'Mening vakansiyalarim' sahifasi topilmadi")
            raise
