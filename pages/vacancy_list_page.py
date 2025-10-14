from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class VacancyListPage(BasePage):
    """
    Vakansiyalar ro'yxati sahifasi - /vacancies
    Ish qidiruvchi vakansiyalarni ko'rish, scroll qilish va asosiy interaksiyalar
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Vakansiya kartochkalari - to'g'ri CSS class selector
        self.vacancy_cards = self.page.locator("[class*='vacancy_card_wrapper'], [class*='vacancy_card__']")
        # Sahifa scroll konteyner
        self.page_container = self.page.locator("body")

    def get_vacancy_cards_count(self) -> int:
        """Sahifadagi vakansiya kartochkalar sonini qaytaradi"""
        self.logger.info("Vakansiya kartochkalar sonini hisoblash...")
        count = self.vacancy_cards.count()
        self.logger.info(f"Jami {count} ta vakansiya topildi")
        return count

    def scroll_to_bottom(self):
        """
        Sahifani pastga scroll qilish
        Mouse'ni vakansiya ustiga olib borib, oxirigacha scroll qiladi
        """
        self.logger.info("Sahifani pastga scroll qilish...")
        try:
            # O'rtadagi vakansiyaga mouse hover qilish
            middle_card = self.vacancy_cards.nth(5)  # 6-vakansiya (0-indexed)
            middle_card.hover()
            self.logger.info("Mouse o'rtadagi vakansiya ustiga olib borildi")

            # Sahifa balandligini olish
            page_height = self.page.evaluate("document.body.scrollHeight")

            # Asta-sekin pastga scroll qilish (natural scroll simulation)
            self.page.mouse.wheel(0, page_height)
            self.page.wait_for_timeout(1000)
            self.logger.info("Scroll muvaffaqiyatli amalga oshirildi")
        except Exception as e:
            self.logger.error(f"Scroll qilishda xatolik: {e}")
            raise

    def scroll_by_pixels(self, pixels: int = 500):
        """
        Ma'lum pixel miqdoriga scroll qilish
        Mouse'ni vakansiya kartochkasi ustiga olib borib, keyin scroll qiladi
        """
        self.logger.info(f"{pixels}px ga scroll qilish...")
        try:
            # Birinchi vakansiya kartochkasiga mouse hover qilish
            first_card = self.vacancy_cards.first
            first_card.hover()
            self.logger.info("Mouse vakansiya ustiga olib borildi")

            # Scroll qilish
            self.page.mouse.wheel(0, pixels)
            self.page.wait_for_timeout(500)
            self.logger.info(f"{pixels}px scroll muvaffaqiyatli")
        except Exception as e:
            self.logger.error(f"Scroll qilishda xatolik: {e}")
            raise

    def wait_for_vacancies_to_load(self, timeout: int = 10000):
        """Vakansiyalar yuklanishini kutish"""
        self.logger.info("Vakansiyalar yuklanishini kutilmoqda...")
        try:
            # Kamida bitta vakansiya kartochka paydo bo'lishini kutish
            self.vacancy_cards.first.wait_for(state="visible", timeout=timeout)
            self.logger.info("Vakansiyalar muvaffaqiyatli yuklandi")
        except Exception as e:
            self.logger.error(f"Vakansiyalar yuklanmadi: {e}")
            raise

    def verify_on_vacancies_page(self):
        """Vakansiyalar sahifasida ekanligini tekshirish"""
        self.logger.info("Vakansiyalar sahifasida ekanligini tekshirish...")
        try:
            # URL'da /vacancies borligini tekshirish
            current_url = self.page.url
            assert "/vacancies" in current_url, f"Vakansiyalar sahifasida emas: {current_url}"
            self.logger.info(f"Vakansiyalar sahifasida tasdiqlandi: {current_url}")
        except Exception as e:
            self.logger.error(f"Vakansiyalar sahifasida emas: {e}")
            raise