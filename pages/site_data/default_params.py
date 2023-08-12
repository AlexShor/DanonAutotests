import os

#from ...input_files.input_data import InputTypeNameMatch as ITNM
#from .urls import Paths


class ProjectType:
    PROMO = 'promo'
    RTM = 'rtm'
    TETRIS = 'tetris'
    CFR = 'cfr'


class ScenarioTypes:
    TYPE = {ProjectType.PROMO: 'promo-scenarios',
            ProjectType.RTM: 'rtm-scenarios',
            ProjectType.TETRIS: 'tetris-scenarios',
            ProjectType.CFR: 'cfr-scenarios'}


class CreateScenarioDefaultParams:
    PROMO_PARAMS = {'Group': 'regular scenario', 'Period': '2023 Q4'}
    RTM_PARAMS = {'Group': 'Regular', 'Type': 'RTM Optimizer'}
    TETRIS_PARAMS = {'Group': 'Regular', 'Date Bucket': 'RF (Month)', 'Date format': '%yM%m'}
    CFR_PARAMS = {'Group': 'Regular', 'Type': 'Optimizer', 'Randomizer regime': 'Demand randomizer'}


class DefaultProjectNames:
    PROJECT_NAME = {ProjectType.PROMO: 'QA_Promo_optimizer_1',
                    ProjectType.RTM: 'QA_RTM_Optimizer_1',
                    ProjectType.TETRIS: 'QA_Tetris_Optimizer_2',
                    ProjectType.CFR: 'QA_CFR_Optimizer_2'}


class DefaultInputFilePaths:
    CURRENT_FOLDER = '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-2])
    PATH = {ProjectType.PROMO: CURRENT_FOLDER + '\\input_files\\files\\promo\\input_files\\',
            ProjectType.RTM: CURRENT_FOLDER + '\\input_files\\files\\rtm\\input_files\\',
            ProjectType.TETRIS: CURRENT_FOLDER + '\\input_files\\files\\tetris\\valid_input_files\\',
            ProjectType.CFR: CURRENT_FOLDER + '\\input_files\\files\\cfr\\input_files\\'}

    TETRIS_INPUT_TYPE_FILE_PATH = {'master-data': 'md',
                                   'sourcing-logistics': 'sourcing',
                                   'industry': 'industry',
                                   'optimilk': 'milkbalance'}
