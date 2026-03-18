import allure

from pages.login_page import LoginPage
from test_data import EXISTING_USER


@allure.feature("Авторизация")
class TestLogin:

    @allure.story("Успешный вход")
    @allure.title("После входа происходит редирект на главную страницу")
    def test_login_redirects_to_main(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(EXISTING_USER["username"], EXISTING_USER["password"])
        login_page.wait_for_success_redirect()

        assert "/recipes" in login_page.get_current_url(), (
            f"Ожидали редирект на /recipes, получили: {login_page.get_current_url()}"
        )

    @allure.story("Успешный вход")
    @allure.title("После входа кнопка «Выход» отображается в шапке")
    def test_login_shows_logout_btn(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(EXISTING_USER["username"], EXISTING_USER["password"])
        login_page.wait_for_success_redirect()

        assert login_page.is_logout_btn_visible(), (
            "Кнопка «Выход» не найдена после успешной авторизации"
        )
