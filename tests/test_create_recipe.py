import allure

from pages.create_recipe_page import CreateRecipePage
from test_data import RECIPE


@allure.feature("Создание рецепта")
class TestCreateRecipe:

    @allure.story("Успешное создание")
    @allure.title("После создания рецепта отображается его карточка")
    def test_recipe_card_is_displayed(self, logged_in_driver):
        recipe_page = CreateRecipePage(logged_in_driver)
        recipe_page.open()
        recipe_page.enter_name(RECIPE["name"])
        recipe_page.add_ingredient(RECIPE["ingredient"], RECIPE["amount"])
        recipe_page.enter_cooking_time(RECIPE["cooking_time"])
        recipe_page.enter_description(RECIPE["description"])
        recipe_page.upload_image(RECIPE["image"])
        recipe_page.submit()
        recipe_page.wait_for_recipe_card()

        titles = recipe_page.get_recipe_titles()
        assert len(titles) > 0, "Карточки рецептов не найдены после создания"

    @allure.story("Успешное создание")
    @allure.title("Карточка содержит название, указанное при создании")
    def test_recipe_card_contains_title(self, logged_in_driver):
        recipe_page = CreateRecipePage(logged_in_driver)
        recipe_page.open()
        recipe_page.enter_name(RECIPE["name"])
        recipe_page.add_ingredient(RECIPE["ingredient"], RECIPE["amount"])
        recipe_page.enter_cooking_time(RECIPE["cooking_time"])
        recipe_page.enter_description(RECIPE["description"])
        recipe_page.upload_image(RECIPE["image"])
        recipe_page.submit()
        recipe_page.wait_for_recipe_card()

        titles = recipe_page.get_recipe_titles()
        assert RECIPE["name"] in titles, (
            f"Название «{RECIPE['name']}» не найдено среди карточек: {titles}"
        )
