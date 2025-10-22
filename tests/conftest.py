import pytest
from playwright.sync_api import Page, BrowserContext
from pages.vacancies_page import VacanciesPage
from pages.login_page import LoginPage
from utils.logger import setup_logger
from config import PHONE_NUMBER, BASE_URL
import os
from pathlib import Path

# Test uchun logger
logger = setup_logger("TestRunner")

# Storage state fayli uchun yo'l
STORAGE_STATE_FILE = Path(__file__).parent.parent / ".auth" / "storage_state.json"


@pytest.fixture(scope="session")
def session_storage_state(browser):
    """
    Session scope fixture - bir marta login qilib, storage state'ni saqlaydi.
    Barcha testlar uchun bir marta login bo'ladi.
    """
    # Storage state fayli yo'lini yaratish
    STORAGE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Agar storage state mavjud bo'lsa va yangi bo'lsa, uni ishlatish
    if STORAGE_STATE_FILE.exists():
        logger.info("session_storage_state: Mavjud storage state topildi, uni ishlatamiz")
        return str(STORAGE_STATE_FILE)

    logger.info("session_storage_state: Yangi login jarayoni boshlanmoqda...")

    # Yangi context ochish va login qilish
    context = browser.new_context()
    page = context.new_page()

    try:
        # Login page orqali kirish
        from pages.login_page import LoginPage
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(PHONE_NUMBER)

        # Login muvaffaqiyatli bo'lganini tekshirish
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        logger.info("session_storage_state: Login muvaffaqiyatli yakunlandi")

        # Storage state'ni saqlash
        context.storage_state(path=str(STORAGE_STATE_FILE))
        logger.info(f"session_storage_state: Storage state saqlandi: {STORAGE_STATE_FILE}")

        return str(STORAGE_STATE_FILE)

    finally:
        context.close()


@pytest.fixture
def context(browser, session_storage_state):
    """
    Har bir test uchun yangi context, lekin saqlangan storage state bilan.
    Bu fixture pytest-playwright'ning standart context fixture'ini override qiladi.
    """
    logger.info("context fixture: Storage state bilan yangi context ochilmoqda...")
    context = browser.new_context(storage_state=session_storage_state)
    yield context
    context.close()


@pytest.fixture
def vacancies_page(page: Page) -> VacanciesPage:
    """VacanciesPage obyektini yaratuvchi fixture"""
    return VacanciesPage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage obyektini yaratuvchi fixture"""
    return LoginPage(page)


@pytest.fixture
def authenticated_page(page: Page) -> Page:
    """
    Tizimga kirgan holda sahifani qaytaruvchi fixture.
    Storage state orqali allaqachon login qilingan bo'ladi.
    """
    logger.info("authenticated_page fixture: Saqlangan session bilan sahifa yuklanmoqda...")

    # Vakansiyalar sahifasiga o'tish (allaqachon login qilingan)
    page.goto(f"{BASE_URL}/vacancies")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    logger.info("authenticated_page fixture: Sahifa tayyor (session qayta ishlatildi)")

    return page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Har bir test natijasini log qilish"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        if rep.passed:
            logger.info(f"✓ TEST PASSED: {item.nodeid}")
        elif rep.failed:
            logger.error(f"✗ TEST FAILED: {item.nodeid}")
            logger.error(f"Xatolik: {rep.longreprtext}")
        elif rep.skipped:
            logger.warning(f"⊘ TEST SKIPPED: {item.nodeid}")


def pytest_runtest_setup(item):
    """Test boshlanishidan oldin log yozish"""
    logger.info(f"{'='*80}")
    logger.info(f"TEST BOSHLANDI: {item.nodeid}")
    logger.info(f"{'='*80}")
