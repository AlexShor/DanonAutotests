from selenium.webdriver.common.by import By

from pages.site_data.element_texts import (BasePage as BPTxt,
                                           BaseScenarioPage as BSTxt,
                                           InputTabScenarioPage as IptTxt,
                                           PFRTabScenarioPage as PFRTxt,
                                           OutputTabScenarioPage as OtpTxt,
                                           CreateScenarioPage as CrtTxt)

ui_lang = 'ru'


class BasePageLocators:
    HTML_TAG = (By.XPATH, '//html')
    BODY_TAG = (By.XPATH, '//body')
    SCROLL_BLOCK = (By.XPATH, '//div[contains(@class, "_scroll_")]')

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
    ITEM_IN_SELECTOR = (By.XPATH, '(//div[@class="rc-select-item-option-content" and text()="{}"])[last()]/..')
    SELECT_DROPDOWN = (By.XPATH, '//div[contains(@class, "rc-select-dropdown-cont")]//div[text()="{}]')

    SIDEBAR = (By.XPATH, '//aside[contains(@class, "_sidebar_")]')
    PROJECT_SELECTOR = (By.XPATH, SIDEBAR[1] + SELECTOR[1])
    ALL_SCENARIOS_BUTTON = (By.XPATH, SIDEBAR[1] + f'//span[text()="{BPTxt.ALL_SCENARIOS_BUTTON[ui_lang]}"]/..')
    OPEN_MENU_BUTTON = (By.XPATH, SIDEBAR[1] + '//div[contains(@class, "_openMenu_")]')


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
    INPUT_NAME = (By.XPATH, f'//span[text()="{CrtTxt.INPUT_NAME[ui_lang]}"]/..//input')
    INPUT_DESCRIPTION = (By.XPATH, f'//span[text()="{CrtTxt.INPUT_DESCRIPTION[ui_lang]}"]/..//input')
    INPUT_GRANULARITY = (By.XPATH,
                         f'//span[text()="{CrtTxt.INPUT_GRANULARITY[ui_lang]}"]'
                         f'/..//span[contains(@class, "_input_")]')
    SELECT_GROUP = (By.XPATH, f'//span[text()="{CrtTxt.SELECT_GROUP[ui_lang]}"]/..//input')
    SELECT_PERIOD = (By.XPATH, f'//span[text()="{CrtTxt.SELECT_PERIOD[ui_lang]}"]/..//input')
    SELECT_TYPE = (By.XPATH, f'//span[text()="{CrtTxt.SELECT_TYPE[ui_lang]}"]/..//input')
    SELECT_DATE_BUCKET = (By.XPATH, f'//span[text()="{CrtTxt.SELECT_DATE_BUCKET[ui_lang]}"]/..//input')
    SELECT_DATE_FORMAT = (By.XPATH, f'//span[text()="{CrtTxt.SELECT_DATE_FORMAT[ui_lang]}"]/..//input')
    SELECT_RANDOMIZER_TYPE = (By.XPATH, f'//span[text()="{CrtTxt.SELECT_RANDOMIZER_TYPE[ui_lang]}"]/..//input')
    CHECK_BOX_SOURCING = (By.XPATH, f'//div[text()="{CrtTxt.CHECK_BOX_SOURCING[ui_lang]}"]/../.')
    CHECK_BOX_MILK = (By.XPATH, f'//div[text()="{CrtTxt.CHECK_BOX_MILK[ui_lang]}"]/../.')
    CHECK_BOX_SOURCING_CHECKED = (By.XPATH, f'//div[contains(@class, "_checked_")]'
                                            f'//div[text()="{CrtTxt.CHECK_BOX_SOURCING[ui_lang]}"]')
    CHECK_BOX_MILK_CHECKED = (By.XPATH, f'//div[contains(@class, "_checked_")]'
                                        f'//div[text()="{CrtTxt.CHECK_BOX_MILK[ui_lang]}"]')


class BaseScenarioPageLocators(BasePageLocators):
    SCENARIO_HEADER = (By.XPATH, '//div[contains(@class, "cenarioHeader_")]')
    SCENARIO_TITLE = (By.XPATH, '//div[contains(@class, "cenarioTitle_")]')
    SCENARIO_SUBTITLE = (By.XPATH, '//div[contains(@class, "cenarioSubtitle_")]')
    SCENARIO_SUBTITLE_ELEMENTS = (By.XPATH, SCENARIO_SUBTITLE[1] + '/SPAN')
    SELECT_EDIT_ACCESS = (By.XPATH, SCENARIO_HEADER[1] + BasePageLocators.SELECTOR[1])
    SELECT_GROUP_UPLOAD_FROM_SCENARIO = (
        By.XPATH,
        f'//div[@class="rc-select-selector"]//span[text()='
        f'"{BSTxt.SELECT_GROUP_UPLOAD_FROM_SCENARIO[ui_lang]}"]')

    TABS = (By.XPATH, '//div[contains(@class, "_tabs_")]/div[contains(@class, "_tabs_")]')
    TAB_INPUT = (By.XPATH, TABS[1] + f'//span[text()="{BSTxt.INPUT_TAB[ui_lang]}"]/../..')
    TAB_PFR = (By.XPATH, TABS[1] + f'//span[text()="{BSTxt.PFR_TAB[ui_lang]}"]/../..')
    TAB_OUTPUT = (By.XPATH, TABS[1] + f'//span[text()="{BSTxt.OUTPUT_TAB[ui_lang]}"]/../..')
    DARK_TAB_INPUT = (By.XPATH, TABS[1] +
                      f'//div[contains(@class, "_dark_")]//span[text()="{BSTxt.INPUT_TAB[ui_lang]}"]')
    DARK_TAB_PFR = (By.XPATH, TABS[1] +
                    f'//div[contains(@class, "_dark_")]//span[text()="{BSTxt.PFR_TAB[ui_lang]}"]')
    DARK_TAB_OUTPUT = (By.XPATH, TABS[1] +
                       f'//div[contains(@class, "_dark_")]//span[text()="{BSTxt.OUTPUT_TAB[ui_lang]}"]')
    TAB_CALCULATE_AND_RESULT = (By.XPATH, TABS[1] +
                                f'//span[text()="{BSTxt.CALC_AND_RESULT_TAB[ui_lang]}"]/../..')
    DARK_TAB_CALCULATE_AND_RESULT = (
        By.XPATH, TABS[1] +
        f'//div[contains(@class, "_dark_")]//span[text()="{BSTxt.CALC_AND_RESULT_TAB[ui_lang]}"]')

