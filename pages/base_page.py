from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    BASE_URL = "https://foodgram-frontend-1.prakticum-team.ru"
    TIMEOUT = 10

    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self, path: str = "") -> None:
        self._driver.get(self.BASE_URL + path)

    def get_current_url(self) -> str:
        return self._driver.current_url

    def wait_url_contains(self, fragment: str, timeout: int = TIMEOUT) -> None:
        WebDriverWait(self._driver, timeout).until(
            EC.url_contains(fragment)
        )

    def _find(self, locator: tuple):
        return self._wait.until(EC.presence_of_element_located(locator))

    def _find_clickable(self, locator: tuple):
        return self._wait.until(EC.element_to_be_clickable(locator))

    def _find_visible(self, locator: tuple):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def _find_all(self, locator: tuple) -> list:
        return self._wait.until(EC.presence_of_all_elements_located(locator))

    def _click(self, locator: tuple) -> None:
        self._find_clickable(locator).click()

    def _fill(self, locator: tuple, text: str) -> None:
        el = self._find_clickable(locator)
        el.clear()
        el.send_keys(text)

    def _is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self._driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
