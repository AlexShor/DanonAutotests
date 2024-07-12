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
            ProjectType.CFR: {'cfr_group_id': 1, 'cfr_type_id': 1, 'cfr_randomizer_regime_id': 1}
        },
        'DEMO_STAGE': {
            ProjectType.PROMO: {'promo_group_id': 1, 'promo_period_id': 11},
            ProjectType.RTM: {'rtm_group_id': 1, 'rtm_type_id': 1},
            ProjectType.TETRIS: {'tetris_group_id': 1, 'tetris_modules_id': [1, 2, 3]},
            ProjectType.CFR: {'cfr_group_id': 1, 'cfr_type_id': 1, 'cfr_randomizer_regime_id': 1}
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


class DefaultProject:

    __params = {
        'DEV': {
            ProjectType.PROMO: {'id': 0, 'name': 'QA_Promo_optimizer_1'},
            ProjectType.RTM: {'id': 0, 'name': 'QA_RTM_Optimizer_1'},
            ProjectType.TETRIS: {'id': 0, 'name': 'QA_Tetris_Optimizer_1'},
            ProjectType.CFR: {'id': 0, 'name': 'QA_CFR_Optimizer_1'},
        },
        'LOCAL_STAGE': {
            ProjectType.PROMO: {'id': 9, 'name': 'QA_Promo_optimizer_1'},
            ProjectType.RTM: {'id': 28, 'name': 'QA_RTM_Optimizer_1'},
            ProjectType.TETRIS: {'id': 35, 'name': 'QA_Tetris_Optimizer_1'},
            ProjectType.CFR: {'id': 41, 'name': 'QA_CFR_Optimizer_1'},
        },
        'DEMO_STAGE': {
            ProjectType.PROMO: {'id': 1, 'name': 'QA_Promo_optimizer_1'},
            ProjectType.RTM: {'id': 11, 'name': 'QA_RTM_Optimizer_1'},
            ProjectType.TETRIS: {'id': 28, 'name': 'QA_Tetris_Optimizer_1'},
            ProjectType.CFR: {'id': 19, 'name': 'QA_CFR_Optimizer_1'},
        },
        'PROD': {
            ProjectType.PROMO: {'id': 1, 'name': 'techjume Promo optimizer'},
            ProjectType.RTM: {'id': 17, 'name': 'techjume RTM test'},
            ProjectType.TETRIS: {'id': 11, 'name': 'techjume Tetris optimizer'},
            ProjectType.CFR: {'id': 18, 'name': 'techjume CFR test'},
        }
    }

    @classmethod
    def get(cls, environment: str, optimizer_type: str):
        return cls.__params[environment][optimizer_type]


class DefaultPFRdata:

    __params = {
        ProjectType.PROMO: {
            'main_params': {
                'promo-objectives': {"objective_func":"MVC, Abs","direction":"max","cust_level":"Chain","prod_level":"total products","holdout":"0"},
                'promo-customer-objectives': {"customer_objective":[{"distr_channel":"Others","chain":"YANDEX LAVKA","channel":"LOCAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"OZON","channel":"LOCAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"SAMOKAT","channel":"LOCAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"ATAC","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"AUCHAN","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"DC DIXY","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"HYPERGLOBUS","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"LENTA","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"MAGNIT","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"METRO","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"MONETKA","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"OKEY","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"PEREKRESTOK","channel":"NATIONAL KEY ACCOUNT"},{"distr_channel":"Others","chain":"PYATEROCHKA","channel":"NATIONAL KEY ACCOUNT"}]},
                'promo-product-objectives': {"product_objective":[{"modern_tradi":"TRADI","portfolio_category":"KEFIRS"},{"modern_tradi":"TRADI","portfolio_category":"MILKS"},{"modern_tradi":"TRADI","portfolio_category":"SMETANA, CREAM & BUTTER"},{"modern_tradi":"TRADI","portfolio_category":"TRADI_OTHER"},{"modern_tradi":"TRADI","portfolio_category":"TRADITIONAL CURDS"},{"modern_tradi":"TRADI","portfolio_category":"YOGHURTS & MODERNIZED CURDS"}]},
            },
            'additional_params': {
                'promo-constraint-coef': {"constraint_list":[{"constraint":"Promo Budget, Abs","sign":"=","ratio":1,"error":5,"type_hier":"total products"}]},
                'promo-constraint-ratio-first': {"constraint_ratio_first_list":[]},
                'promo-constraint-ratio-second': {"constraint_ratio_second_list":[]}
            }
        },
        ProjectType.RTM: {
            'main_params': {
                'wh-filter': {"wh_filters":["Not Available 5000","5100 RU DR HQ","5100 RU PL Petmol","5100 RU PL SAMARALAKTO","5100 RU PL EDELVEIS-M","5100 RU PL Saransk","5100 RU PL Lipetsk","5100 RU PL Vladimir","5100 RU PL Orel","5100 RU PL Volgograd","5100 RU PL Labinsk","5100 RU PL Tikhoretsk","5100 RU PL Ekaterinburg","5100 RU PL Shadrinsk","5100 RU PL Yalutorovsk","5100 RU PL Kemerovo","5100 RU PL MILKO","5100 RU PL Omsk","5100 RU PL Kostroma","5100 RU PL Chekhov","5500 RU PL Chekhov","XPO Logistik","5100 RU Delivery Fud","5100 RU KPD KARGO","5100 RU RP Saransk Remote","5100 RU RP DIAL","5100 RU RP IP Sutyagin","5100 RU RP Hladokombinat","5100 RU RP EDELVEIS-M Remote","5100 RU RP Yuryevets","5100 RU RP 4F","5100 RU RP SLG","5100 RU OKKAM","5100 RU RP Krasnoyarsk","5100 RU RP Kemerovo","Inactive 5500 RU RP Fruteks","5500 RU FRAGARIA","5500 RU DIAL GROUP LOGISTIC","Inactive 5500 HQ DANONE INDUST","5100 RU RP Fruteks","5100 RU FRAGARIA","5000 RU HQ Tomsk","5000 RU DC Tomsk","5000 RU DC Tomsk remote","5000 RU HQ Krasnoyarsk","5000 RU DC Krasnoyarsk","5000 RU DC Krasnoyarsk Remote","5000 RU DC Krasnoyarsk LP","5000 RU DC Stupino Dan","5000 RU DC Irkutsk","5000 RU DC Krasnoyarsk Tetra","5000 RU DC Troitse-Seltso","5000 RU HQ Novosibirsk","5000 RU DC Novosibirsk","5000 RU DC Novosibirsk Remote","5000 RU DC Omsk","5000 RU DC Barnaul","5000 RU HQ Kemerovo","5000 RU DC Kemerovo","5000 RU DC Novokuznetsk","5000 RU DC Kemerovo Resp1","5000 RU HQ Vladimir","5000 RU DC Vladimir","5000 RU DC Bogolybovo","5000 RU HQ Volgograd","5000 RU DC Volgograd","5000 RU HQ Yekaterinburg","5000 RU DC Yekaterinburg","5000 RU DC Yekaterinburg Rem","5000 RU DC Perm","5000 RU HQ Kostroma","5000 RU DC Kostroma","5000 RU HQ Krasnodar","5000 RU DC Krasnodar","5000 RU DC Rostov-na-Donu","5000 RU DC Labinsk","5000 RU DC Tikhoretsk","5000 RU HQ Lipetsk","5000 RU DC Lipetsk","5000 RU DC Lipetsk Remote","5000 RU HQ Moscow","5000 RU DC Klimovsk","5000 RU DC Pivdom","5000 RU HQ N.Novgorod","5000 RU DC N.Novgorod","5000 RU HQ Orel","5000 RU DC Orel","5000 RU HQ Samara","5000 RU DC Samara","5000 RU DC Saratov","5000 RU DC Togliatti","5000 RU HQ St. Petersburg","5000 RU DC Parnas","5000 RU DC Real","5000 RU DC 4F","5000 RU DC Porter","5000 RU HQ Saransk","5000 RU DC Saransk","5000 RU DC Saransk Remote","5000 RU HQ Smolensk","5000 RU DC Smolensk Logotrade","5000 RU DC Kaluga","5000 RU HQ Cheboksary","5000 RU DC Cheboksary","5000 RU HQ Shadrinsk","5000 RU DC Shadrinsk","5000 RU DC Chelyabinsk","5000 RU HQ Bekasovo","5000 RU HQ Tyumen","5000 RU DC Yalutorovsk","5000 RU DC Tyumen","5000 RU DC Surgut","5000 RU DC Yalutorovsk Resp1","5000 RU HQ Voronezh","5000 RU DC Voronezh","5000 RU HQ Tver","5000 RU DC Tver Logotrade","5000 RU HQ Kazan","5000 RU DC Kazan","5000 RU DC Kazan Remote","5000 RU DC Naberezhnye Chelny","5000 RU DC Ufa","5000 RU HQ Yaroslavl","5000 RU HQ Chekhov","5000 RU DC Chekhov","5000 RU KUM HQ Yekaterinburg","5000 RU KUM HQ Shadrinsk","5000 RU KUM HQ Yalutorovsk","5000 RU KUM HQ Cheboksary","5000 RU KUM HQ Kazan","5000 RU KUM HQ Saransk","5000 RU KUM HQ Samara","5000 RU KUM HQ Tikhoretsk","5000 RU KUM HQ Labinsk","5000 RU KUM HQ Volgograd","5000 RU KUM HQ Tomsk","5000 RU KUM HQ Kemerovo","5000 RU KUM HQ Novosibirsk","5000 RU Abrams","5100 RU ДР HQ RigaLand","5000 RU UM HQ RigaLand","5000 RU HQ RigaLand","Not Available 5200","4000 RU HQ Nutricia JSC","4000 RU PL Istra Factory","4000 RU DC Vnukovo Virt","5200 RU HQ Nutricia LLC","5200 RU DC Vnukovo  Admiral","5200 RU DC Spb  Admiral","5200 RU DC Ekb Uniland","5200 RU DC Artem Hermes","5200 RU DC Istra LLC","5200 RU DC Krasnodar","5200 RU DC Novosibirsk"]},
                'logistics-filter': {"region_filters":["East","Center","Other","West"]},
                'commercial-filter': {"commercial_filters":[{"filter_regions_rsd":"RSD EAST","filter_regions_bu":"BU EAST SIBERIA"},{"filter_regions_rsd":"RSD EAST","filter_regions_bu":"BU EKATERINBURG"},{"filter_regions_rsd":"RSD EAST","filter_regions_bu":"BU WEST SIBERIA"},{"filter_regions_rsd":"RSD EAST","filter_regions_bu":"BU CENTER SIBERIA"},{"filter_regions_rsd":"RSD MOSCOW","filter_regions_bu":"BU N.NOVGOROD"},{"filter_regions_rsd":"RSD MOSCOW","filter_regions_bu":"BU MOSCOW (CITY)"},{"filter_regions_rsd":"RSD MOSCOW","filter_regions_bu":"BU TULA"},{"filter_regions_rsd":"RSD MOSCOW","filter_regions_bu":"BU MOSCOW REGION"},{"filter_regions_rsd":"RSD SOUTH","filter_regions_bu":"BU KRASNODAR"},{"filter_regions_rsd":"RSD SOUTH","filter_regions_bu":"BU SOUTH URAL"},{"filter_regions_rsd":"RSD SOUTH","filter_regions_bu":"BU VOLGOGRAD"},{"filter_regions_rsd":"RSD SOUTH","filter_regions_bu":"BU NORTH CAUCASIAN"},{"filter_regions_rsd":"RSD WEST","filter_regions_bu":"BU ST. PETERBURG"},{"filter_regions_rsd":"RSD WEST","filter_regions_bu":"BU VOLGA"},{"filter_regions_rsd":"RSD WEST","filter_regions_bu":"BU NW REGION"},{"filter_regions_rsd":"#","filter_regions_bu":"#"}]}
            },
            'additional_params': None
        },
        ProjectType.TETRIS: None,
        ProjectType.CFR: {
            'Simulator': {
                'main_params': {
                    'params-for-run': {"cfr_params":[{"code":"Simulation start date","is_default":True,"value":20230401},{"code":"Simulation horizon (days)","is_default":False,"value":180}]}
                }
            },
            'Optimizer': {
                'main_params': {
                    'params-for-run': {"cfr_params":[{"code":"Simulation start date","is_default":True,"value":20230401},{"code":"Simulation horizon (days)","is_default":False,"value":180},{"code":"Min CFR threshold, %","is_default":False,"value":90},{"code":"Value step","is_default":False,"value":4}]}
                }
            },
            'Simulation (multi-level)': {
                'main_params': {
                    'params-for-run': {"cfr_params":[{"code":"Simulation start date","is_default":True,"value":20230401},{"code":"Simulation horizon (days)","is_default":False,"value":180},{"code":"Min CFR threshold, %","is_default":False,"value":90},{"code":"Value step","is_default":False,"value":4}]}
                }
            }
        },
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__params[optimizer_type]
