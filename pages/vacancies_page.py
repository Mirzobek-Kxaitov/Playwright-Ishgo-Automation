from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class VacanciesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.post_vacancy_button = self.page.get_by_role("button", name="Vakansiya joylashtirish")
        self.my_vacancies_header = self.page.get_by_role("heading", name="Mening vakansiyalarim")

    def click_post_vacancy(self):
        """'Vakansiya joylashtirish' tugmasini bosish"""
        self.post_vacancy_button.click()

    def verify_on_my_vacancies_page(self):
        """'Mening vakansiyalarim' sahifasida ekanligini tekshirish"""
        expect(self.my_vacancies_header).to_be_visible()
