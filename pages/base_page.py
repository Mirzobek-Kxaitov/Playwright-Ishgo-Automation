from playwright.sync_api import Page
from config import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = BASE_URL

    def navigate(self, path: str = ""):
        """Sahifaga o'tish (faqat yo'l bilan)"""
        self.page.goto(f"{self.base_url}{path}")

    def get_title(self) -> str:
        """Sahifa sarlavhasini olish"""
        return self.page.title()
