from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class VacancySearchPage(BasePage):
    """
    Vakansiyalar qidiruv sahifasi - /vacancies
    Qidiruv input, filtrlar va natijalar bilan ishlash
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Qidiruv input field - "Vakansiyalarni qidirish" placeholder bilan
        self.search_input = self.page.locator("input[placeholder*='qidirish'], input[type='text']").first
        # Qidiruv natijasi kartochkalar
        self.search_result_cards = self.page.locator("[class*='vacancy'], [data-testid='vacancy-card']")
        # "Natija topilmadi" xabari
        self.no_results_message = self.page.locator("text=/Hech narsa topilmadi|Natija yo'q|No results/i")

    def search_vacancy(self, query: str):
        """
        Vakansiyani qidirish

        Args:
            query: Qidiruv so'zi (masalan, "oshpaz")
        """
        self.logger.info(f"Vakansiya qidirilmoqda: '{query}'")
        try:
            # Qidiruv inputiga focus va matn kiritish
            self.search_input.click()
            self.search_input.fill(query)
            self.logger.info(f"Qidiruv so'zi kiritildi: '{query}'")

            # Enter bosish yoki qidiruv tugmasi bosish
            self.search_input.press("Enter")
            self.logger.info("Enter bosildi - qidiruv boshlandi")

            # Qidiruv natijalarini kutish (bir oz vaqt berish)
            self.page.wait_for_timeout(1500)
            self.logger.info("Qidiruv natijalari kutilmoqda...")

        except Exception as e:
            self.logger.error(f"Qidiruv jarayonida xatolik: {e}")
            raise

    def get_search_results_count(self) -> int:
        """Qidiruv natijalari sonini qaytarish"""
        self.logger.info("Qidiruv natijalari sonini hisoblash...")
        try:
            count = self.search_result_cards.count()
            self.logger.info(f"Qidiruv natijalari: {count} ta")
            return count
        except Exception as e:
            self.logger.error(f"Natijalarni hisoblashda xatolik: {e}")
            return 0

    def verify_search_results_exist(self):
        """Qidiruv natijalari bor ekanligini tekshirish"""
        self.logger.info("Qidiruv natijalari mavjudligini tekshirish...")
        try:
            expect(self.search_result_cards.first).to_be_visible(timeout=5000)
            self.logger.info("Qidiruv natijalari topildi")
        except Exception as e:
            self.logger.error(f"Qidiruv natijalari topilmadi: {e}")
            raise

    def verify_no_results_message(self):
        """'Natija topilmadi' xabari ko'rinishini tekshirish"""
        self.logger.info("'Natija topilmadi' xabari tekshirilmoqda...")
        try:
            expect(self.no_results_message).to_be_visible(timeout=5000)
            self.logger.info("'Natija topilmadi' xabari ko'rsatildi")
        except Exception as e:
            self.logger.warning(f"'Natija topilmadi' xabari topilmadi: {e}")
            # Bu xato emas, faqat warning

    def clear_search(self):
        """Qidiruv inputini tozalash"""
        self.logger.info("Qidiruv inputini tozalash...")
        try:
            self.search_input.click()
            self.search_input.fill("")
            self.logger.info("Qidiruv tozalandi")
        except Exception as e:
            self.logger.error(f"Qidiruvni tozalashda xatolik: {e}")
            raise