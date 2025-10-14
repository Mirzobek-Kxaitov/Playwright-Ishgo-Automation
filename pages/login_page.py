from playwright.sync_api import Page, expect, TimeoutError
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Homepage'dagi Login tugmasi
        self.login_button = self.page.get_by_role("button", name="Login")
        # Modal ichidagi telefon input (type=tel)
        self.phone_input = self.page.locator("input[type='tel']")
        # Modal ichidagi submit button (XPath - tildan qat'iy nazar)
        self.submit_button = self.page.locator("xpath=/html/body/div[5]/div/div/div[2]/div/div/button[1]")
        # Login muvaffaqiyatli bo'lgandan keyin URL /vacancies bo'ladi
        # "Statistika" heading mavjud (bu vacancies sahifasida)

    def login(self, phone_number: str):
        """
        Saytga login qiladi - har doim to'liq login jarayonini bajaradi.
        """
        self.logger.info(f"Login jarayoni boshlandi. Telefon raqami: {phone_number}")

        # Login jarayonini bajarish
        try:
            self.logger.info("'Login' tugmasi bosilmoqda...")
            self.login_button.click(timeout=10000)
            self.page.wait_for_timeout(1000)  # Modal ochilishini ko'rish uchun
            self.logger.info("'Login' tugmasi muvaffaqiyatli bosildi - Modal ochildi")

            # Modal oynasi ochilishini kutish
            self.phone_input.wait_for(state="visible", timeout=5000)

            self.logger.info(f"Telefon raqami kiritilmoqda: {phone_number}")
            self.phone_input.fill(phone_number)
            self.page.wait_for_timeout(1000)  # Raqam kiritilishini ko'rish uchun
            self.logger.info("Telefon raqami muvaffaqiyatli kiritildi")

            self.logger.info("Modal ichidagi 'Kirish' tugmasi bosilmoqda...")
            self.submit_button.click()
            self.page.wait_for_timeout(1000)  # Tugma bosilishini ko'rish uchun
            self.logger.info("'Kirish' tugmasi muvaffaqiyatli bosildi")
        except TimeoutError as e:
            self.logger.error(f"Login jarayonida TimeoutError xatosi: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Login jarayonida kutilmagan xatolik: {e}")
            raise

        # Login muvaffaqiyatli bo'lgach, /vacancies URL'ga o'tganini kutish
        self.logger.info("'/vacancies' sahifasiga o'tishini kutilmoqda...")
        try:
            # URL /vacancies bo'lishini kutish
            self.page.wait_for_url("**/vacancies", timeout=15000)
            self.logger.info("Login jarayoni muvaffaqiyatli yakunlandi - /vacancies sahifasida")
        except Exception as e:
            self.logger.error(f"'/vacancies' sahifasiga o'ta olmadi - Login muvaffaqiyatsiz: {e}")
            raise
