from selenium.webdriver.common.by import By


class BasePageLocators:
    JENIUS_BUTTON = (By.XPATH, '//button[contains(@class, "_circleCont_")]')
    JB_BUTTON = (By.XPATH, '//div[contains(@class, "_button_")]' + JENIUS_BUTTON[1])
    JB_SMALL = (By.XPATH, '//div[contains(@class, "_small_")]' + JENIUS_BUTTON[1])
    JB_LEFT = (By.XPATH, '//div[contains(@class, "_bottomLeft_") and contains(@class, "_scaleInMax_")]' +
               JENIUS_BUTTON[1])
    JB_BOTTOM = (By.XPATH, '//div[contains(@class, "_bottom_")]' + JENIUS_BUTTON[1])
    POPOVER = (By.XPATH, '//div[contains(@class, "_popover_")]')
    HEADER = (By.XPATH, '//h1[contains(@class, "_header_")]')
    BLOCK = (By.XPATH, '//div[contains(@class, "_wrap_") and contains(@class, "_block_")]')
    SELECTOR = (By.XPATH, '//div[@class="rc-select-selector"]')

    @staticmethod
    def select_item(item):
        return By.XPATH, f'//div[@class="rc-select-item-option-content" and text()="{item}"]/..'


class LoginPageLocators:
    INPUT_EMAIL = (By.XPATH, '//input[@type="email"]')
    INPUT_PASSWORD = (By.XPATH, '//input[@type="password"]')
    CHECKBOX_REMEMBER_ME = (By.XPATH, '//div[contains(@class, "_rememberMe_")]')
    FORGOT_PASS_BUTTON = (By.XPATH, '//div[contains(@class, "_forgot_")]/span')
    PASSWORD_EYE = (By.XPATH, '//div[contains(@class, "_noMultiline_")]/..//div[contains(@class, "_icon_")]')


class ScenarioListPageLocators:
    BLOCK_FILTERS = (By.XPATH, '//div[contains(@class, "_filters_")]')
    BLOCK_SEARCH = (By.XPATH, '//div[contains(@class, "_search_")]')


class CreateScenarioPageLocators(BasePageLocators):
    ITEM_WRAPPER = (By.XPATH, '//div[contains(@class, "_itemWrapper_")]')
    ITEM_NAME = (By.XPATH, '//span[contains(@class, "_itemName_")]')
    INPUT_NAME = (By.XPATH, '//span[text()="Name"]/..//input')
    INPUT_DESCRIPTION = (By.XPATH, '//span[text()="Description"]/..//input')
    INPUT_GRANULARITY = (By.XPATH, '//span[text()="Granularity"]/..//span[contains(@class, "_input_")]')
    SELECT_GROUP = (By.XPATH, '//span[text()="Group"]/..//input')
    SELECT_PERIOD = (By.XPATH, '//span[text()="Period"]/..//input')


class BaseScenarioPageLocators(BasePageLocators):
    SCENARIO_HEADER = (By.XPATH, '//div[contains(@class, "ScenarioHeader")]')
    SCENARIO_TITLE = (By.XPATH, '//div[contains(@class, "ScenarioTitle_")]')
    SCENARIO_SUBTITLE = (By.XPATH, '//div[contains(@class, "ScenarioSubtitle_")]')
    SCENARIO_SUBTITLE_ELEMENTS = (By.XPATH, SCENARIO_SUBTITLE[1] + '/SPAN')
    SELECT_EDIT_ACCESS = (By.XPATH, SCENARIO_HEADER[1] + BasePageLocators.SELECTOR[1])
    TABS = (By.XPATH, '//div[contains(@class, "_tabs_")]/div[contains(@class, "_tabs_")]')
    TAB_INPUT = (By.XPATH, TABS[1] + '//span[text()="Input"]/../..')
    TAB_PFR = (By.XPATH, TABS[1] + '//span[text()="Params for run"]/../..')
    TAB_OUTPUT = (By.XPATH, TABS[1] + '//span[text()="Output"]/../..')
