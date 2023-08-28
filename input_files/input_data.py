from operator import itemgetter

from pages.site_data.default_params import ProjectType as Ptype
from pages.site_data.urls import Paths

google_sheets_url = 'https://docs.google.com/spreadsheets/d/'


class Spreadsheets:
    class Promo:
        CHECK_INPUT = f'{google_sheets_url}1uYnl-r1F9AIMgAE4PNJSBXVmgvhcnu8PNcjWArUMYSI' + '/'
        INPUT_PROMO = f'{google_sheets_url}1fn4PxFE6bbyOTe0aPRUpYhEVC9uTDslF' + '/'

    class RTM:
        CHECK_INPUT = f'{google_sheets_url}1VYYQiF7ftxTdFj40cw1aPS_nTAvSBFWq' + '/'
        INPUT_RTM = f'{google_sheets_url}1gKS4J3tPOn1y-s9t5W5Mnf-SChoGTbJJ' + '/'

    class Tetris:
        CHECK_INPUT_OLD = f'{google_sheets_url}1YERmUHZL-cEIbWDW3NUGAnU6I8LhZcn-' + '/'
        CHECK_INPUT = f'{google_sheets_url}1TANskCVYrdvyiYa2ki3VPwaWN-G0avos' + '/'
        INPUT_MILK_BALANCE = f'{google_sheets_url}1KleiyYpvy_LxdklVIjBY18NGo2ygB36n' + '/'
        INPUT_MD = f'{google_sheets_url}1YL6eHd61hlxaDdIypljwGtp8BAIDstbQ' + '/'
        INPUT_INDUSTRY = f'{google_sheets_url}1GOyAx82lEWSb5MsdSIgj48CKlX8zxSJ-' + '/'
        INPUT_SOURCING = f'{google_sheets_url}1vz9V5l4bta_UDHa7NpersgI6I5ve3Y_h' + '/'

    class TetrisNew:
        CHECK_INPUT_OLD = f'{google_sheets_url}1YERmUHZL-cEIbWDW3NUGAnU6I8LhZcn-' + '/'
        CHECK_INPUT = f'{google_sheets_url}1TANskCVYrdvyiYa2ki3VPwaWN-G0avos' + '/'
        INPUT_MILK = f'{google_sheets_url}1WMJuYwMva13dKtmRWw2g4EXckbdYImgr' + '/'
        INPUT_SOURCING = f'{google_sheets_url}15zY1rJFOlmnwTXH9ZLfH4ZaBfX1xsUI4' + '/'

    class CFR:
        CHECK_INPUT = f'{google_sheets_url}1szjepPIIj3qt2B5aLqncG2yegI50-_t2' + '/'
        INPUT_CFR = f'{google_sheets_url}1RlZwjrDmh0xecyDm9RrA0qXPI66k532f' + '/'


class DataTypes:
    VARCHAR = 'VARCHAR'
    DATE = 'DATE'
    DECIMAL = 'DECIMAL'
    INT = 'INT'
    BOOL = 'BOOL'


class FillData(DataTypes):
    @staticmethod
    def get_value(data_type, validity=True):
        types = {True: {DataTypes.VARCHAR: 'varchar',
                        DataTypes.DATE: '01-01-2023',
                        DataTypes.DECIMAL: '111.45',
                        DataTypes.INT: '222',
                        DataTypes.BOOL: '1|TRUE:0|FALSE'},
                 False: {DataTypes.VARCHAR: '555',
                         DataTypes.DATE: 'date',
                         DataTypes.DECIMAL: 'decimal',
                         DataTypes.INT: 'int',
                         DataTypes.BOOL: '555'}}
        return types.get(validity).get(data_type)


class DataTypesErrorExceptions:
    DATA = [['gps', 'SKU_SAP_CODE'],
            ['routes', 'code_plant'],
            ['routes', 'id_sh#point1']]


