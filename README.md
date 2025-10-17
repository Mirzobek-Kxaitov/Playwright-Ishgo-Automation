# Playwright Ishgo Automation

![Playwright Tests](https://github.com/YOUR_USERNAME/Playwright-Ishgo-Automation/workflows/Playwright%20Tests/badge.svg)

Playwright bilan yozilgan avtomatik test suit - Ishgo.uz platformasi uchun.

## Test Coverage

### Vakansiyalar Filterlari (List View)
- ✅ Maosh filtri (5 variant)
- ✅ Ish turi filtri (5 variant)
- ✅ Bandlik turi filtri (9 variant)
- ✅ Ish tajribasi filtri (5 variant)
- ✅ Saralash filtri (6 variant)

### Vakansiyalar Filterlari (Map View)
- ✅ Maosh filtri (5 variant)
- ✅ Ish turi filtri (5 variant)
- ✅ Bandlik turi filtri (9 variant)
- ✅ Ish tajribasi filtri (5 variant)
- ✅ Saralash filtri (6 variant)

**Jami: 60 ta test case**

## Texnologiyalar

- **Python 3.12**
- **Playwright** - Browser automation
- **Pytest** - Testing framework
- **Page Object Model (POM)** - Design pattern

## O'rnatish

```bash
# Virtual environment yaratish
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# yoki
.venv\Scripts\activate  # Windows

# Dependencies o'rnatish
pip install -r requirements.txt

# Playwright browsers o'rnatish
python -m playwright install chromium
```

## Testlarni ishga tushirish

### Lokal (headed mode - brauzer ko'rinadi)
```bash
pytest tests/ -v --headed --slowmo 1000
```

### CI/CD (headless mode - brauzer ko'rinmaydi)
```bash
pytest tests/ -v
```

### Aniq test fayl
```bash
pytest tests/test_vacancies/test_vacancy_filters.py -v
```

### Aniq test funksiya
```bash
pytest tests/test_vacancies/test_vacancy_filters.py::test_salary_filter -v
```

## Struktura

```
Playwright-Ishgo-Automation/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml    # CI/CD workflow
├── pages/
│   ├── base_page.py               # Base class
│   ├── login_page.py              # Login page
│   ├── vacancy_list_page.py       # Vacancy list page
│   ├── vacancy_filters_page.py    # Filters page
│   └── vacancy_map_page.py        # Map view page
├── tests/
│   └── test_vacancies/
│       ├── test_vacancy_list.py          # List tests
│       ├── test_vacancy_filters.py       # Filter tests
│       └── test_vacancy_map_filters.py   # Map filter tests
├── config.py                      # Configuration
├── conftest.py                    # Pytest fixtures
├── pytest.ini                     # Pytest config
└── requirements.txt               # Dependencies
```

## CI/CD

GitHub Actions orqali avtomatik testlar:
- ✅ Har push da
- ✅ Har pull request da
- ✅ Manual trigger

Test natijalarini GitHub Actions tab'da ko'rish mumkin.

## Hissa qo'shish

1. Repository'ni fork qiling
2. Feature branch yarating (`git checkout -b feature/new-test`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add new test'`)
4. Branch'ni push qiling (`git push origin feature/new-test`)
5. Pull Request oching

## Muallif

Test User Automation
