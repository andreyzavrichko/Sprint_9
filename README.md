# Sprint 9 — Автотесты Foodgram

Selenium + Allure автотесты для сервиса [Продуктовый помощник](https://foodgram-frontend-1.prakticum-team.ru/).

---

## Стек

| Инструмент | Версия | Назначение |
|---|--------|---|
| Python | 3.12   | Рантайм |
| Selenium | 4.18.1 | WebDriver |
| pytest | 8.1.1  | Тест-раннер |
| allure-pytest | 2.13.5 | Отчёт |
| Faker | 24.3.0 | Генерация тестовых данных |
| Selenoid | latest | Remote WebDriver |
| Chrome | 128.0  | Браузер |

---

## Структура проекта

```
Sprint_9/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD
├── assets/
│   └── test_image.jpg           # Тестовое фото для рецепта
├── pages/
│   ├── base_page.py             # BasePage: find / click / fill / wait
│   ├── login_page.py            # Страница авторизации /signin
│   ├── register_page.py         # Страница регистрации /signup
│   └── create_recipe_page.py    # Страница создания рецепта /recipes/create
├── tests/
│   ├── test_register.py         # Тесты: создание аккаунта
│   ├── test_login.py            # Тесты: авторизация
│   └── test_create_recipe.py    # Тесты: создание рецепта
├── conftest.py                  # Фикстуры: driver, logged_in_driver
├── test_data.py                 # Тестовые данные: EXISTING_USER, RECIPE
├── pytest.ini                   # Конфиг pytest + allure-results
├── requirements.txt             # Зависимости Python
├── Dockerfile                   # Образ с тестами
├── docker-compose.yml           # Selenoid + тесты
└── browser.json                 # Конфиг браузеров для Selenoid
```

---

## Тестовые сценарии

| # | Файл | Тест | Проверка |
|---|---|---|---|
| 1 | test_register.py | test_register_redirects_to_signin | После регистрации URL содержит /signin |
| 2 | test_register.py | test_register_shows_auth_form | После редиректа форма авторизации видна |
| 3 | test_login.py | test_login_redirects_to_main | После входа URL содержит /recipes |
| 4 | test_login.py | test_login_shows_logout_btn | После входа кнопка «Выход» видна |
| 5 | test_create_recipe.py | test_recipe_card_is_displayed | После создания страница рецепта открылась |
| 6 | test_create_recipe.py | test_recipe_card_contains_title | Заголовок рецепта совпадает с введённым |

---

## Быстрый старт

### 1. Предварительно: зарегистрировать EXISTING_USER

Вручную зарегистрировать пользователя на стенде с данными из `test_data.py`:
Пример:
```
email:    autotest_user@example.com
password: AutoTest123!
username: autotestuser
```

Или запустить `test_register` один раз, затем обновить `EXISTING_USER` в `test_data.py`.

---

### 2. Локальный запуск (Chrome)

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить все тесты
pytest

# Запустить с видимым браузером (без headless)
pytest --headless=false   # по умолчанию headless не задан — браузер откроется

# Запустить один тест
pytest tests/test_login.py::TestLogin::test_login_redirects_to_main -v

# Открыть Allure-отчёт
allure serve allure-results
```

---

### 3. Запуск через Selenoid (локально без Docker Compose)

```bash
# Шаг 1: скачать образ Chrome для Selenoid
docker pull selenoid/chrome:128.0

# Шаг 2: запустить Selenoid
docker run -d \
  --name selenoid \
  -p 4444:4444 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/browsers.json:/etc/selenoid/browsers.json:ro \
  aerokube/selenoid:latest \
  -conf /etc/selenoid/browsers.json -limit 4

# Шаг 3: запустить тесты против Selenoid
pytest --selenoid-uri http://localhost:4444/wd/hub --headless -v

# Шаг 4: остановить Selenoid после прогона
docker stop selenoid && docker rm selenoid
```

---

### 4. Запуск через Docker Compose (полная изоляция)

```bash
# Шаг 1: убедиться что образ Chrome скачан
docker pull selenoid/chrome:128.0

# Шаг 2: собрать образ и запустить
docker-compose up --build

# Allure-результаты будут в ./allure-results на хосте
# Открыть отчёт после прогона:
allure serve allure-results
```

Остановить всё:
```bash
docker-compose down
```

Пересобрать образ с нуля (если менялся код):
```bash
docker-compose up --build --force-recreate
```

---

### 5. GitHub Actions (CI/CD)

Push в `main`/ `develop` запускает автоматический прогон.

Результаты публикуются в GitHub Pages ветки `gh-pages`.

После этого Allure-отчёт будет доступен по адресу:
```
https://andreyzavrichko.github.io/Sprint_9/
```

---

## Переменные и тестовые данные

Все данные сосредоточены в `test_data.py`:

```python
EXISTING_USER = {
    "email": "test@test.test",
    "password": "Passw0rd$",
    ...
}

RECIPE = {
    "name": f"Автотест Борщ {uuid}",
    "ingredient": "капу",     
    "amount": "300",
    "cooking_time": "60",
    ...
}
```

---

## CLI-опции pytest

| Опция | Описание | Пример |
|---|---|---|
| `--selenoid-uri` | URL Selenoid WebDriver | `http://localhost:4444/wd/hub` |
| `--headless` | Запуск Chrome без GUI | флаг без значения |

---

## Allure-отчёт

```bash
# Генерировать HTML-отчёт в папку allure-report
allure generate allure-results -o allure-report --clean

# Открыть интерактивный сервер
allure serve allure-results
```
