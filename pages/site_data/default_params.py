import os


class ProjectType:
    PROMO = 'promo'
    RTM = 'rtm'
    TETRIS = 'tetris-old'
    TETRIS_NEW = 'tetris'
    CFR = 'cfr'


class DefaultProjectLanguage:
    TYPE = {ProjectType.PROMO: 'en',
            ProjectType.RTM: 'en',
            ProjectType.TETRIS: 'en',
            ProjectType.TETRIS_NEW: 'ru',
            ProjectType.CFR: 'en'}


class ScenarioTypes:
    TYPE = {ProjectType.PROMO: 'promo-scenarios',
            ProjectType.RTM: 'rtm-scenarios',
            ProjectType.TETRIS: 'tetris-old-scenarios',
            ProjectType.TETRIS_NEW: 'tetris-scenarios',
            ProjectType.CFR: 'cfr-scenarios'}


class CreateScenarioDefaultParams:
    PROMO_PARAMS = {'Group': 'regular scenario', 'Period': '2023 Q4'}
    RTM_PARAMS = {'Group': 'Regular', 'Type': 'RTM Optimizer'}
    TETRIS_PARAMS = {'Group': 'Regular', 'Date Bucket': 'RF (Month)', 'Date format': '%yM%m'}
    TETRIS_NEW_PARAMS = {'Группа': 'RF', 'Молочный баланс': True, 'Сорсинг и логистика': True}
    CFR_PARAMS = {'Group': 'Regular', 'Type': 'Optimizer', 'Randomizer regime': 'Demand randomizer'}


class DefaultProjectNames:
    PROJECT_NAME = {ProjectType.PROMO: 'QA_Promo_optimizer_1',
                    ProjectType.RTM: 'QA_RTM_Optimizer_1',
                    ProjectType.TETRIS: 'QA_Tetris_Optimizer_1',
                    ProjectType.TETRIS_NEW: 'QA_Tetris_Optimizer_1',
                    ProjectType.CFR: 'QA_CFR_Optimizer_1'}


class DefaultInputFilePaths:
    CURRENT_FOLDER = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-2])
    PATH = {ProjectType.PROMO: CURRENT_FOLDER + '\\input_files\\files\\promo\\input_files\\',
            ProjectType.RTM: CURRENT_FOLDER + '\\input_files\\files\\rtm\\input_files\\',
            ProjectType.TETRIS: CURRENT_FOLDER + '\\input_files\\files\\tetris\\valid_input_files\\',
            ProjectType.TETRIS_NEW: CURRENT_FOLDER + '\\input_files\\files\\tetris_new\\input_files\\',
            ProjectType.CFR: CURRENT_FOLDER + '\\input_files\\files\\cfr\\input_files\\'}

    TETRIS_INPUT_TYPE_FILE_PATH = {'master-data': 'md',
                                   'sourcing-logistics': 'sourcing',
                                   'industry': 'industry',
                                   'optimilk': 'milkbalance'}

    TETRIS_NEW_INPUT_TYPE_FILE_PATH = {'sourcing': 'sourcing',
                                       'milk': 'milk'}
