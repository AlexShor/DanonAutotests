class BasePage:
    ALL_SCENARIOS_BUTTON = {'en': 'All scenarios', 'ru': 'Все сценарии'}


class BaseScenarioPage:
    INPUT_TAB = {'en': 'Input', 'ru': 'Входящие данные'}
    PFR_TAB = {'en': 'Params for run', 'ru': ''}
    OUTPUT_TAB = {'en': 'Output', 'ru': ''}
    CALC_AND_RESULT_TAB = {'en': 'Output', 'ru': 'Расчет и результат'}

    SELECT_GROUP_UPLOAD_FROM_SCENARIO = {'en': 'group upload from scenario', 'ru': 'массовая загрузка из сценария'}


class InputTabScenarioPage(BaseScenarioPage):
    INPUT_TAB_TITLE = {'en': 'Input', 'ru': 'Входящие данные'}

    ITEM_IN_SELECTOR_FILE = {'en': 'local file', 'ru': 'файл'}
    ITEM_IN_SELECTOR_SCENARIO = {'en': 'scenario based', 'ru': 'пред. сценарий'}
    PRELOADER_LOADING = {'en': 'loading', 'ru': 'загрузка'}
    PRELOADER_CHECK = {'en': 'file check', 'ru': 'Проверка файлов'}
    PREVIEW_BUTTON = {'en': 'preview', 'ru': 'предпросмотр'}
    CARD_INFO_UPLOADED = {'en': 'Uploaded on', 'ru': 'Загружено'}
    CARD_INFO_COPIED = {'en': 'Copied', 'ru': 'Скопировано'}

    TETRIS_INPUT_TAB_MD = {'en': 'masterdata', 'ru': ''}
    TETRIS_INPUT_TAB_SOURCING = {'en': 'sourcing&Logistics', 'ru': ''}
    TETRIS_INPUT_TAB_INDUSTRY = {'en': 'industry', 'ru': ''}
    TETRIS_INPUT_TAB_OPTIMILK = {'en': 'optimilk', 'ru': ''}

    TETRIS_NEW_INPUT_TAB_SOURCING = {'en': 'sourcing&Logistics', 'ru': 'Сорсинг и логистика'}
    TETRIS_NEW_INPUT_TAB_MILK = {'en': 'milkbalance', 'ru': 'Молочный баланс'}


class PFRTabScenarioPage(BaseScenarioPage):
    PFR_TAB_TITLE = {'en': 'Params for run', 'ru': ''}

    HIERARCHY_LEVEL_BLOCK_NAME = {'en': 'Select hierarchy level', 'ru': ''}
    HIERARCHY_ELEMENTS_BLOCK_NAME = {'en': 'Select hierarchy elements', 'ru': ''}
    TARGET_VARIABLE_BLOCK_NAME = {'en': 'Target variable', 'ru': ''}




class OutputTabScenarioPage(BaseScenarioPage):
    OUTPUT_TAB_TITLE = {'en': 'Output', 'ru': ''}


class CalcAndResultTabScenarioPage(BaseScenarioPage):
    CALC_AND_RESULT_TAB_TITLE = {'en': '', 'ru': 'Расчет и результат'}


class CreateScenarioPage:
    HEADER = {'en': 'New scenario', 'ru': 'Создание нового сценария'}
    INPUT_NAME = {'en': 'Name', 'ru': 'Имя'}
    INPUT_DESCRIPTION = {'en': 'Description', 'ru': 'Описание'}
    INPUT_GRANULARITY = {'en': 'Granularity', 'ru': ''}
    SELECT_GROUP = {'en': 'Group', 'ru': 'Группа'}
    SELECT_PERIOD = {'en': 'Period', 'ru': ''}
    SELECT_TYPE = {'en': 'Type', 'ru': ''}
    SELECT_DATE_BUCKET = {'en': 'Date Bucket', 'ru': ''}
    SELECT_DATE_FORMAT = {'en': 'Date format', 'ru': ''}
    SELECT_RANDOMIZER_TYPE = {'en': 'Randomizer regime', 'ru': ''}
    CHECK_BOX_SOURCING = {'en': '', 'ru': 'Сорсинг и логистика'}
    CHECK_BOX_MILK = {'en': '', 'ru': 'Молочный баланс'}
