from playwright.sync_api import Page
from pages.vacancy_filters_page import VacancyFiltersPage
from config import BASE_URL


class VacancyMapPage(VacancyFiltersPage):
    """
    Vakansiyalar xarita sahifasi - /vacancies?child=map
    VacancyFiltersPage dan meros oladi, barcha filter metodlari ishlatiladi
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Xarita buttonini XPath
        self.map_button_xpath = "/html/body/div[2]/main/div[1]/div[2]/div[1]/div[1]/div[2]/button"

        # Xarita URL
        self.map_url = f"{BASE_URL}/vacancies?child=map"

    def open_map_view(self):
        """Xarita ko'rinishiga o'tish - Map button orqali"""
        self.logger.info("Xarita ko'rinishiga o'tilmoqda...")
        try:
            # Map buttonni topish va bosish
            map_button = self.page.locator(f"xpath={self.map_button_xpath}")

            if map_button.is_visible(timeout=5000):
                map_button.click()
                self.page.wait_for_timeout(2000)  # Xarita yuklanishini kutish
                self.logger.info("Xarita ko'rinishi ochildi")

                # URL tekshirish
                current_url = self.page.url
                if "child=map" in current_url:
                    self.logger.info(f"Xarita URL tasdiqlandi: {current_url}")
                else:
                    self.logger.warning(f"URL kutilganday emas: {current_url}")
            else:
                self.logger.error("Xarita button topilmadi")
                raise Exception("Map button not found")

        except Exception as e:
            self.logger.error(f"Xarita ko'rinishiga o'tishda xatolik: {e}")
            raise

    def verify_map_loaded(self) -> bool:
        """
        Xarita yuklanganligini tekshirish

        Returns:
            bool: Xarita yuklangan bo'lsa True
        """
        self.logger.info("Xarita yuklanishi tekshirilmoqda...")
        try:
            # URL tekshirish
            current_url = self.page.url
            is_map_url = "child=map" in current_url

            if is_map_url:
                self.logger.info("Xarita muvaffaqiyatli yuklandi")
                return True
            else:
                self.logger.warning("Xarita yuklanmadi")
                return False

        except Exception as e:
            self.logger.error(f"Xarita holatini tekshirishda xatolik: {e}")
            return False

    def close_map_view(self):
        """Xarita ko'rinishidan chiqish - qayta list view ga qaytish"""
        self.logger.info("Xarita ko'rinishidan chiqilmoqda...")
        try:
            # Agar map button qayta bosilsa, list view ga qaytadi
            map_button = self.page.locator(f"xpath={self.map_button_xpath}")

            if map_button.is_visible(timeout=5000):
                map_button.click()
                self.page.wait_for_timeout(2000)
                self.logger.info("List view ga qaytildi")
            else:
                self.logger.warning("Map button topilmadi")

        except Exception as e:
            self.logger.error(f"Map viewdan chiqishda xatolik: {e}")
            raise

    # ==================== Xarita uchun override metodlar ====================
    # Xaritada filterlar sekinroq ishlaydi, shuning uchun wait time oshirilgan

    def select_employment_type(self, employment_type: str):
        """
        Xaritada Bandlik turini tanlash (override metod - ko'proq wait time)

        Xaritada 0 vakansiya bo'lsa ham filter tanlanishi kerak

        Args:
            employment_type: "To'liq bandlik", "Vaqtincha ish", va boshqalar
        """
        self.logger.info(f"Xaritada Bandlik turi filtri tanlanmoqda: {employment_type}")
        try:
            # Bandlik turi dropdown'ni ochish
            employment_dropdown = self.page.get_by_text("Bandlik turi", exact=True).first
            employment_dropdown.click()
            self.page.wait_for_timeout(3000)  # Xaritada ko'proq kutish - 3 soniya

            # Dropdown ochilishini kutish - visible bo'lishini kutamiz (timeout 5s)
            try:
                self.page.wait_for_selector(f"text={employment_type}", state="visible", timeout=5000)

                # Kerakli variantni tanlash - locator orqali
                employment_option = self.page.locator(f"text={employment_type}").first
                employment_option.click(force=True, timeout=5000)  # Force click
                self.page.wait_for_timeout(2000)
                self.logger.info(f"Xaritada Bandlik turi filtri tanlandi: {employment_type}")
            except Exception as inner_e:
                # Variant topilmasa - 0 vakansiya bo'lishi mumkin
                self.logger.warning(f"Xaritada '{employment_type}' varianti topilmadi (0 vakansiya bo'lishi mumkin)")
                # Dropdown'ni yopish - force click
                try:
                    employment_dropdown.click(force=True, timeout=3000)
                    self.page.wait_for_timeout(1000)
                except:
                    # Yopilmasa ham davom etamiz
                    self.page.wait_for_timeout(500)

        except Exception as e:
            self.logger.error(f"Xaritada Bandlik turi dropdown ochishda xatolik: {e}")
            raise

    def select_sort_option(self, sort_option: str):
        """
        Xaritada Saralash turini tanlash (override metod - force click)

        Xaritada 0 vakansiya bo'lsa ham filter tanlanishi kerak

        Args:
            sort_option: "Joylangan sana bo'yicha (Yangi)", va boshqalar
        """
        self.logger.info(f"Xaritada Saralash filtri tanlanmoqda: {sort_option}")
        try:
            # Saralash dropdown'ni ochish - force click
            saralash_dropdown = self.page.get_by_text("Saralash", exact=True).first
            saralash_dropdown.click(force=True, timeout=10000)
            self.page.wait_for_timeout(3000)  # Xaritada ko'proq kutish

            # Dropdown ochilishini kutish (timeout 5s)
            try:
                self.page.wait_for_selector(f"text={sort_option}", state="visible", timeout=5000)

                # Kerakli variantni tanlash
                sort_option_locator = self.page.locator(f"text={sort_option}").first
                sort_option_locator.click(force=True, timeout=5000)
                self.page.wait_for_timeout(2000)
                self.logger.info(f"Xaritada Saralash filtri tanlandi: {sort_option}")
            except Exception as inner_e:
                # Variant topilmasa - 0 vakansiya bo'lishi mumkin
                self.logger.warning(f"Xaritada '{sort_option}' varianti topilmadi (0 vakansiya bo'lishi mumkin)")
                # Dropdown'ni yopish
                saralash_dropdown.click(force=True)
                self.page.wait_for_timeout(1000)

        except Exception as e:
            self.logger.error(f"Xaritada Saralash dropdown ochishda xatolik: {e}")
            raise