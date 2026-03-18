"""
Тестовые данные.
EXISTING_USER — пользователь, созданный заранее (register раз вручную или через тест).
"""
from faker import Faker

_fake = Faker("ru_RU")

BASE_URL = "https://foodgram-frontend-1.prakticum-team.ru"

# ── Существующий пользователь (для тестов авторизации и создания рецепта) ───────
EXISTING_USER = {
    "email": "test@test.test",
    "password": "AutoTest123!",
    "username": "autotestuser-f-l",
    "first_name": "autotest_first_name",
    "last_name": "autotest_last_name",
}

# ── Генерация уникального пользователя на каждый прогон ─────────────────────────
def new_user() -> dict:
    uid = _fake.uuid4()[:8]
    return {
        "first_name": f"Test_{uid}",
        "last_name": f"User_{uid}",
        "username": f"user_{uid}",
        "email": f"user_{uid}@autotest.ru",
        "password": _fake.password(),
    }


# ── Данные нового рецепта ────────────────────────────────────────────────────────
RECIPE = {
    "name": f"Автотест Борщ {_fake.uuid4()[:8]}",
    "ingredient": "капу",          # первые символы — достаточно для автодополнения
    "amount": "300",
    "cooking_time": "60",
    "description": "Рецепт создан автотестом.",
    "image": "assets/test_image.png",  # путь относительно корня проекта
}
