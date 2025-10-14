import pytest
from playwright.sync_api import Page
from pages.vacancies_page import VacanciesPage
from pages.login_page import LoginPage
from utils.logger import setup_logger
from config import PHONE_NUMBER

# Test uchun logger
logger = setup_logger("TestRunner")


@pytest.fixture
def vacancies_page(page: Page) -> VacanciesPage:
    """VacanciesPage obyektini yaratuvchi fixture"""
    return VacanciesPage(page)


@pytest.fixture(autouse=True)
def clear_cookies_before_test(page: Page):
    """Har bir testdan oldin cookie'larni tozalash"""
    page.context.clear_cookies()
    yield
    # Test tugagandan keyin ham tozalash (opsional)
    page.context.clear_cookies()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage obyektini yaratuvchi fixture"""
    return LoginPage(page)


@pytest.fixture
def authenticated_page(page: Page, login_page: LoginPage) -> Page:
    """
    Tizimga kirgan holda sahifani qaytaruvchi fixture.
    Bu fixture vakansiyalar va boshqa testlar uchun kerak.

    IMPORTANT: Har safar yangi session - cookie'larni tozalaydi va qayta login qiladi
    """
    logger.info("authenticated_page fixture: Cookie'larni tozalash...")
    page.context.clear_cookies()

    logger.info("authenticated_page fixture: Login jarayoni boshlanmoqda...")
    login_page.navigate()
    login_page.login(PHONE_NUMBER)
    logger.info("authenticated_page fixture: Login muvaffaqiyatli yakunlandi")
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
