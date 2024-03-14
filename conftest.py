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


# def custom_parametrize(data, arguments=(), skip=None, skip_reason='Skipped', **kwargs):
#     if skip is None:
#         skip = {}
#
#     args = [key for key in list(data.values())[0].keys() if key in arguments]
#     ids = list(data.keys())
#
#     formatted_data = []
#     for key, item in data.items():
#
#         if key in skip:
#             mark = getattr(pytest.mark, skip[key]['method'])(True, reason=skip[key].get('msg', skip_reason))
#         else:
#             mark = ()
#
#         formatted_data.append(pytest.param(*[item[a] for a in args], marks=mark))
#
#     return pytest.mark.parametrize(args, formatted_data, ids=ids, **kwargs)



# def pytest_runtest_makereport(item, call):
#     print()
#     print('item.keywords', *item.keywords)
#     print('call.excinfo', call.excinfo)
#     print('item.parent', item.parent)
#     print('item', item)
#     print()
#     if "incremental" in item.keywords:
#         if call.excinfo is not None:
#             parent = item.parent
#             parent._previousfailed = item
#
#
# def pytest_runtest_setup(item):
#     previousfailed = getattr(item.parent, "_previousfailed", None)
#     if previousfailed is not None:
#         pytest.xfail("previous test failed (%s)" % previousfailed.name)