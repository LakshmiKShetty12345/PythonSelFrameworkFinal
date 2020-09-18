from idlelib import browser
from lib2to3.pgen2 import driver

import drv as drv
import pytest
from pytest_html.extras import extra
from selenium import webdriver
from virtualenv import report


def pytest_addoption(parser):
    # TODO: Add support safari in future
    parser.addoption("--drv", action="store", default="ff,ie11",
                     help="Browser type. Possible value: ie11, chrome, ff, edge")
    parser.addoption("--url", action="store", required=False, default="http://localhost:3000/", help="frontend url")
    parser.addoption("--username", action="store", required=True, help="username")
    parser.addoption("--password", action="store", required=True, help="password")


@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome(executable_path="F:\\Python-Seleniumjars\\chromedriver.exe")
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path="F:\\Python-Seleniumjars\\geckodriver.exe")
    elif browser_name == "IE":
        print("IE driver")
    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()

    request.cls.driver = driver
    yield
    driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            file_name = report.nodeid.replace("::", "_").split("/")[1] + ".png"

            path = driver._capture_screenshot(file_name)
            drv = item.capture_screenshot(file_name)

            if file_name:
                extra.append(pytest_html.extras.image(path))
    report.extra = extra


def test_a(self, driver_init):

    assert 0


