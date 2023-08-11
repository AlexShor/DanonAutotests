class ProjectType:
    PROMO = 'promo'
    RTM = 'rtm'
    TETRIS = 'tetris'
    CFR = 'cfr'


class CreateScenarioDefaultParams:
    PROMO_PARAMS = {'Group': 'regular scenario', 'Period': '2023 Q4'}
    RTM_PARAMS = {'Group': 'Regular', 'Type': 'RTM Optimizer'}
    TETRIS_PARAMS = {'Group': 'Regular', 'Date Bucket': 'RF (Month)', 'Date format': '%yM%m'}
    CFR_PARAMS = {'Group': 'Regular', 'Type': 'Optimizer', 'Randomizer regime': 'Demand randomizer'}


class ChangeProjectTypeDefaultParams:
    PROJECT_NAME = {ProjectType.PROMO: 'QA_Promo_optimizer_1',
                    ProjectType.RTM: 'QA_RTM_Optimizer_1',
                    ProjectType.TETRIS: 'QA_Tetris_Optimizer_2',
                    ProjectType.CFR: 'QA_CFR_Optimizer_2'}
