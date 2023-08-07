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
        return By.XPATH, f'(//div[@class="rc-select-item-option-content" and text()="{item}"])[last()]/..'


class LoginPageLocators:
    INPUT_EMAIL = (By.XPATH, '//input[@type="email"]')
    INPUT_PASSWORD = (By.XPATH, '//input[@type="password"]')
    CHECKBOX_REMEMBER_ME = (By.XPATH, '//div[contains(@class, "_rememberMe_")]')
    FORGOT_PASS_BUTTON = (By.XPATH, '//div[contains(@class, "_forgot_")]/span')
    PASSWORD_EYE = (By.XPATH, '//div[contains(@class, "_noMultiline_")]/..//div[contains(@class, "_icon_")]')


class ScenarioListPageLocators(BasePageLocators):
    BLOCK_FILTERS = (By.XPATH, '//div[contains(@class, "_filters_")]')
    BLOCK_SEARCH = (By.XPATH, '//div[contains(@class, "_search_")]')
    SCENARIO_BLOCK = (By.XPATH, '//div[contains(@class, "_scenarioBlock_")]')
    SCENARIO_TITLE = (By.XPATH, SCENARIO_BLOCK[1] + '//p[contains(@class, "_title_") and text()="{}"]')
    MAIN_INFO = (By.XPATH, SCENARIO_BLOCK[1] + '//div[contains(@class, "_mainInfo_")]')
    ACTION_BUTTONS = (By.XPATH, SCENARIO_BLOCK[1] + '//div[contains(@class, "_actionButtons_")]')
    PROGRESS_INFO = (By.XPATH, SCENARIO_BLOCK[1] + '//div[contains(@class, "_progressInfo_")]')
    MAIN_INFO_TOOLTIPS = (By.XPATH, MAIN_INFO[1] + '//div[contains(@class, "_tooltip_") and contains(@class, "_top_")]')
    ACTION_BUTTON_EDIT = (By.XPATH, ACTION_BUTTONS[1] + '//div[contains(@class, "_wrap_")][1]')
    ACTION_BUTTON_COPY = (By.XPATH, ACTION_BUTTONS[1] + '//div[contains(@class, "_wrap_")][2]')
    ACTION_BUTTON_DELETE = (By.XPATH, ACTION_BUTTONS[1] + '//div[contains(@class, "_wrap_")][3]')
    PROGRESS_INFO_BUTTON = (By.XPATH, PROGRESS_INFO[1] + '//button[contains(@class, "_status_")]')
    PROGRESS_INFO_UPDATED = (By.XPATH, PROGRESS_INFO[1] + '//p[contains(@class, "_updated_")]')


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
    SELECT_GROUP_UPLOAD_FROM_SCENARIO = (
        By.XPATH,
        '//div[@class="rc-select-selector"]//span[text()="group upload from scenario"]')

    TABS = (By.XPATH, '//div[contains(@class, "_tabs_")]/div[contains(@class, "_tabs_")]')
    TAB_INPUT = (By.XPATH, TABS[1] + '//span[text()="Input"]/../..')
    TAB_PFR = (By.XPATH, TABS[1] + '//span[text()="Params for run"]/../..')
    TAB_OUTPUT = (By.XPATH, TABS[1] + '//span[text()="Output"]/../..')
    DARK_TAB_INPUT = (By.XPATH, TABS[1] + '//div[contains(@class, "_dark_")]//span[text()="Input"]')


class InputTabLocators(BaseScenarioPageLocators):
    TAB_TITLE = (By.XPATH, '//div[contains(@class, "_tabTitle_") and text()="Input"]')

    CARD = (By.XPATH, '//div[contains(@class, "_card_")]')
    CARD_TITLE = (By.XPATH, CARD[1] + '//div[contains(@class, "_cardTitle_") and text()="{}"]')
    CARD_CONTENT = (By.XPATH, '//div[contains(@class, "_cardContent_")]')
    CARD_CONTENT_BY_TITLE = (By.XPATH, CARD_TITLE[1] + '/../..' + CARD_CONTENT[1])

    SELECT = (By.XPATH, CARD_TITLE[1] + BasePageLocators.SELECTOR[1])
    SELECT_TYPE_DATA = (By.XPATH, CARD_CONTENT_BY_TITLE[1] + '/div[1]' + BasePageLocators.SELECTOR[1])

    UPLOAD_FILE_BUTTON = (By.XPATH, CARD_CONTENT_BY_TITLE[1] + '//input[@type="file"]')
    INFO_TAG_UPLOADED_DATA = (By.XPATH, CARD_CONTENT_BY_TITLE[1] + '//div[contains(@class, "_tag_")]')
    PREVIEW_BUTTON = (By.XPATH, CARD_CONTENT_BY_TITLE[1] + '//button[contains(@class, "_cardAction_")]')
    CARD_INFO_TEXT = (By.XPATH, CARD_CONTENT_BY_TITLE[1] + '//p[contains(@class, "_cardInfo_")]')

    PRELOADER = (By.XPATH, CARD_CONTENT_BY_TITLE[1] + '//div[contains(@class, "_loader_")]')
    PRELOADER_TEXT = (By.XPATH, PRELOADER[1] + '//div[text()="{}"]')
    PRELOADER_SPINNER_LARGE = (By.XPATH, CARD_CONTENT_BY_TITLE[1] + '//div[contains(@class, "_spinnerLarge_")]')

    POPOVER_MESSAGE_LIST = (By.XPATH, BasePageLocators.POPOVER[1] + '//div[contains(@class, "_messageList_")]')
    MESSAGE_IN_POPOVER_MESSAGE_LIST = (By.XPATH, POPOVER_MESSAGE_LIST[1] +
                                       '//span[contains(@class, "_messageText_") and text()="{}"]')
