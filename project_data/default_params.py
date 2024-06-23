from datetime import datetime

from project_data.main_data import ProjectType


class CreateScenarioDefaultParams:

    __params = {
        'DEV': {
            ProjectType.PROMO: {'promo_group_id': 1, 'promo_period_id': 16},
            ProjectType.RTM: {'rtm_group_id': 1, 'rtm_type_id': 1},
            ProjectType.TETRIS: {'tetris_group_id': 1, 'tetris_modules_id': [1, 2, 3]},
            ProjectType.CFR: {'cfr_group_id': 1, 'cfr_type_id': 2, 'cfr_randomizer_regime_id': 1}
        },
        'LOCAL_STAGE': {
            ProjectType.PROMO: {'promo_group_id': 1, 'promo_period_id': 16},
            ProjectType.RTM: {'rtm_group_id': 1, 'rtm_type_id': 1},
            ProjectType.TETRIS: {'tetris_group_id': 1, 'tetris_modules_id': [1, 2, 3]},
            ProjectType.CFR: {'cfr_group_id': 1, 'cfr_type_id': 2, 'cfr_randomizer_regime_id': 1}
        },
        'DEMO_STAGE': {
            ProjectType.PROMO: {'promo_group_id': 1, 'promo_period_id': 11},
            ProjectType.RTM: {'rtm_group_id': 1, 'rtm_type_id': 1},
            ProjectType.TETRIS: {'tetris_group_id': 1, 'tetris_modules_id': [1, 2, 3]},
            ProjectType.CFR: {'cfr_group_id': 1, 'cfr_type_id': 2, 'cfr_randomizer_regime_id': 1}
        },
        'PROD': {
            ProjectType.PROMO: {'promo_group_id': 1, 'promo_period_id': 8},
            ProjectType.RTM: {'rtm_group_id': 1, 'rtm_type_id': 1},
            ProjectType.TETRIS: {'tetris_group_id': 1, 'tetris_modules_id': [1, 2, 3]},
            ProjectType.CFR: {'cfr_group_id': 1, 'cfr_type_id': 2, 'cfr_randomizer_regime_id': 1}
        }
    }

    # __params = {
    #     'DEV': {
    #         ProjectType.PROMO: {
    #             'group': {'id': 1, 'code': 'regular scenario'},
    #             'period': {'id': 16, 'year': 2024, 'quarter': 'Q4'}
    #         },
    #         ProjectType.RTM: {
    #             'group': {'id': 1, 'code': 'Regular'},
    #             'type': {'id': 1, 'code': 'CtS'}
    #         },
    #         ProjectType.TETRIS: {
    #             'group': {'id': 1, 'code': 'RF'},
    #             'modules': [{"id": 1, "code": "Sourcing"}, {"id": 2, "code": "Milk"}, {"id": 3, "code": "Industry"}]
    #         },
    #         ProjectType.CFR: {
    #             'group': {'id': 1, 'code': 'Regular'},
    #             'type': {'id': 2, 'code': 'Optimizer'},
    #             'randomizer_regime': {'id': 1, 'code': "No randomizer"}
    #         }
    #     }
    # }

    @classmethod
    def get(cls, environment: str, optimizer_type: str):

        params = cls.__params[environment][optimizer_type]
        params['description'] = 'QA Test'
        params['title'] = 'QA_test_scenario_' + datetime.now().strftime('%y%m%d_%H%M%S_%f')

        return params


class DefaultProjectNames:
    PROJECT_NAME = {ProjectType.PROMO: 'QA_Promo_optimizer_1',
                    ProjectType.RTM: 'QA_RTM_Optimizer_1',
                    ProjectType.TETRIS: 'QA_Tetris_Optimizer_1',
                    ProjectType.CFR: 'QA_CFR_Optimizer_1'}
