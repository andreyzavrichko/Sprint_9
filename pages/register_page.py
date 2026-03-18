import allure
from selenium.webdriver.common.by import By

from endpoints import PATH_REGISTER
from pages.base_page import BasePage


class RegisterPage(BasePage):
    _FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[name='first_name']")
    _LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[name='last_name']")
    _USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    _EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    _PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    _SUBMIT_BTN = (By.XPATH, "//button[normalize-space()='Создать аккаунт']")
    _AUTH_LINK = (By.CSS_SELECTOR, "a[href='/signin']")

    @allure.step("Открываем страницу регистрации")
    def open(self) -> "RegisterPage":
        super().open(PATH_REGISTER)
        return self

    @allure.step("Заполняем форму регистрации")
    def fill_form(
            self,
            first_name: str,
            last_name: str,
            username: str,
            email: str,
            password: str,
    ) -> "RegisterPage":
        self._fill(self._FIRST_NAME_INPUT, first_name)
        self._fill(self._LAST_NAME_INPUT, last_name)
        self._fill(self._USERNAME_INPUT, username)
        self._fill(self._EMAIL_INPUT, email)
        self._fill(self._PASSWORD_INPUT, password)
        return self

    @allure.step("Нажимаем «Создать аккаунт»")
    def submit(self) -> "RegisterPage":
        self._click(self._SUBMIT_BTN)
        return self

    @allure.step("Регистрируемся: username={username}, email={email}")
    def register(
            self,
            first_name: str,
            last_name: str,
            username: str,
            email: str,
            password: str,
    ) -> "RegisterPage":
        self.fill_form(first_name, last_name, username, email, password).submit()
        return self

    @allure.step("Ждём редиректа на страницу авторизации")
    def wait_for_redirect_to_signin(self) -> None:
        self.wait_url_contains("/signin")

    @allure.step("Проверяем: текущий URL — страница авторизации")
    def is_on_signin_page(self) -> bool:
        return "/signin" in self.get_current_url()

    @allure.step("Проверяем: ссылка «Войти» отображается")
    def is_signin_link_visible(self) -> bool:
        return self._is_visible(self._AUTH_LINK)