class InputTabLocators(BaseScenarioPageLocators):
    TAB_TITLE = (By.XPATH,
                 f'//div[contains(@class, "_tabTitle_") and text()="{IptTxt.INPUT_TAB_TITLE[ui_lang]}"]')

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

    CONTAINER_INPUT = (By.XPATH, '//div[contains(@class, "_containerInput_")]')
    INPUT_TABS = (By.XPATH, CONTAINER_INPUT[1] +
                  '//div[contains(@class, "_inputTabs_")]/div[contains(@class, "_tabs_")]')

    INPUT_TAB_MD = (By.XPATH,
                    INPUT_TABS[1] + f'//span[text()="{IptTxt.TETRIS_INPUT_TAB_MD[ui_lang]}"]/../..')
    INPUT_TAB_SOURCING = (By.XPATH,
                          INPUT_TABS[1] + f'//span[text()="{IptTxt.TETRIS_INPUT_TAB_SOURCING[ui_lang]}"]/../..')
    INPUT_TAB_INDUSTRY = (By.XPATH,
                          INPUT_TABS[1] + f'//span[text()="{IptTxt.TETRIS_INPUT_TAB_INDUSTRY[ui_lang]}"]/../..')
    INPUT_TAB_OPTIMILK = (By.XPATH,
                          INPUT_TABS[1] + f'//span[text()="{IptTxt.TETRIS_INPUT_TAB_OPTIMILK[ui_lang]}"]/../..')

    INPUT_TAB_SOURCING_LOG = (By.XPATH, INPUT_TABS[1] +
                              f'//span[text()="{IptTxt.TETRIS_NEW_INPUT_TAB_SOURCING[ui_lang]}"]/../..')
    INPUT_TAB_MILK = (By.XPATH, INPUT_TABS[1] +
                      f'//span[text()="{IptTxt.TETRIS_NEW_INPUT_TAB_MILK[ui_lang]}"]/../..')

    ACTIVE_INPUT_TAB_MD = (
        By.XPATH, INPUT_TABS[1] +
        f'//div[contains(@class, "_active_")]//span[text()="{IptTxt.TETRIS_INPUT_TAB_MD[ui_lang]}"]')
    ACTIVE_INPUT_TAB_SOURCING = (
        By.XPATH, INPUT_TABS[1] +
        f'//div[contains(@class, "_active_")]//span[text()="{IptTxt.TETRIS_INPUT_TAB_SOURCING[ui_lang]}"]')
    ACTIVE_INPUT_TAB_INDUSTRY = (
        By.XPATH, INPUT_TABS[1] +
        f'//div[contains(@class, "_active_")]//span[text()="{IptTxt.TETRIS_INPUT_TAB_INDUSTRY[ui_lang]}"]')
    ACTIVE_INPUT_TAB_OPTIMILK = (
        By.XPATH, INPUT_TABS[1] +
        f'//div[contains(@class, "_active_")]//span[text()="{IptTxt.TETRIS_INPUT_TAB_OPTIMILK[ui_lang]}"]')

    ACTIVE_INPUT_TAB_SOURCING_LOG = (
        By.XPATH, INPUT_TABS[1] +
        f'//div[contains(@class, "_active_")]//span[text()="{IptTxt.TETRIS_NEW_INPUT_TAB_SOURCING[ui_lang]}"]')
    ACTIVE_INPUT_TAB_MILK = (
        By.XPATH, INPUT_TABS[1] +
        f'//div[contains(@class, "_active_")]//span[text()="{IptTxt.TETRIS_NEW_INPUT_TAB_MILK[ui_lang]}"]')


class PFRTabLocators(BaseScenarioPageLocators):
    TAB_TITLE = (By.XPATH, f'//h2[contains(@class, "_title_") and text()="{PFRTxt.PFR_TAB_TITLE[ui_lang]}"]')
    APPLY_BUTTON = (By.XPATH, '//button[contains(@class, "_applyButton_")]')

    BLOCKS_WRAPPER = (By.XPATH, '//form//div[contains(@class, "_blocksWrapper_")]')
    BLOCKS_WITH_TITLE = (By.XPATH, BLOCKS_WRAPPER[1] + '//p[contains(@class, "_blocksTitle_") and text()="{}"]/..')
