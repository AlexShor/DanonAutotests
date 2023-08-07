import pytest

from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption('--browser_name',
                     action='store',
                     default="chrome",
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language',
                     action='store',
                     default="en",
                     help="Choose browser language")

    parser.addoption('--base_url',
                     action='store',
                     default="DEV",
                     help="Choose base url")


@pytest.fixture()
def env(request):
    return request.config.getoption("base_url")


@pytest.fixture(scope="class")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    env = request.config.getoption("base_url")

    print(f'[browser={browser_name}] [language={user_language}] [env={env}]', end=' ')

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser
    browser.quit()


def dict_parametrize(data, **kwargs):
    args = list(list(data.values())[0].keys())
    formatted_data = [[item[a] for a in args] for item in data.values()]
    ids = list(data.keys())
    return pytest.mark.parametrize(args, formatted_data, ids=ids, **kwargs)
