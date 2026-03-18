from pathlib import Path

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from endpoints import PATH_CREATE
from pages.base_page import BasePage

_PROJECT_ROOT = Path(__file__).parent.parent


class CreateRecipePage(BasePage):
    _RECIPE_NAME_INPUT = (By.XPATH,
                          "//div[contains(text(),'Название рецепта')]/following-sibling::input")
    _INGREDIENT_INPUT = (By.CSS_SELECTOR,
                         "input[class*='ingredientsInput']")
    _INGREDIENT_DROP = (By.CSS_SELECTOR,
                        "div[class*='container__3ukwm'] div:first-child")
    _INGREDIENT_AMOUNT = (By.CSS_SELECTOR,
                          "input[class*='ingredientsAmountValue']")
    _ADD_INGREDIENT_BTN = (By.CSS_SELECTOR,
                           "div[class*='ingredientAdd']")
    _COOKING_TIME_INPUT = (By.CSS_SELECTOR,
                           "div[class*='ingredientsTimeInput'] input")
    _DESCRIPTION_INPUT = (By.CSS_SELECTOR,
                          "textarea[class*='textareaField']")
    _FILE_INPUT = (By.CSS_SELECTOR,
                   "input[class*='fileInput'][type='file']")
    _SUBMIT_BTN = (By.XPATH,
                   "//button[normalize-space()='Создать рецепт']")
    _RECIPE_CARD_TITLE = (By.CSS_SELECTOR, "h1[class*='single-card__title']")

    @allure.step("Открываем страницу создания рецепта")
    def open(self) -> "CreateRecipePage":
        super().open(PATH_CREATE)
        return self

    @allure.step("Вводим название рецепта: {name}")
    def enter_name(self, name: str) -> "CreateRecipePage":
        self._fill(self._RECIPE_NAME_INPUT, name)
        return self

    @allure.step("Добавляем ингредиент: {ingredient} × {amount}")
    def add_ingredient(self, ingredient: str, amount: str) -> "CreateRecipePage":
        self._fill(self._INGREDIENT_INPUT, ingredient)
        self._click(self._INGREDIENT_DROP)
        self._fill(self._INGREDIENT_AMOUNT, amount)
        self._click(self._ADD_INGREDIENT_BTN)
        return self

    @allure.step("Вводим время приготовления: {minutes} мин")
    def enter_cooking_time(self, minutes: str) -> "CreateRecipePage":
        self._fill(self._COOKING_TIME_INPUT, minutes)
        return self

    @allure.step("Вводим описание рецепта")
    def enter_description(self, text: str) -> "CreateRecipePage":
        self._fill(self._DESCRIPTION_INPUT, text)
        return self

    @allure.step("Загружаем фото рецепта")
    def upload_image(self, relative_path: str) -> "CreateRecipePage":
        abs_path = str(_PROJECT_ROOT / relative_path)
        self._find(self._FILE_INPUT).send_keys(abs_path)
        return self

    @allure.step("Нажимаем «Создать рецепт»")
    def submit(self) -> "CreateRecipePage":
        self._click(self._SUBMIT_BTN)
        return self

    @allure.step("Ждём появления страницы созданного рецепта")
    def wait_for_recipe_card(self) -> None:
        WebDriverWait(self._driver, 15).until(
            lambda d: "/recipes/create" not in d.current_url
                      and "/recipes/" in d.current_url
        )
        self._find_visible(self._RECIPE_CARD_TITLE)

    @allure.step("Получаем заголовок созданного рецепта")
    def get_recipe_titles(self) -> list[str]:
        el = self._find_visible(self._RECIPE_CARD_TITLE)
        return [el.text.strip()]