class ErrorLogTexts:
    class Rus:
        OBLIGATION = 'Ошибки касающийся обязательных полей:'
        TYPE = 'Ошибки по типам полей:'
        NEGATIVE = 'Ошибки по неотрицательным значениям:'
        ROW = 'строка'
        COLUMN = 'колонка'

    class Eng:
        OBLIGATION = 'Errors regarding obligatory fields:'
        TYPE = 'Type errors:'
        NEGATIVE = 'Errors with non-negative values:'
        ROW = 'row'
        COLUMN = 'column'


class ScenarioTypes:
    TYPE = {Ptype.PROMO: 'promo-scenarios',
            Ptype.RTM: 'rtm-scenarios',
            Ptype.TETRIS: 'tetris-scenarios',
            Ptype.CFR: 'cfr-scenarios'}


class OptimizationTypes:
    TYPE = {
        Ptype.PROMO: None,
        Ptype.RTM: {
            'optimizer': 'RTM Optimizer',
            'cts': 'RTM CtS',
        },
        Ptype.TETRIS: None,
        Ptype.CFR: {
            'type': {
                'simulator': 'Simulator',
                'optimizer': 'Optimizer',
                'optimizer_multi_level': 'Optimizer (multi-level)'
            },
            'rnd_mode': {
                'no_randomizer': 'No randomizer',
                'demand_randomizer': 'Demand randomizer',
                'logistics_randomizer': 'Logistics randomizer'
            }
        }
    }


