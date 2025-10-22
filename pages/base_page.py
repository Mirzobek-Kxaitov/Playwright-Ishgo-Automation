from playwright.sync_api import Page
from config import BASE_URL
from utils.logger import setup_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = BASE_URL
        self.logger = setup_logger(self.__class__.__name__)

    def navigate(self, path: str = ""):
        """Sahifaga o'tish (faqat yo'l bilan)"""
        full_url = f"{self.base_url}{path}"
        self.logger.info(f"Sahifaga o'tilmoqda: {full_url}")
        try:
            # Timeout 60 sekundga oshirildi (sekin serverlar uchun)
            self.page.goto(full_url, timeout=60000)
            self.logger.info(f"Sahifa muvaffaqiyatli yuklandi: {full_url}")
        except Exception as e:
            self.logger.error(f"Sahifaga o'tishda xatolik: {full_url} - {e}")
            raise

    def get_title(self) -> str:
        """Sahifa sarlavhasini olish"""
        title = self.page.title()
        self.logger.debug(f"Sahifa sarlavhasi: {title}")
        return title
