import pytest
from playwright.sync_api import Page
from pages.vacancies_page import VacanciesPage
from pages.login_page import LoginPage


@pytest.fixture
def vacancies_page(page: Page) -> VacanciesPage:
    """VacanciesPage obyektini yaratuvchi fixture"""
    return VacanciesPage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage obyektini yaratuvchi fixture"""
    return LoginPage(page)
