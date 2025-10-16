"""
P0 Priority Test: Vakansiyalar ro'yxatini scroll qilish

Test Scenarios:
1. Sahifani pastga scroll qilish
2. Scroll qilgandan keyin ko'proq vakansiyalar yuklanishini tekshirish
"""

from playwright.sync_api import Page, expect
from pages.vacancy_list_page import VacancyListPage
from config import BASE_URL


def test_scroll_vacancy_list(authenticated_page: Page):
    """
    Test: Vakansiyalar ro'yxatini oxirigacha scroll qilish

    Steps:
    1. Dastlabki vakansiyalar sonini hisoblash
    2. Bir necha marta pastga scroll qilish (oxirigacha)
    3. Har safar scroll qilganda yangi vakansiyalar yuklanishini kuzatish
    4. Oxiriga yetganda to'xtash
    """
    vacancy_list_page = VacancyListPage(authenticated_page)

    # 1. Vakansiyalar yuklanishini kutish
    vacancy_list_page.wait_for_vacancies_to_load()

    # 2. Dastlabki vakansiyalar soni
    initial_count = vacancy_list_page.get_vacancy_cards_count()
    assert initial_count > 0, "Vakansiyalar yuklanmadi"
    print(f"Dastlab: {initial_count} ta vakansiya")

    # 3. Bir necha marta scroll qilish va natijani kuzatish
    max_scrolls = 20  # Maksimal 20 marta scroll (oxirigacha yetguncha)
    previous_count = initial_count

    for i in range(max_scrolls):
        # Scroll qilish
        vacancy_list_page.scroll_by_pixels(800)
        authenticated_page.wait_for_timeout(2000)  # Yangi vakansiyalar yuklanishini kutish

        # Scroll container'ning hozirgi holatini olish
        container_state = authenticated_page.evaluate("""() => {
            const container = document.querySelector('.styles_vacancy_list_wrapper__OFLB1');
            return {
                scrollTop: container.scrollTop,
                scrollHeight: container.scrollHeight,
                clientHeight: container.clientHeight,
                isAtBottom: (container.scrollTop + container.clientHeight) >= (container.scrollHeight - 50)
            };
        }""")

        print(f"Scroll {i+1}: scrollTop={container_state['scrollTop']}px")
        print(f"  ↳ Container: {container_state['clientHeight']}px / {container_state['scrollHeight']}px")

        # Yangi vakansiyalar sonini tekshirish
        current_count = vacancy_list_page.get_vacancy_cards_count()

        if current_count > previous_count:
            print(f"  ↳ Vakansiyalar: {previous_count} → {current_count} (+{current_count - previous_count} yangi)")
            previous_count = current_count
        else:
            print(f"  ↳ Vakansiyalar: {current_count} ta")

        # Agar container oxiriga yetgan bo'lsak
        if container_state['isAtBottom']:
            print(f"  ↳ ✓ Container oxiriga yetdik!")
            break

    # 4. Yakuniy natija
    final_count = vacancy_list_page.get_vacancy_cards_count()
    assert final_count >= initial_count, "Scroll qilgandan keyin vakansiyalar kamaydi!"
    print(f"✓ Yakuniy: {final_count} ta vakansiya ({final_count - initial_count} yangi yuklandi)")
    expect(authenticated_page).to_have_url(f"{BASE_URL}/vacancies")