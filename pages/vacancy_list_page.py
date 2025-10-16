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
        # Vakansiyalar ro'yxati scroll konteyner
        self.vacancy_list_container = self.page.locator(".styles_vacancy_list_wrapper__OFLB1")

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
        Vakansiyalar ro'yxati konteynerida scroll qiladi
        """
        self.logger.info(f"{pixels}px ga scroll qilish...")
        try:
            # Container'ga scroll qilish
            scroll_result = self.vacancy_list_container.evaluate(f"""(element) => {{
                const before = element.scrollTop;
                element.scrollBy(0, {pixels});
                const after = element.scrollTop;
                return {{before: before, after: after, scrollHeight: element.scrollHeight, clientHeight: element.clientHeight}};
            }}""")
            self.logger.info(f"Scroll: {scroll_result['before']}px → {scroll_result['after']}px (total: {scroll_result['scrollHeight']}px)")
            self.page.wait_for_timeout(500)
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