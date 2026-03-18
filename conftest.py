import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from test_data import EXISTING_USER



def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--selenoid-uri",
        action="store",
        default=None,
        help="Selenoid WebDriver URL, e.g. http://selenoid:4444/wd/hub",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запускать Chrome в headless-режиме",
    )


@pytest.fixture
def driver(request: pytest.FixtureRequest):
    selenoid_uri: str | None = request.config.getoption("--selenoid-uri")
    headless: bool = request.config.getoption("--headless")

    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    if headless:
        options.add_argument("--headless=new")

    if selenoid_uri:
        options.set_capability(
            "selenoid:options", {"enableVNC": False, "enableVideo": False}
        )
        browser = webdriver.Remote(
            command_executor=selenoid_uri,
            options=options,
        )
    else:
        browser = webdriver.Chrome(options=options)

    yield browser
    browser.quit()



@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(EXISTING_USER["username"], EXISTING_USER["password"])

    WebDriverWait(driver, 10).until(EC.url_contains("/recipes"))

    return driver
