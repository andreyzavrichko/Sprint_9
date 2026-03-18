import allure

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from test_data import new_user


@allure.feature("Регистрация")
class TestRegister:

    @allure.story("Успешная регистрация")
    @allure.title("После заполнения формы происходит редирект на /signin")
    def test_register_redirects_to_signin(self, driver):
        user = new_user()

        register_page = RegisterPage(driver)
        register_page.open()
        register_page.register(
            first_name=user["first_name"],
            last_name=user["last_name"],
            username=user["username"],
            email=user["email"],
            password=user["password"],
        )
        register_page.wait_for_redirect_to_signin()

        assert register_page.is_on_signin_page(), (
            f"Ожидали редирект на /signin, получили: {register_page.get_current_url()}"
        )

    @allure.story("Успешная регистрация")
    @allure.title("После редиректа отображается форма авторизации")
    def test_register_shows_auth_form(self, driver):
        user = new_user()

        register_page = RegisterPage(driver)
        register_page.open()
        register_page.register(
            first_name=user["first_name"],
            last_name=user["last_name"],
            username=user["username"],
            email=user["email"],
            password=user["password"],
        )
        register_page.wait_for_redirect_to_signin()

        login_page = LoginPage(driver)
        assert login_page.is_auth_form_visible(), (
            "Форма авторизации не отображается после регистрации"
        )
