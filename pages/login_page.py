import allure
from selenium.webdriver.common.by import By

from endpoints import PATH_LOGIN
from pages.base_page import BasePage


class LoginPage(BasePage):
    _EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    _PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    _LOGIN_BTN = (By.XPATH, "//button[normalize-space()='Войти']")
    _CREATE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/signup']")
    _LOGOUT_BTN = (By.XPATH, "//a[normalize-space()='Выход']")
    _AUTH_FORM = (By.CSS_SELECTOR, "form")

    @allure.step("Открываем страницу авторизации")
    def open(self) -> "LoginPage":
        super().open(PATH_LOGIN)
        return self

    @allure.step("Вводим email: {email}")
    def enter_email(self, email: str) -> "LoginPage":
        self._fill(self._EMAIL_INPUT, email)
        return self

    @allure.step("Вводим пароль")
    def enter_password(self, password: str) -> "LoginPage":
        self._fill(self._PASSWORD_INPUT, password)
        return self

    @allure.step("Нажимаем кнопку «Войти»")
    def click_login(self) -> "LoginPage":
        self._click(self._LOGIN_BTN)
        return self

    @allure.step("Выполняем авторизацию: {email}")
    def login(self, email: str, password: str) -> "LoginPage":
        self.enter_email(email).enter_password(password).click_login()
        return self

    @allure.step("Нажимаем «Создать аккаунт»")
    def click_create_account(self) -> None:
        self._click(self._CREATE_ACCOUNT_LINK)

    @allure.step("Проверяем: текущий URL содержит '/signin'")
    def is_on_login_page(self) -> bool:
        return "/signin" in self.get_current_url()

    @allure.step("Проверяем: форма авторизации отображается")
    def is_auth_form_visible(self) -> bool:
        return self._is_visible(self._AUTH_FORM)

    @allure.step("Ждём редиректа на главную страницу после входа")
    def wait_for_success_redirect(self) -> None:
        self.wait_url_contains("/recipes")

    @allure.step("Проверяем: кнопка «Выход» отображается")
    def is_logout_btn_visible(self) -> bool:
        return self._is_visible(self._LOGOUT_BTN)
