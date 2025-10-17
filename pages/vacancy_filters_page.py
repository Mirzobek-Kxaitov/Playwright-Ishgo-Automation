from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class VacancyFiltersPage(BasePage):
    """
    Vakansiyalar filtrlar sahifasi - /vacancies
    Vakansiyalarni filtrlash va saralash funksiyalari
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Filterlarni ochish tugmasi - XPath orqali
        self.filter_button_xpath = "/html/body/div[2]/main/div[1]/div[2]/div[1]/div[1]/button"

    # ==================== Filterlarni ochish ====================
    def open_filters(self):
        """Filterlar panelini ochish - Filter button orqali"""
        self.logger.info("Filterlar paneli ochilmoqda...")
        try:
            # Check if filters are already open by checking for any filter dropdown
            salary_dropdown = self.page.get_by_text("Maosh", exact=True).first
            if salary_dropdown.is_visible(timeout=2000):
                self.logger.info("Filterlar paneli allaqachon ochiq")
                return

            # Try multiple methods to find and click filter button
            # Method 1: XPath
            try:
                filter_button = self.page.locator(f"xpath={self.filter_button_xpath}")
                if filter_button.is_visible(timeout=3000):
                    filter_button.click()
                    self.page.wait_for_timeout(2000)
                    self.logger.info("Filterlar paneli ochildi (XPath)")
                    return
            except:
                pass

            # Method 2: Text-based (for headless mode)
            try:
                filter_button = self.page.get_by_role("button").filter(has_text="Filter")
                if filter_button.is_visible(timeout=3000):
                    filter_button.click()
                    self.page.wait_for_timeout(2000)
                    self.logger.info("Filterlar paneli ochildi (Text)")
                    return
            except:
                pass

            # Method 3: Aria-label or other attributes
            try:
                filter_button = self.page.locator("button:has-text('Filter')")
                if filter_button.is_visible(timeout=3000):
                    filter_button.click()
                    self.page.wait_for_timeout(2000)
                    self.logger.info("Filterlar paneli ochildi (has-text)")
                    return
            except:
                pass

            self.logger.warning("Filter tugmasi topilmadi - filterlar allaqachon ochiq bo'lishi mumkin")

        except Exception as e:
            self.logger.warning(f"Filterlarni ochishda xatolik: {e}")
            # Don't raise - filters might already be open
            pass

    # ==================== Maosh filtri ====================
    def select_salary_range(self, range_text: str):
        """
        Maosh oralig'ini tanlash

        Args:
            range_text: "1 mln - 3 mln", "3 mln - 5 mln", "5 mln - 7 mln",
                       "7 mln - 10 mln", "10 mln+"
        """
        self.logger.info(f"Maosh filtri tanlanmoqda: {range_text}")
        try:
            # Maosh dropdown'ni topish va ochish - text="Maosh" bilan
            salary_dropdown = self.page.get_by_text("Maosh", exact=True).first
            salary_dropdown.click()
            self.page.wait_for_timeout(1000)

            # Kerakli variantni tanlash
            salary_option = self.page.get_by_text(range_text, exact=True)
            salary_option.click()
            self.page.wait_for_timeout(1000)
            self.logger.info(f"Maosh filtri tanlandi: {range_text}")
        except Exception as e:
            self.logger.error(f"Maosh filtrini tanlashda xatolik: {e}")
            raise

    # ==================== Ish turi filtri ====================
    def select_work_type(self, work_type: str):
        """
        Ish turini tanlash

        Args:
            work_type: "Ish joyidan", "Masofadan", "Gibrid(onlayn/oflayn)",
                      "Safarbar", "Kasanachi"
        """
        self.logger.info(f"Ish turi filtri tanlanmoqda: {work_type}")
        try:
            # Ish turi dropdown'ni ochish
            work_type_dropdown = self.page.get_by_text("Ish turi", exact=True).first
            work_type_dropdown.click()
            self.page.wait_for_timeout(1000)

            # Kerakli variantni tanlash
            work_type_option = self.page.get_by_text(work_type, exact=True)
            work_type_option.click()
            self.page.wait_for_timeout(1000)
            self.logger.info(f"Ish turi filtri tanlandi: {work_type}")
        except Exception as e:
            self.logger.error(f"Ish turi filtrini tanlashda xatolik: {e}")
            raise

    # ==================== Bandlik turi filtri ====================
    def select_employment_type(self, employment_type: str):
        """
        Bandlik turini tanlash

        Args:
            employment_type: "To'liq bandlik", "Vaqtincha ish", "Loyihaviy ish",
                            "Qo'shimcha ish", "Mavsumiy ish", "Qismang bandlik",
                            "Frilans", "Amaliyot", "Ko'ngilli ish"
        """
        self.logger.info(f"Bandlik turi filtri tanlanmoqda: {employment_type}")
        try:
            # Bandlik turi dropdown'ni ochish
            employment_dropdown = self.page.get_by_text("Bandlik turi", exact=True).first
            employment_dropdown.click()
            self.page.wait_for_timeout(1000)

            # Kerakli variantni tanlash
            employment_option = self.page.get_by_text(employment_type, exact=True)
            employment_option.click()
            self.page.wait_for_timeout(1000)
            self.logger.info(f"Bandlik turi filtri tanlandi: {employment_type}")
        except Exception as e:
            self.logger.error(f"Bandlik turi filtrini tanlashda xatolik: {e}")
            raise

    # ==================== Ish tajribasi filtri ====================
    def select_experience(self, experience: str):
        """
        Ish tajribasini tanlash

        Args:
            experience: "Tajribasiz", "0-1 yil", "1-3 yil", "3-6 yil", "6+ yil"
        """
        self.logger.info(f"Ish tajribasi filtri tanlanmoqda: {experience}")
        try:
            # Ish tajribasi dropdown'ni ochish - "Ish tajribasi(yil)" matni bilan
            experience_dropdown = self.page.get_by_text("Ish tajribasi(yil)", exact=True).first
            experience_dropdown.click()
            self.page.wait_for_timeout(1000)

            # Kerakli variantni tanlash
            experience_option = self.page.get_by_text(experience, exact=True)
            experience_option.click()
            self.page.wait_for_timeout(1000)
            self.logger.info(f"Ish tajribasi filtri tanlandi: {experience}")
        except Exception as e:
            self.logger.error(f"Ish tajribasi filtrini tanlashda xatolik: {e}")
            raise

    # ==================== Saralash filtri ====================
    def select_sort_option(self, sort_option: str):
        """
        Saralash turini tanlash

        Args:
            sort_option: "Joylangan sana bo'yicha (Yangi)",
                        "Joylangan sana bo'yicha (Eski)",
                        "Maosh bo'yicha (O'sish tartibida)",
                        "Maosh bo'yicha (Kamayish tartibida)",
                        "Ommaboplik bo'yicha (Ko'p ko'rilgan)",
                        "Ommaboplik bo'yicha (Ko'p murojaat qilingan)"
        """
        self.logger.info(f"Saralash filtri tanlanmoqda: {sort_option}")
        try:
            # Saralash dropdown'ni ochish
            sort_dropdown = self.page.get_by_text("Saralash", exact=True).first
            sort_dropdown.click()
            self.page.wait_for_timeout(1000)

            # Kerakli variantni tanlash
            sort_option_locator = self.page.get_by_text(sort_option, exact=True)
            sort_option_locator.click()
            self.page.wait_for_timeout(1000)
            self.logger.info(f"Saralash filtri tanlandi: {sort_option}")
        except Exception as e:
            self.logger.error(f"Saralash filtrini tanlashda xatolik: {e}")
            raise

    # ==================== Yordamchi metodlar ====================
    def clear_selected_filter(self):
        """Tanlangan filterni tozalash - oxirgi "X" button orqali va filterlarni qayta ochish"""
        self.logger.info("Tanlangan filter tozalanmoqda...")
        try:
            # Find all X buttons using pattern: /html/body/div[2]/main/div[1]/div[2]/div[1]/div[2]/div[*]/div/button/button
            # This will find buttons in div[1], div[2], div[3], etc.
            x_buttons_xpath = "/html/body/div[2]/main/div[1]/div[2]/div[1]/div[2]//div/button/button"
            x_buttons = self.page.locator(f"xpath={x_buttons_xpath}")

            count = x_buttons.count()
            self.logger.info(f"Topilgan X buttonlar soni: {count}")

            if count > 0:
                # Click the last X button (oxirgi tanlangan filter)
                x_buttons.last.click()
                self.page.wait_for_timeout(1500)
                self.logger.info("Tanlangan filter tozalandi (oxirgi X button)")
                # Filterlarni qayta ochish
                self.open_filters()
                return

            self.logger.warning("Tozalash tugmasi (X) topilmadi")

        except Exception as e:
            self.logger.warning(f"Filterni tozalashda xatolik (Bu normal bo'lishi mumkin): {e}")
            pass

    def clear_all_filters(self):
        """Barcha filterlarni tozalash"""
        self.logger.info("Barcha filterlar tozalanmoqda...")
        try:
            # "Tozalash" yoki "Clear" tugmasini topish va bosish
            clear_button = self.page.locator("text='Tozalash'").or_(self.page.locator("text='Clear'"))
            if clear_button.is_visible():
                clear_button.click()
                self.page.wait_for_timeout(1000)
                self.logger.info("Barcha filterlar tozalandi")
            else:
                self.logger.warning("Tozalash tugmasi topilmadi")
        except Exception as e:
            self.logger.error(f"Filterlarni tozalashda xatolik: {e}")
            raise

    def get_filtered_vacancies_count(self) -> int:
        """Filtrlangan vakansiyalar sonini qaytarish"""
        self.logger.info("Filtrlangan vakansiyalar soni hisoblanmoqda...")
        try:
            # Vakansiya kartochkalarini hisoblash
            vacancy_cards = self.page.locator("[class*='vacancy_card_wrapper'], [class*='vacancy_card__']")
            count = vacancy_cards.count()
            self.logger.info(f"Filtrlangan vakansiyalar soni: {count}")
            return count
        except Exception as e:
            self.logger.error(f"Vakansiyalar sonini hisoblashda xatolik: {e}")
            raise

    def wait_for_filter_results(self, timeout: int = 5000):
        """Filter natijalarining yuklanishini kutish"""
        self.logger.info("Filter natijalari yuklanishi kutilmoqda...")
        try:
            # Vakansiya kartochkalari yuklanishini kutish
            self.page.wait_for_selector("[class*='vacancy_card_wrapper'], [class*='vacancy_card__']",
                                       state="visible",
                                       timeout=timeout)
            self.page.wait_for_timeout(1000)  # Qo'shimcha stabillik uchun
            self.logger.info("Filter natijalari yuklandi")
        except Exception as e:
            # Agar vakansiyalar topilmasa, bu normal holat bo'lishi mumkin (0 natija)
            self.logger.warning(f"Vakansiya kartochkalari topilmadi (0 natija bo'lishi mumkin): {e}")
            self.page.wait_for_timeout(1000)  # Sahifa yuklanishini kutish

    def verify_filter_applied(self, filter_name: str) -> bool:
        """
        Filter qo'llanganligini tekshirish

        Args:
            filter_name: Filter nomi

        Returns:
            bool: Filter qo'llangan bo'lsa True
        """
        self.logger.info(f"'{filter_name}' filtri qo'llanganligini tekshirish...")
        try:
            # Active filter badge'ni topish
            filter_badge = self.page.locator(f"[class*='filter_badge'], [class*='active_filter']").filter(has_text=filter_name)
            is_applied = filter_badge.is_visible()
            self.logger.info(f"Filter qo'llangan: {is_applied}")
            return is_applied
        except Exception as e:
            self.logger.error(f"Filter holatini tekshirishda xatolik: {e}")
            return False