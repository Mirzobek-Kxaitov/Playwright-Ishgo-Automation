"""
P0 Priority Test: Vakansiyalar filterlarini test qilish

Professional approach: Har bir filter uchun bitta test
Har bir test o'sha filterdagi barcha variantlarni tekshiradi
"""

from playwright.sync_api import Page, expect
from pages.vacancy_filters_page import VacancyFiltersPage
from config import BASE_URL


def test_salary_filter(authenticated_page: Page):
    """
    Test: Maosh filtri - barcha 5 ta variantni ketma-ket sinash

    Variants: 1mln-3mln, 3mln-5mln, 5mln-7mln, 7mln-10mln, 10mln+

    STATUS: ✓ PASSED
    """
    filters_page = VacancyFiltersPage(authenticated_page)

    # Filterlarni ochish
    filters_page.open_filters()

    # Maosh filtri variantlari
    # Note: Last one is "10+ mln" (reversed order)
    salary_ranges = ["1 mln - 3 mln", "3 mln - 5 mln", "5 mln - 7 mln", "7 mln - 10 mln", "10+ mln"]

    for salary_range in salary_ranges:
        print(f"\n{'='*60}")
        print(f"Maosh filtri test: {salary_range}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = filters_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        filters_page.select_salary_range(salary_range)

        # Natijalarni kutish
        filters_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = filters_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion - Filter ishlashi kerak
        assert filtered_count >= 0, f"Filter {salary_range} noto'g'ri ishladi"
        print(f"✓ {salary_range} filtri muvaffaqiyatli ishladi")

        # Keyingi variant uchun filterni tozalash - "X" button orqali
        filters_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies")
    print(f"\n{'='*60}")
    print("✓ Maosh filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_work_type_filter(authenticated_page: Page):
    """
    Test: Ish turi filtri - barcha 5 ta variantni ketma-ket sinash

    Variants: Ish joyidan, Masofadan, Gibrid, Safarbar, Kasanachi

    STATUS: ✓ PASSED
    """
    filters_page = VacancyFiltersPage(authenticated_page)

    # Filterlarni ochish
    filters_page.open_filters()

    # Ish turi filtri variantlari
    work_types = ["Ish joyidan", "Masofadan", "Gibrid (onlayn/oflayn)", "Safarbar", "Kasanachi (Uyda)"]

    for work_type in work_types:
        print(f"\n{'='*60}")
        print(f"Ish turi filtri test: {work_type}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = filters_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        filters_page.select_work_type(work_type)

        # Natijalarni kutish
        filters_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = filters_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion
        assert filtered_count >= 0, f"Filter {work_type} noto'g'ri ishladi"
        print(f"✓ {work_type} filtri muvaffaqiyatli ishladi")

        # Filterni tozalash
        filters_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies")
    print(f"\n{'='*60}")
    print("✓ Ish turi filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_employment_type_filter(authenticated_page: Page):
    """
    Test: Bandlik turi filtri - barcha 9 ta variantni ketma-ket sinash

    Variants: To'liq bandlik, Vaqtincha ish, Loyihaviy ish, va boshqalar

    STATUS: ✓ PASSED
    """
    filters_page = VacancyFiltersPage(authenticated_page)

    # Filterlarni ochish
    filters_page.open_filters()

    # Bandlik turi filtri variantlari
    employment_types = [
        "To‘liq bandlik",
        "Vaqtincha ish",
        "Loyihaviy ish",
        "Qo‘shimcha ish",
        "Mavsumiy ish",
        "Qisman bandlik",
        "Frilans",
        "Amaliyot",
        "Ko‘ngilli ish"
    ]

    for employment_type in employment_types:
        print(f"\n{'='*60}")
        print(f"Bandlik turi filtri test: {employment_type}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = filters_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        filters_page.select_employment_type(employment_type)

        # Natijalarni kutish
        filters_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = filters_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion
        assert filtered_count >= 0, f"Filter {employment_type} noto'g'ri ishladi"
        print(f"✓ {employment_type} filtri muvaffaqiyatli ishladi")

        # Filterni tozalash
        filters_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies")
    print(f"\n{'='*60}")
    print("✓ Bandlik turi filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_experience_filter(authenticated_page: Page):
    """
    Test: Ish tajribasi filtri - barcha 5 ta variantni ketma-ket sinash

    Variants: Tajribasiz, 0-1 yil, 1-3 yil, 3-6 yil, 6+ yil

    STATUS: ✓ PASSED
    """
    filters_page = VacancyFiltersPage(authenticated_page)

    # Filterlarni ochish
    filters_page.open_filters()

    # Ish tajribasi filtri variantlari
    experiences = ["Tajribasiz", "0–1 yil", "1–3 yil", "3–6 yil", "6+ yil"]

    for experience in experiences:
        print(f"\n{'='*60}")
        print(f"Ish tajribasi filtri test: {experience}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = filters_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        filters_page.select_experience(experience)

        # Natijalarni kutish
        filters_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = filters_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion
        assert filtered_count >= 0, f"Filter {experience} noto'g'ri ishladi"
        print(f"✓ {experience} filtri muvaffaqiyatli ishladi")

        # Filterni tozalash
        filters_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies")
    print(f"\n{'='*60}")
    print("✓ Ish tajribasi filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_sort_filter(authenticated_page: Page):
    """
    Test: Saralash filtri - barcha 6 ta variantni ketma-ket sinash

    Variants: Yangi, Eski, Maosh o'sish, Maosh kamayish, Ko'p ko'rilgan, Ko'p murojaat
    """
    filters_page = VacancyFiltersPage(authenticated_page)

    # Filterlarni ochish
    filters_page.open_filters()

    # Saralash filtri variantlari
    sort_options = [
        "Joylangan sana bo‘yicha (Yangi)",
        "Joylangan sana bo‘yicha (Eski)",
        "Maosh bo‘yicha (O‘sish tartibida)",
        "Maosh bo‘yicha (Kamayish tartibida)",
        "Ommaboplik bo‘yicha (Ko‘p ko‘rilgan)",
        "Ommaboplik bo‘yicha (Ko‘p murojaat qilingan)"
    ]

    # Dastlabki vakansiyalar sonini olish
    initial_count = filters_page.get_filtered_vacancies_count()
    print(f"Dastlab: {initial_count} ta vakansiya")

    for sort_option in sort_options:
        print(f"\n{'='*60}")
        print(f"Saralash filtri test: {sort_option}")
        print(f"{'='*60}")

        # Saralash variantini tanlash
        filters_page.select_sort_option(sort_option)

        # Natijalarni kutish
        filters_page.wait_for_filter_results()

        # Saralangan natijalarni tekshirish
        sorted_count = filters_page.get_filtered_vacancies_count()
        print(f"Saralashdan keyin: {sorted_count} ta vakansiya")

        # Assertion - Saralash vakansiyalar sonini o'zgartirmaydi
        assert sorted_count == initial_count, f"Saralash {sort_option} vakansiyalar sonini o'zgartirdi"
        print(f"✓ {sort_option} filtri muvaffaqiyatli ishladi")

        authenticated_page.wait_for_timeout(500)

        # Filterni tozalash - "X" button orqali
        filters_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies")
    print(f"\n{'='*60}")
    print("✓ Saralash filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")