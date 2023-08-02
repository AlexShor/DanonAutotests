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
    DATA = [['gps', 'SKU_SAP_CODE']]


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


class InputTypeNameMatch:
    class Promo:
        type_scenarios = 'promo-scenarios'

        TYPES = {
            'gps': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-gps',
                'file_name': 'gps',
                'front_name': 'GPS'
            },
            'distr_mapping': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-distr-mappings',
                'file_name': 'distr_mapping',
                'front_name': 'Distribution Mapping'
            },
            'combine_products': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-combine-products',
                'file_name': 'combine_products',
                'front_name': 'Combine Products'
            },
            'combine_chains': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-combine-chains',
                'file_name': 'combine_chains',
                'front_name': 'Combine Chains'
            },
            'up_down_size': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-up-down-sizes',
                'file_name': 'up_down_size',
                'front_name': 'Up/Down Size'
            },
            'prod_md': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-product-mds',
                'file_name': 'prod_md',
                'front_name': 'Product Masterdata'
            },
            'cust_md': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-customer-mds',
                'file_name': 'cust_md',
                'front_name': 'Customer Masterdata'
            },
            'lib': {
                'type_scenarios': type_scenarios,
                'url_path': 'promo-libs',
                'file_name': 'lib',
                'front_name': 'Promo Library'
            }
        }

    class RTM:
        TYPES = {
            'fin_log_model': {
                'file_name': 'fin_log_model',
                'front_name': 'Fin Log Model',
                'parameter': 'fin_log_model'
            },
            'fin_scorecard': {
                'file_name': 'fin_scorecard',
                'front_name': 'Fin Scorecard',
                'parameter': 'fin_scorecard'
            },
            'md_ship_to': {
                'file_name': 'md_ship_to',
                'front_name': 'MD shipTo',
                'parameter': 'md_ship_to'
            },
            'plants_info': {
                'file_name': 'plants_info',
                'front_name': 'Plants info',
                'parameter': 'plants_info'
            },
            'wh_mapping': {
                'file_name': 'wh_mapping',
                'front_name': 'WH mapping',
                'parameter': 'wh_mapping'
            },
            'drivers_break_old_version': {
                'file_name': 'drivers_break_old_version',
                'front_name': 'Drivers break (old)',
                'parameter': 'drivers_break_old_version'
            },
            'drivers_break_mobile': {
                'file_name': 'drivers_break_mobile',
                'front_name': 'Drivers break (mobile)',
                'parameter': 'drivers_break_mobile'
            },
            'distance_data': {
                'file_name': 'distance_data',
                'front_name': 'Distance',
                'parameter': 'distance_data'
            },
            'wh_cost_split_cost': {
                'file_name': 'wh_cost_split_cost',
                'front_name': 'Cost Split Cost WH',
                'parameter': 'wh_cost_split_cost'
            },
            't2_cost_split_rule': {
                'file_name': 't2_cost_split_rule',
                'front_name': 'Cost Split Rule T2',
                'parameter': 't2_cost_split_rule'
            },
            'conso_eod': {
                'file_name': 'conso_eod',
                'front_name': 'Conso EOD',
                'parameter': 'conso_eod'
            },
            'transport_capacity': {
                'file_name': 'transport_capacity',
                'front_name': 'Transport capacity',
                'parameter': 'transport_capacity'
            },
            'transport_availability': {
                'file_name': 'transport_availability',
                'front_name': 'Transport availability',
                'parameter': 'transport_availability'
            },
            'mapping_plant': {
                'file_name': 'mapping_plant',
                'front_name': 'Plant-Location mapping',
                'parameter': 'mapping_plant'
            },
            'plant_line_sku': {
                'file_name': 'plant_line_sku',
                'front_name': 'Plant-Line-SKU',
                'parameter': 'plant_line_sku'
            },
            'dlc': {
                'file_name': 'dlc',
                'front_name': 'DLC',
                'parameter': 'dlc'
            },
            'quarantine_soft_hard': {
                'file_name': 'quarantine_soft_hard',
                'front_name': 'Quarantine',
                'parameter': 'quarantine_soft_hard'
            },
            'min_delivery_freq': {
                'file_name': 'min_delivery_freq',
                'front_name': 'Min delivery frequency',
                'parameter': 'min_delivery_freq'
            },
            'min_delivery_freq_except': {
                'file_name': 'min_delivery_freq_except',
                'front_name': 'Min delivery frequency (exceptions)',
                'parameter': 'min_delivery_freq_except'
            },
            'md_shipto_cust_group': {
                'file_name': 'md_shipto_cust_group',
                'front_name': 'MD ShipTo Customer Group',
                'parameter': 'md_shipto_cust_group'
            },
            'wh_schedule': {
                'file_name': 'wh_schedule',
                'front_name': 'WH Schedule',
                'parameter': 'wh_schedule'
            },
            'cost_pasting_copaking': {
                'file_name': 'cost_pasting_copaking',
                'front_name': 'Pasting, copaking',
                'parameter': 'cost_pasting_copaking'
            },
            'client_requirements': {
                'file_name': 'client_requirements',
                'front_name': 'Client Requirements',
                'parameter': 'client_requirements'
            },

        }

    class Tetris:
        url_path_md = 'master-data'
        url_path_sourcing = 'sourcing-logistics'
        url_path_industry = 'industry'
        url_path_optimilk = 'optimilk'
        type_scenarios = 'tetris-scenarios'

        TYPES_MD = {
            'alt_names_locations': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'AlternativeLocations',
                'front_name': 'Alternative Names Locations',
                'parameter': 'alt_names_locations'
            },
            'alt_names_materials': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'AlternativeMaterials',
                'front_name': 'Alternative Names Materials',
                'parameter': 'alt_names_materials'
            },
            'alt_names_products': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'AlternativeProducts',
                'front_name': 'Alternative Names Products',
                'parameter': 'alt_names_products'
            },
            'alt_names_vendors': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'AlternativeVendors',
                'front_name': 'Alternative Names Vendors',
                'parameter': 'alt_names_vendors'
            },
            'calendars': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'Calendars',
                'front_name': 'Calendars',
                'parameter': 'calendars'
            },
            'locations': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'Locations',
                'front_name': 'Locations',
                'parameter': 'locations'
            },
            'material_groups': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'MaterialGroups',
                'front_name': 'Material Groups',
                'parameter': 'material_groups'
            },
            'materials': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'Materials',
                'front_name': 'Materials',
                'parameter': 'materials'
            },
            'products': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'Products',
                'front_name': 'Products',
                'parameter': 'products'
            },
            'vendors': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'VendorsBuyers',
                'front_name': 'Vendors',
                'parameter': 'vendors'
            },
            'uom': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_md,
                'file_name': 'UOM',
                'front_name': 'UOM',
                'parameter': 'uom'
            }
        }

        TYPES_SOURCING = {
            'demand': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'OP(Demand)',
                'front_name': 'Demand',
                'parameter': 'demand'
            },
            'premade_volumes': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'Premade',
                'front_name': 'Premade Volumes',
                'parameter': 'premade_volumes'
            },
            'product_terms': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'Product Terms',
                'front_name': 'Product Terms',
                'parameter': 'product_terms'
            },
            'rejections': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'Rejects',
                'front_name': 'Rejections',
                'parameter': 'rejections'
            },
            't1_adjustments': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'T1 Adjustments',
                'front_name': 'T1 Adjustments',
                'parameter': 't1_adjustments'
            },
            't1_legs': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'T1 Legs',
                'front_name': 'T1 Legs',
                'parameter': 't1_legs'
            },
            't1_scheme': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'Транспортная схема',
                'front_name': 'T1 Scheme',
                'parameter': 't1_scheme'
            },
            'trade_terms': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'Trade Terms',
                'front_name': 'Trade Terms',
                'parameter': 'trade_terms'
            },
            'sourcing_scheme': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'BP19DCPlant(сорсинг матрица)',
                'front_name': 'Sourcing Scheme',
                'parameter': 'sourcing_scheme'
            },
            'sourcing_settings': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_sourcing,
                'file_name': 'Settings',
                'front_name': 'Sourcing Settings',
                'parameter': 'sourcing_settings'
            }
        }

        TYPES_INDUSTRY = {
            'bom': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_industry,
                'file_name': 'BOM',
                'front_name': 'BOM',
                'parameter': 'bom'
            },
            'bom_replacements': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_industry,
                'file_name': 'BOMSubstitutions',
                'front_name': 'BOM Replacements',
                'parameter': 'bom_replacements'
            },
            'line_capacity': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_industry,
                'file_name': 'LineCapacity',
                'front_name': 'Line Capacity',
                'parameter': 'line_capacity'
            },
            'material_contents': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_industry,
                'file_name': 'MaterialContents',
                'front_name': 'Material Contents',
                'parameter': 'material_contents'
            },
            'min_batches': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_industry,
                'file_name': 'MinBatches',
                'front_name': 'Min-batches',
                'parameter': 'min_batches'
            },
            'mr_adjustments': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_industry,
                'file_name': 'MRAdjustments',
                'front_name': 'MR Adjustments',
                'parameter': 'mr_adjustments'
            },
            'line_bindings': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_industry,
                'file_name': 'PlantLineSKU',
                'front_name': 'Line Bindings',
                'parameter': 'line_bindings'
            }
        }

        TYPES_OPTIMILK = {
            'separation': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'BomSeparation',
                'front_name': 'Separation',
                'parameter': 'separation'
            },
            'regular_supplies': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'Commitments_M',
                'front_name': 'Regular Supplies',
                'parameter': 'regular_supplies'
            },
            'derivation_material': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'DerivationMaterial',
                'front_name': 'Material Stocks',
                'parameter': 'derivation_material'
            },
            'co_packers': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'DisposalsCopacker',
                'front_name': 'Co-Packers',
                'parameter': 'co_packers'
            },
            'stop_buyers': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'DisposalsSpot',
                'front_name': 'Stop Buyers',
                'parameter': 'stop_buyers'
            },
            'inbound_capacity': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'InboundCapacities',
                'front_name': 'Inbound Capacity',
                'parameter': 'inbound_capacity'
            },
            'mb_adjustments': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'MBAdjustments',
                'front_name': 'MB Adjustments',
                'parameter': 'mb_adjustments'
            },
            'new_farms': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'NewFarms_M',
                'front_name': 'New Farms',
                'parameter': 'new_farms'
            },
            'outbound_capacity': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'OutboundCapacities',
                'front_name': 'Outbound Capacity',
                'parameter': 'outbound_capacity'
            },
            'reco_material': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'RecoMaterial',
                'front_name': 'Recomb/Recon',
                'parameter': 'reco_material'
            },
            'shortage': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'Shortage',
                'front_name': 'Shortage',
                'parameter': 'shortage'
            },
            'spot_supplies': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'Spot_M',
                'front_name': 'Spot Supplies',
                'parameter': 'spot_supplies'
            },
            'material_stocks': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'Stock',
                'front_name': 'Material Stocks',
                'parameter': 'material_stocks'
            },
            'ts_farm_to_buyer': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'TSFarmToBuyer',
                'front_name': 'Transport Scheme farm-to-buyer',
                'parameter': 'ts_farm_to_buyer'
            },
            'ts_farm_to_plant': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'TSFarmToPlant',
                'front_name': 'Transport Scheme farm-to-plant',
                'parameter': 'ts_farm_to_plant'
            },
            'ts_plant_to_buyer': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'TSPlantToBuyer',
                'front_name': 'Transport Scheme plant-to-buyer',
                'parameter': 'ts_plant_to_buyer'
            },
            'ts_plant_to_plant': {
                'type_scenarios': type_scenarios,
                'url_path': url_path_optimilk,
                'file_name': 'TSPlantToPlant',
                'front_name': 'Transport Scheme plant-to-plant',
                'parameter': 'ts_plant_to_plant'
            }
        }

    class CFR:
        type_scenarios = 'cfr-scenarios'

        OBLIGATORY_TYPES = {
            'safety_days': {
                'type_scenarios': type_scenarios,
                'file_name': 'safety_days',
                'front_name': 'Safety days',
                'parameter': 'safety_days'
            },
            'coef': {
                'type_scenarios': type_scenarios,
                'file_name': 'coef',
                'front_name': 'Coef',
                'parameter': 'coef'
            },
            'routes': {
                'type_scenarios': type_scenarios,
                'file_name': 'routes',
                'front_name': 'Routes',
                'parameter': 'routes'
            },
            'moq': {
                'type_scenarios': type_scenarios,
                'file_name': 'moq',
                'front_name': 'Moq',
                'parameter': 'moq'
            },
            'fc': {
                'type_scenarios': type_scenarios,
                'file_name': 'fc',
                'front_name': 'FC',
                'parameter': 'fc'
            },
            'fact': {
                'type_scenarios': type_scenarios,
                'file_name': 'fact',
                'front_name': 'Fact',
                'parameter': 'fact'
            },
            'quarantine': {
                'type_scenarios': type_scenarios,
                'file_name': 'quarantine',
                'front_name': 'Quarantine',
                'parameter': 'quarantine'
            },
            'step_table': {
                'type_scenarios': type_scenarios,
                'file_name': 'step_table',
                'front_name': 'Step table',
                'parameter': 'step_table'
            },
            'dlc': {
                'type_scenarios': type_scenarios,
                'file_name': 'dlc',
                'front_name': 'DLC',
                'parameter': 'dlc'
            },
            'shipment_freq': {
                'type_scenarios': type_scenarios,
                'file_name': 'shipment_freq',
                'front_name': 'Shipment freq',
                'parameter': 'shipment_freq'
            },
            'costs': {
                'type_scenarios': type_scenarios,
                'file_name': 'costs',
                'front_name': 'Costs',
                'parameter': 'costs'
            },
            'frozen_horizon': {
                'type_scenarios': type_scenarios,
                'file_name': 'frozen_horizon',
                'front_name': 'Frozen horizon',
                'parameter': 'frozen_horizon'
            },
            'hubbing_days': {
                'type_scenarios': type_scenarios,
                'file_name': 'hubbing_days',
                'front_name': 'Hubbing days',
                'parameter': 'hubbing_days'
            },
            'md_locations': {
                'type_scenarios': type_scenarios,
                'file_name': 'md_locations',
                'front_name': 'Md locations',
                'parameter': 'md_locations'
            },
            'uom': {
                'type_scenarios': type_scenarios,
                'file_name': 'uom',
                'front_name': 'UOM',
                'parameter': 'uom'
            }
        }

        NOT_OBLIGATORY_TYPES = {
            'min_cfr_max_pped': {
                'type_scenarios': type_scenarios,
                'file_name': 'min_cfr_max_pped',
                'front_name': 'Min CFR/Max PPED',
                'parameter': 'min_cfr_max_pped'
            },
            'delta_fa_bias': {
                'type_scenarios': type_scenarios,
                'file_name': 'delta_fa_bias',
                'front_name': 'Delta FA bias',
                'parameter': 'delta_fa_bias'
            }
        }



