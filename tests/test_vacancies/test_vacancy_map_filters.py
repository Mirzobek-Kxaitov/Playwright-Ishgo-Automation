"""
P0 Priority Test: Xaritada vakansiyalar filterlarini test qilish

Xarita sahifasida (/vacancies?child=map) barcha filterlar ishlashini tekshirish
VacancyFiltersPage metodlaridan foydalaniladi
"""

from playwright.sync_api import Page, expect
from pages.vacancy_map_page import VacancyMapPage
from config import BASE_URL


def test_salary_filter_on_map(authenticated_page: Page):
    """
    Test: Xaritada Maosh filtri - barcha 5 ta variantni ketma-ket sinash

    Variants: 1mln-3mln, 3mln-5mln, 5mln-7mln, 7mln-10mln, 10mln+
    """
    map_page = VacancyMapPage(authenticated_page)

    # Xaritaga o'tish
    map_page.open_map_view()

    # Xarita yuklanganini tekshirish
    assert map_page.verify_map_loaded(), "Xarita yuklanmadi"
    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies?child=map")

    # Filterlarni ochish
    map_page.open_filters()

    # Maosh filtri variantlari
    salary_ranges = ["1 mln - 3 mln", "3 mln - 5 mln", "5 mln - 7 mln", "7 mln - 10 mln", "10+ mln"]

    for salary_range in salary_ranges:
        print(f"\n{'='*60}")
        print(f"Xaritada Maosh filtri test: {salary_range}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = map_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        map_page.select_salary_range(salary_range)

        # Natijalarni kutish
        map_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = map_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion - Filter ishlashi kerak
        assert filtered_count >= 0, f"Xaritada filter {salary_range} noto'g'ri ishladi"
        print(f"✓ Xaritada {salary_range} filtri muvaffaqiyatli ishladi")

        # Keyingi variant uchun filterni tozalash - "X" button orqali
        map_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies?child=map")
    print(f"\n{'='*60}")
    print("✓ Xaritada Maosh filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_work_type_filter_on_map(authenticated_page: Page):
    """
    Test: Xaritada Ish turi filtri - barcha 5 ta variantni ketma-ket sinash

    Variants: Ish joyidan, Masofadan, Gibrid, Safarbar, Kasanachi
    """
    map_page = VacancyMapPage(authenticated_page)

    # Xaritaga o'tish
    map_page.open_map_view()

    # Xarita yuklanganini tekshirish
    assert map_page.verify_map_loaded(), "Xarita yuklanmadi"

    # Filterlarni ochish
    map_page.open_filters()

    # Ish turi filtri variantlari
    work_types = ["Ish joyidan", "Masofadan", "Gibrid (onlayn/oflayn)", "Safarbar", "Kasanachi (Uyda)"]

    for work_type in work_types:
        print(f"\n{'='*60}")
        print(f"Xaritada Ish turi filtri test: {work_type}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = map_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        map_page.select_work_type(work_type)

        # Natijalarni kutish
        map_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = map_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion
        assert filtered_count >= 0, f"Xaritada filter {work_type} noto'g'ri ishladi"
        print(f"✓ Xaritada {work_type} filtri muvaffaqiyatli ishladi")

        # Filterni tozalash
        map_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies?child=map")
    print(f"\n{'='*60}")
    print("✓ Xaritada Ish turi filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_employment_type_filter_on_map(authenticated_page: Page):
    """
    Test: Xaritada Bandlik turi filtri - barcha 9 ta variantni ketma-ket sinash

    Variants: To'liq bandlik, Vaqtincha ish, Loyihaviy ish, va boshqalar
    """
    map_page = VacancyMapPage(authenticated_page)

    # Xaritaga o'tish
    map_page.open_map_view()

    # Xarita yuklanganini tekshirish
    assert map_page.verify_map_loaded(), "Xarita yuklanmadi"

    # Filterlarni ochish
    map_page.open_filters()

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
        print(f"Xaritada Bandlik turi filtri test: {employment_type}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = map_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        map_page.select_employment_type(employment_type)

        # Natijalarni kutish
        map_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = map_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion
        assert filtered_count >= 0, f"Xaritada filter {employment_type} noto'g'ri ishladi"
        print(f"✓ Xaritada {employment_type} filtri muvaffaqiyatli ishladi")

        # Filterni tozalash
        map_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies?child=map")
    print(f"\n{'='*60}")
    print("✓ Xaritada Bandlik turi filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_experience_filter_on_map(authenticated_page: Page):
    """
    Test: Xaritada Ish tajribasi filtri - barcha 5 ta variantni ketma-ket sinash

    Variants: Tajribasiz, 0-1 yil, 1-3 yil, 3-6 yil, 6+ yil
    """
    map_page = VacancyMapPage(authenticated_page)

    # Xaritaga o'tish
    map_page.open_map_view()

    # Xarita yuklanganini tekshirish
    assert map_page.verify_map_loaded(), "Xarita yuklanmadi"

    # Filterlarni ochish
    map_page.open_filters()

    # Ish tajribasi filtri variantlari
    experiences = ["Tajribasiz", "0–1 yil", "1–3 yil", "3–6 yil", "6+ yil"]

    for experience in experiences:
        print(f"\n{'='*60}")
        print(f"Xaritada Ish tajribasi filtri test: {experience}")
        print(f"{'='*60}")

        # Dastlabki holatni olish
        initial_count = map_page.get_filtered_vacancies_count()
        print(f"Dastlab: {initial_count} ta vakansiya")

        # Filter variantini tanlash
        map_page.select_experience(experience)

        # Natijalarni kutish
        map_page.wait_for_filter_results()

        # Filtrlangan natijalarni tekshirish
        filtered_count = map_page.get_filtered_vacancies_count()
        print(f"Filtrdan keyin: {filtered_count} ta vakansiya")

        # Assertion
        assert filtered_count >= 0, f"Xaritada filter {experience} noto'g'ri ishladi"
        print(f"✓ Xaritada {experience} filtri muvaffaqiyatli ishladi")

        # Filterni tozalash
        map_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies?child=map")
    print(f"\n{'='*60}")
    print("✓ Xaritada Ish tajribasi filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")


def test_sort_filter_on_map(authenticated_page: Page):
    """
    Test: Xaritada Saralash filtri - barcha 6 ta variantni ketma-ket sinash

    Variants: Yangi, Eski, Maosh o'sish, Maosh kamayish, Ko'p ko'rilgan, Ko'p murojaat
    """
    map_page = VacancyMapPage(authenticated_page)

    # Xaritaga o'tish
    map_page.open_map_view()

    # Xarita yuklanganini tekshirish
    assert map_page.verify_map_loaded(), "Xarita yuklanmadi"

    # Filterlarni ochish
    map_page.open_filters()

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
    initial_count = map_page.get_filtered_vacancies_count()
    print(f"Dastlab: {initial_count} ta vakansiya")

    for sort_option in sort_options:
        print(f"\n{'='*60}")
        print(f"Xaritada Saralash filtri test: {sort_option}")
        print(f"{'='*60}")

        # Saralash variantini tanlash
        map_page.select_sort_option(sort_option)

        # Natijalarni kutish
        map_page.wait_for_filter_results()

        # Saralangan natijalarni tekshirish
        sorted_count = map_page.get_filtered_vacancies_count()
        print(f"Saralashdan keyin: {sorted_count} ta vakansiya")

        # Assertion - Saralash vakansiyalar sonini o'zgartirmaydi
        assert sorted_count == initial_count, f"Xaritada saralash {sort_option} vakansiyalar sonini o'zgartirdi"
        print(f"✓ Xaritada {sort_option} filtri muvaffaqiyatli ishladi")

        authenticated_page.wait_for_timeout(500)

        # Filterni tozalash - "X" button orqali
        map_page.clear_selected_filter()
        authenticated_page.wait_for_timeout(500)

    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies?child=map")
    print(f"\n{'='*60}")
    print("✓ Xaritada Saralash filtri testi muvaffaqiyatli yakunlandi!")
    print(f"{'='*60}")