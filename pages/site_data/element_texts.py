class BasePage:
    ALL_SCENARIOS_BUTTON = {'en': 'All scenarios', 'ru': ''}


class BaseScenarioPage:
    INPUT_TAB = {'en': 'Input', 'ru': ''}
    PFR_TAB = {'en': 'Params for run', 'ru': ''}
    OUTPUT_TAB = {'en': 'Output', 'ru': ''}

    SELECT_GROUP_UPLOAD_FROM_SCENARIO = {'en': 'group upload from scenario', 'ru': ''}


class InputTabScenarioPage(BaseScenarioPage):
    INPUT_TAB_TITLE = {'en': 'Input', 'ru': ''}

    ITEM_IN_SELECTOR_FILE = {'en': 'local file', 'ru': ''}
    ITEM_IN_SELECTOR_SCENARIO = {'en': 'scenario based', 'ru': ''}
    PRELOADER_LOADING = {'en': 'loading', 'ru': ''}
    PRELOADER_CHECK = {'en': 'file check', 'ru': ''}
    PREVIEW_BUTTON = {'en': 'preview', 'ru': ''}
    CARD_INFO_UPLOADED = {'en': 'Uploaded on', 'ru': ''}
    CARD_INFO_COPIED = {'en': 'Copied', 'ru': ''}


class PFRTabScenarioPage(BaseScenarioPage):
    PFR_TAB_TITLE = {'en': 'Params for run', 'ru': ''}

    HIERARCHY_LEVEL_BLOCK_NAME = {'en': 'Select hierarchy level', 'ru': ''}
    HIERARCHY_ELEMENTS_BLOCK_NAME = {'en': 'Select hierarchy elements', 'ru': ''}
    TARGET_VARIABLE_BLOCK_NAME = {'en': 'Target variable', 'ru': ''}


class OutputTabScenarioPage(BaseScenarioPage):
    OUTPUT_TAB_TITLE = {'en': 'Output', 'ru': ''}


class CreateScenarioPage:
    HEADER = {'en': 'New scenario', 'ru': ''}
    INPUT_NAME = {'en': 'Name', 'ru': ''}
    INPUT_DESCRIPTION = {'en': 'Description', 'ru': ''}
    INPUT_GRANULARITY = {'en': 'Granularity', 'ru': ''}
    SELECT_GROUP = {'en': 'Group', 'ru': ''}
    SELECT_PERIOD = {'en': 'Period', 'ru': ''}
    SELECT_TYPE = {'en': 'Type', 'ru': ''}
    SELECT_DATE_BUCKET = {'en': 'Date Bucket', 'ru': ''}
    SELECT_DATE_FORMAT = {'en': 'Date format', 'ru': ''}
    SELECT_RANDOMIZER_TYPE = {'en': 'Randomizer regime', 'ru': ''}