class InputTypeNameMatch:
    class Promo:
        scenario_type = ScenarioTypes.TYPE[Ptype.PROMO]

        TYPES = {
            'gps': {
                'scenario_type': scenario_type,
                'url_path': 'promo-gps',
                'system_file_name': 'gps',
                'front_name': 'GPS',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            },
            'distr_mapping': {
                'scenario_type': scenario_type,
                'url_path': 'promo-distr-mappings',
                'system_file_name': 'distr_mapping',
                'front_name': 'Distribution Mapping',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            },
            'combine_products': {
                'scenario_type': scenario_type,
                'url_path': 'promo-combine-products',
                'system_file_name': 'combine_products',
                'front_name': 'Combine Products',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            },
            'combine_chains': {
                'scenario_type': scenario_type,
                'url_path': 'promo-combine-chains',
                'system_file_name': 'combine_chains',
                'front_name': 'Combine Chains',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            },
            'up_down_size': {
                'scenario_type': scenario_type,
                'url_path': 'promo-up-down-sizes',
                'system_file_name': 'up_down_size',
                'front_name': 'Up/Down Size',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            },
            'prod_md': {
                'scenario_type': scenario_type,
                'url_path': 'promo-product-mds',
                'system_file_name': 'prod_md',
                'front_name': 'Product Masterdata',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            },
            'cust_md': {
                'scenario_type': scenario_type,
                'url_path': 'promo-customer-mds',
                'system_file_name': 'cust_md',
                'front_name': 'Customer Masterdata',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            },
            'lib': {
                'scenario_type': scenario_type,
                'url_path': 'promo-libs',
                'system_file_name': 'lib',
                'front_name': 'Promo Library',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.PROMO],)
            }
        }

    class RTM:
        scenario_type = ScenarioTypes.TYPE[Ptype.RTM]
        opti_type = OptimizationTypes.TYPE[Ptype.RTM]

        TYPES = {
            'fin_log_model': {
                'scenario_type': scenario_type,
                'system_file_name': 'fin_log_model',
                'front_name': 'Fin Log Model',
                'parameter': 'fin_log_model',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'fin_scorecard': {
                'scenario_type': scenario_type,
                'system_file_name': 'fin_scorecard',
                'front_name': 'Fin Scorecard',
                'parameter': 'fin_scorecard',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'md_ship_to': {
                'scenario_type': scenario_type,
                'system_file_name': 'md_ship_to',
                'front_name': 'MD shipTo',
                'parameter': 'md_ship_to',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'plants_info': {
                'scenario_type': scenario_type,
                'system_file_name': 'plants_info',
                'front_name': 'Plants info',
                'parameter': 'plants_info',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'wh_mapping': {
                'scenario_type': scenario_type,
                'system_file_name': 'wh_mapping',
                'front_name': 'WH mapping',
                'parameter': 'wh_mapping',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'drivers_break_old_version': {
                'scenario_type': scenario_type,
                'system_file_name': 'drivers_break_old_version',
                'front_name': 'Drivers break (old)',
                'parameter': 'drivers_break_old_version',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'drivers_break_mobile': {
                'scenario_type': scenario_type,
                'system_file_name': 'drivers_break_mobile',
                'front_name': 'Drivers break (mobile)',
                'parameter': 'drivers_break_mobile',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'distance_data': {
                'scenario_type': scenario_type,
                'system_file_name': 'distance_data',
                'front_name': 'Distance',
                'parameter': 'distance_data',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'wh_cost_split_cost': {
                'scenario_type': scenario_type,
                'system_file_name': 'wh_cost_split_cost',
                'front_name': 'Cost Split Cost WH',
                'parameter': 'wh_cost_split_cost',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            't2_cost_split_rule': {
                'scenario_type': scenario_type,
                'system_file_name': 't2_cost_split_rule',
                'front_name': 'Cost Split Rule T2',
                'parameter': 't2_cost_split_rule',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
            'conso_eod': {
                'scenario_type': scenario_type,
                'system_file_name': 'conso_eod',
                'front_name': 'Conso EOD',
                'parameter': 'conso_eod',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'transport_capacity': {
                'scenario_type': scenario_type,
                'system_file_name': 'transport_capacity',
                'front_name': 'Transport capacity',
                'parameter': 'transport_capacity',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'transport_availability': {
                'scenario_type': scenario_type,
                'system_file_name': 'transport_availability',
                'front_name': 'Transport availability',
                'parameter': 'transport_availability',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'mapping_plant': {
                'scenario_type': scenario_type,
                'system_file_name': 'mapping_plant',
                'front_name': 'Plant-Location mapping',
                'parameter': 'mapping_plant',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'plant_line_sku': {
                'scenario_type': scenario_type,
                'system_file_name': 'plant_line_sku',
                'front_name': 'Plant-Line-SKU',
                'parameter': 'plant_line_sku',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'dlc': {
                'scenario_type': scenario_type,
                'system_file_name': 'dlc',
                'front_name': 'DLC',
                'parameter': 'dlc',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'quarantine_soft_hard': {
                'scenario_type': scenario_type,
                'system_file_name': 'quarantine_soft_hard',
                'front_name': 'Quarantine',
                'parameter': 'quarantine_soft_hard',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'min_delivery_freq': {
                'scenario_type': scenario_type,
                'system_file_name': 'min_delivery_freq',
                'front_name': 'Min delivery frequency',
                'parameter': 'min_delivery_freq',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'min_delivery_freq_except': {
                'scenario_type': scenario_type,
                'system_file_name': 'min_delivery_freq_except',
                'front_name': 'Min delivery frequency (exceptions)',
                'parameter': 'min_delivery_freq_except',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'md_shipto_cust_group': {
                'scenario_type': scenario_type,
                'system_file_name': 'md_shipto_cust_group',
                'front_name': 'MD ShipTo Customer Group',
                'parameter': 'md_shipto_cust_group',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'wh_schedule': {
                'scenario_type': scenario_type,
                'system_file_name': 'wh_schedule',
                'front_name': 'WH Schedule',
                'parameter': 'wh_schedule',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'cost_pasting_copaking': {
                'scenario_type': scenario_type,
                'system_file_name': 'cost_pasting_copaking',
                'front_name': 'Pasting, copaking',
                'parameter': 'cost_pasting_copaking',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'client_requirements': {
                'scenario_type': scenario_type,
                'system_file_name': 'client_requirements',
                'front_name': 'Client Requirements',
                'parameter': 'client_requirements',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
        }

    class Tetris:
        URL_PATH_MD = Paths.URL_PATH_MD
        URL_PATH_SOURCING = Paths.URL_PATH_SOURCING
        URL_PATH_INDUSTRY = Paths.URL_PATH_INDUSTRY
        URL_PATH_OPTIMILK = Paths.URL_PATH_OPTIMILK
        scenario_type = ScenarioTypes.TYPE[Ptype.TETRIS]

        TYPES_MD = {
            'alt_names_locations': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'AlternativeLocations',
                'front_name': 'Alternative Names Locations',
                'parameter': 'alt_names_locations',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'alt_names_materials': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'AlternativeMaterials',
                'front_name': 'Alternative Names Materials',
                'parameter': 'alt_names_materials',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'alt_names_products': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'AlternativeProducts',
                'front_name': 'Alternative Names Products',
                'parameter': 'alt_names_products',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'alt_names_vendors': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'AlternativeVendors',
                'front_name': 'Alternative Names Vendors',
                'parameter': 'alt_names_vendors',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'calendars': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'Calendars',
                'front_name': 'Calendars',
                'parameter': 'calendars',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'locations': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'Locations',
                'front_name': 'Locations',
                'parameter': 'locations',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'material_groups': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'MaterialGroups',
                'front_name': 'Material Groups',
                'parameter': 'material_groups',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'materials': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'Materials',
                'front_name': 'Materials',
                'parameter': 'materials',
                'obligatory': True,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'products': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'Products',
                'front_name': 'Products',
                'parameter': 'products',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'vendors': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'VendorsBuyers',
                'front_name': 'Vendors',
                'parameter': 'vendors',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'uom': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_MD,
                'system_file_name': 'UOM',
                'front_name': 'UOM',
                'parameter': 'uom',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            }
        }

        TYPES_SOURCING = {
            'demand': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'OP(Demand)',
                'front_name': 'Demand',
                'parameter': 'demand',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'premade_volumes': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'Premade',
                'front_name': 'Premade Volumes',
                'parameter': 'premade_volumes',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'product_terms': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'Product Terms',
                'front_name': 'Product Terms',
                'parameter': 'product_terms',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'rejections': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'Rejects',
                'front_name': 'Rejections',
                'parameter': 'rejections',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            't1_adjustments': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'T1 Adjustments',
                'front_name': 'T1 Adjustments',
                'parameter': 't1_adjustments',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            't1_legs': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'T1 Legs',
                'front_name': 'T1 Legs',
                'parameter': 't1_legs',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            't1_scheme': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'Транспортная схема',
                'front_name': 'T1 Scheme',
                'parameter': 't1_scheme',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'trade_terms': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'Trade Terms',
                'front_name': 'Trade Terms',
                'parameter': 'trade_terms',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'sourcing_scheme': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'BP19DCPlant(сорсинг матрица)',
                'front_name': 'Sourcing Scheme',
                'parameter': 'sourcing_scheme',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'sourcing_settings': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_SOURCING,
                'system_file_name': 'Settings',
                'front_name': 'Sourcing Settings',
                'parameter': 'sourcing_settings',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            }
        }

        TYPES_INDUSTRY = {
            'bom': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_INDUSTRY,
                'system_file_name': 'BOM',
                'front_name': 'BOM',
                'parameter': 'bom',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'bom_replacements': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_INDUSTRY,
                'system_file_name': 'BOMSubstitutions',
                'front_name': 'BOM Replacements',
                'parameter': 'bom_replacements',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'line_capacity': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_INDUSTRY,
                'system_file_name': 'LineCapacity',
                'front_name': 'Line Capacity',
                'parameter': 'line_capacity',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'material_contents': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_INDUSTRY,
                'system_file_name': 'MaterialContents',
                'front_name': 'Material Contents',
                'parameter': 'material_contents',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'min_batches': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_INDUSTRY,
                'system_file_name': 'MinBatches',
                'front_name': 'Min-batches',
                'parameter': 'min_batches',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'mr_adjustments': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_INDUSTRY,
                'system_file_name': 'MRAdjustments',
                'front_name': 'MR Adjustments',
                'parameter': 'mr_adjustments',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'line_bindings': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_INDUSTRY,
                'system_file_name': 'PlantLineSKU',
                'front_name': 'Line Bindings',
                'parameter': 'line_bindings',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            }
        }

        TYPES_OPTIMILK = {
            'separation': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'BomSeparation',
                'front_name': 'Separation',
                'parameter': 'separation',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'regular_supplies': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'Commitments_M',
                'front_name': 'Regular Supplies',
                'parameter': 'regular_supplies',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'derivation_material': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'DerivationMaterial',
                'front_name': 'Ingredient Production',
                'parameter': 'derivation_material',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'co_packers': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'DisposalsCopacker',
                'front_name': 'Co-Packers',
                'parameter': 'co_packers',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'stop_buyers': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'DisposalsSpot',
                'front_name': 'Spot Buyers',
                'parameter': 'stop_buyers',  # stop_buyers
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'inbound_capacity': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'InboundCapacities',
                'front_name': 'Inbound Capacity',
                'parameter': 'inbound_capacity',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'mb_adjustments': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'MBAdjustments',
                'front_name': 'MB Adjustments',
                'parameter': 'mb_adjustments',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'new_farms': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'NewFarms_M',
                'front_name': 'New Farms',
                'parameter': 'new_farms',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'outbound_capacity': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'OutboundCapacities',
                'front_name': 'Outbound Capacity',
                'parameter': 'outbound_capacity',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'reco_material': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'RecoMaterial',
                'front_name': 'Recomb/Recon',
                'parameter': 'reco_material',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'shortage': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'Shortage',
                'front_name': 'Shortage',
                'parameter': 'shortage',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'spot_supplies': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'Spot_M',
                'front_name': 'Spot Supplies',
                'parameter': 'spot_supplies',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'material_stocks': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'Stock',
                'front_name': 'Material Stocks',
                'parameter': 'material_stocks',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'ts_farm_to_buyer': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'TSFarmToBuyer',
                'front_name': 'Transport Scheme farm-to-buyer',
                'parameter': 'ts_farm_to_buyer',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'ts_farm_to_plant': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'TSFarmToPlant',
                'front_name': 'Transport Scheme farm-to-plant',
                'parameter': 'ts_farm_to_plant',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'ts_plant_to_buyer': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'TSPlantToBuyer',
                'front_name': 'Transport Scheme plant-to-buyer',
                'parameter': 'ts_plant_to_buyer',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'ts_plant_to_plant': {
                'scenario_type': scenario_type,
                'url_path': URL_PATH_OPTIMILK,
                'system_file_name': 'TSPlantToPlant',
                'front_name': 'Transport Scheme plant-to-plant',
                'parameter': 'ts_plant_to_plant',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            }
        }

        TYPES = {**TYPES_MD, **TYPES_SOURCING, **TYPES_INDUSTRY, **TYPES_OPTIMILK}

    class TetrisNew:
        scenario_type = ScenarioTypes.TYPE[Ptype.TETRIS]

        TYPES_SOURCING = {
            'products': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Products',
                'front_name': 'Продукты',
                'parameter': 'products',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'innovations': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Innovations',
                'front_name': 'Инновации',
                'parameter': 'innovations',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'uoms': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Uoms',
                'front_name': 'Единицы измерения',
                'parameter': 'uoms',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'sourcing_calendars': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Calendars',
                'front_name': 'Календари',
                'parameter': 'sourcing_calendars',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'warehouses': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Warehouses',
                'front_name': 'Склады',
                'parameter': 'warehouses',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'sourcing_parameters': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Parameters',
                'front_name': 'Параметры',
                'parameter': 'sourcing_parameters',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'min_batches': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Min-batches',
                'front_name': 'Минимальные партии',
                'parameter': 'min_batches',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'line_capacities': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Line Capacities',
                'front_name': 'Мощности линий',
                'parameter': 'line_capacities',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'line_priorities': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Line Priorities',
                'front_name': 'Приоритеты линий',
                'parameter': 'line_priorities',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'mr_adjustments': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'MR Adjustments',
                'front_name': 'Корректировки ПП',
                'parameter': 'mr_adjustments',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'line_bindings': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Line Bindings',
                'front_name': 'Завод-линия-скю',
                'parameter': 'line_bindings',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'demand': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Demand',
                'front_name': 'План продаж',
                'parameter': 'demand',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'sourcing_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Sourcing Scheme',
                'front_name': 'План распределения',
                'parameter': 'sourcing_scheme',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'deliveries': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Deliveries',
                'front_name': 'Схема доставки',
                'parameter': 'deliveries',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'itineraries': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Itineraries',
                'front_name': 'Маршруты',
                'parameter': 'itineraries',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'shipments': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Shipments',
                'front_name': 'Мастер данные Т1',
                'parameter': 'shipments',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'premade_volumes': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Premade Volumes',
                'front_name': 'Дополнительные объемы',
                'parameter': 'premade_volumes',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'rejections': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Rejections',
                'front_name': 'Альтернативные источники',
                'parameter': 'rejections',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'demand_options': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Demand Options',
                'front_name': 'Настройки плана продаж',
                'parameter': 'demand_options',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            }
        }

        TYPES_MILK = {
            'milk_calendars': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Calendars',
                'front_name': 'Календари',
                'parameter': 'milk_calendars',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'plants': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Plants',
                'front_name': 'Заводы',
                'parameter': 'plants',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'materials': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Materials',
                'front_name': 'Материалы',
                'parameter': 'materials',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'material_contents': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Material Contents',
                'front_name': 'Характеристики материалов',
                'parameter': 'material_contents',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'material_groups': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Material Groups',
                'front_name': 'Группы материалов',
                'parameter': 'material_groups',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'vendors': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Vendors',
                'front_name': 'Поставщика',
                'parameter': 'vendors',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'buyers': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Buyers',
                'front_name': 'Покупатели',
                'parameter': 'buyers',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'milk_parameters': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Parameters',
                'front_name': 'Параметры',
                'parameter': 'milk_parameters',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'milk_table_parameters': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Table Parameters',
                'front_name': 'Табличные параметры',
                'parameter': 'milk_table_parameters',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'new_farms': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'New Farms',
                'front_name': 'Молоко новых ферм',
                'parameter': 'new_farms',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'regular_supplies': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Regular Supplies',
                'front_name': 'База поставок',
                'parameter': 'regular_supplies',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'spot_supplies': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Spot Supplies',
                'front_name': 'Спотовое молоко',
                'parameter': 'spot_supplies',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'shortage': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Shortage',
                'front_name': 'Дефицит',
                'parameter': 'shortage',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'stock_supplies': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Stock Supplies',
                'front_name': 'Начальные стоки',
                'parameter': 'stock_supplies',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'supply_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Supply Scheme',
                'front_name': 'ТЗР ферма-завод',
                'parameter': 'supply_scheme',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'farm_sales_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Farm Sales Scheme',
                'front_name': 'ТЗР ферма-покупатель',
                'parameter': 'farm_sales_scheme',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'plant_sales_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Plant Sales Scheme',
                'front_name': 'ТЗР завод-покупатель',
                'parameter': 'plant_sales_scheme',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'movement_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Movement Scheme',
                'front_name': 'ТЗР завод-завод',
                'parameter': 'movement_scheme',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'spot_buyers': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Spot Buyers',
                'front_name': 'Спотовые продажи',
                'parameter': 'spot_buyers',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'co_packers_contracts': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Copacker Contracts',
                'front_name': 'Продажи копакерам',
                'parameter': 'co_packers_contracts',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'reco_capabilities': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Reco Capabilities',
                'front_name': 'Возможности восстановления',
                'parameter': 'reco_capabilities',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'derivation': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Derivation',
                'front_name': 'Производство ингридиентов',
                'parameter': 'derivation',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'mb_adjustments': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'MB Adjustments',
                'front_name': 'Корректировки МБ',
                'parameter': 'mb_adjustments',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'separation': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Separation',
                'front_name': 'Сепарация',
                'parameter': 'separation',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'inbound_capacity': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Inbound Capacity',
                'front_name': 'Возможности приемки',
                'parameter': 'inbound_capacity',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'outbound_capacity': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Outbound Capacity',
                'front_name': 'Возможности отгрузки',
                'parameter': 'outbound_capacity',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'stock_bounds': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Stock Bounds',
                'front_name': 'Уровни стоков ЖС',
                'parameter': 'stock_bounds',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'base_formulas': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Base Formulas',
                'front_name': 'Базовые рецепты',
                'parameter': 'base_formulas',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
            'reco_formulas': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Reco Formulas',
                'front_name': 'Рецепты восстановления',
                'parameter': 'reco_formulas',
                'obligatory': False,
                'optimization_type': (OptimizationTypes.TYPE[Ptype.TETRIS],)
            },
        }

        TYPES = {**TYPES_SOURCING, **TYPES_MILK}

    class CFR:
        scenario_type = ScenarioTypes.TYPE[Ptype.CFR]
        opti_type = OptimizationTypes.TYPE[Ptype.CFR]
        all_opti_type = dict(type=tuple(opti_type['type'].values()), rnd_mode=tuple(opti_type['type'].values()))

        TYPES = {
            'min_cfr_max_pped': {
                'scenario_type': scenario_type,
                'system_file_name': 'min_cfr_max_pped',
                'front_name': 'Min CFR/Max PPED',
                'parameter': 'min_cfr_max_pped',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'optimizer_multi_level')(opti_type['type'])
            },
            'delta_fa_bias': {
                'scenario_type': scenario_type,
                'system_file_name': 'delta_fa_bias',
                'front_name': 'Delta FA bias',
                'parameter': 'delta_fa_bias',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('demand_randomizer')(opti_type['rnd_mode'])
            },
            'safety_days': {
                'scenario_type': scenario_type,
                'system_file_name': 'safety_days',
                'front_name': 'Safety days',
                'parameter': 'safety_days',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'coef': {
                'scenario_type': scenario_type,
                'system_file_name': 'coef',
                'front_name': 'Coef',
                'parameter': 'coef',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'routes': {
                'scenario_type': scenario_type,
                'system_file_name': 'routes',
                'front_name': 'Routes',
                'parameter': 'routes',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'moq': {
                'scenario_type': scenario_type,
                'system_file_name': 'moq',
                'front_name': 'Moq',
                'parameter': 'moq',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'fc': {
                'scenario_type': scenario_type,
                'system_file_name': 'fc',
                'front_name': 'FC',
                'parameter': 'fc',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'fact': {
                'scenario_type': scenario_type,
                'system_file_name': 'fact',
                'front_name': 'Fact',
                'parameter': 'fact',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'quarantine': {
                'scenario_type': scenario_type,
                'system_file_name': 'quarantine',
                'front_name': 'Quarantine',
                'parameter': 'quarantine',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'step_table': {
                'scenario_type': scenario_type,
                'system_file_name': 'step_table',
                'front_name': 'Step table',
                'parameter': 'step_table',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'dlc': {
                'scenario_type': scenario_type,
                'system_file_name': 'dlc',
                'front_name': 'DLC',
                'parameter': 'dlc',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'shipment_freq': {
                'scenario_type': scenario_type,
                'system_file_name': 'shipment_freq',
                'front_name': 'Shipment freq',
                'parameter': 'shipment_freq',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'costs': {
                'scenario_type': scenario_type,
                'system_file_name': 'costs',
                'front_name': 'Costs',
                'parameter': 'costs',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'frozen_horizon': {
                'scenario_type': scenario_type,
                'system_file_name': 'frozen_horizon',
                'front_name': 'Frozen horizon',
                'parameter': 'frozen_horizon',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'hubbing_days': {
                'scenario_type': scenario_type,
                'system_file_name': 'hubbing_days',
                'front_name': 'Hubbing days',
                'parameter': 'hubbing_days',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'md_locations': {
                'scenario_type': scenario_type,
                'system_file_name': 'md_locations',
                'front_name': 'Md locations',
                'parameter': 'md_locations',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            },
            'uom': {
                'scenario_type': scenario_type,
                'system_file_name': 'uom',
                'front_name': 'UOM',
                'parameter': 'uom',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
            }
        }
