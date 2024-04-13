from operator import itemgetter

from pages.site_data.default_params import ProjectType as Ptype


class ScenarioTypes:
    TYPE = {Ptype.PROMO: 'promo-scenarios',
            Ptype.RTM: 'rtm-scenarios',
            Ptype.TETRIS_NEW: 'tetris-scenarios',
            Ptype.CFR: 'cfr-scenarios'}


class OptimizationTypes:
    TYPE = {
        Ptype.PROMO: None,
        Ptype.RTM: {
            'optimizer': 'RTM Optimizer',
            'cts': 'RTM CtS',
        },
        Ptype.TETRIS_NEW: {
            'sourcing': 'sourcing',
            'milk': 'milk',
        },
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
            'drivers_break_old': {
                'scenario_type': scenario_type,
                'system_file_name': 'drivers_break_old',
                'front_name': 'Drivers break (old)',
                'parameter': 'drivers_break_old',
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
            'deliveries_for_wms': {
                'scenario_type': scenario_type,
                'system_file_name': 'deliveries_for_wms',
                'front_name': 'Deliveries for WMS',
                'parameter': 'deliveries_for_wms',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'wms_delivery': {
                'scenario_type': scenario_type,
                'system_file_name': 'wms_delivery',
                'front_name': 'WMS delivery',
                'parameter': 'wms_delivery',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'wms_support': {
                'scenario_type': scenario_type,
                'system_file_name': 'wms_support',
                'front_name': 'WMS support',
                'parameter': 'wms_support',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'xd_fact_volumes': {
                'scenario_type': scenario_type,
                'system_file_name': 'xd_fact_volumes',
                'front_name': 'XD Fact volumes',
                'parameter': 'xd_fact_volumes',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer')(opti_type)
            },
            'wh_cost_split_rule': {
                'scenario_type': scenario_type,
                'system_file_name': 'wh_cost_split_rule',
                'front_name': 'Cost Split Cost WH',
                'parameter': 'wh_cost_split_rule',
                'url_path': None,
                'obligatory': True,
                'optimization_type': itemgetter('optimizer', 'cts')(opti_type)
            },
        }

        N_TYPES = {
            'md_shipto_cust_group': {
                'scenario_type': scenario_type,
                'system_file_name': 'md_shipto_cust_group',
                'front_name': 'MD ShipTo Customer Group',
                'parameter': 'md_shipto_cust_group',
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
            'wh_schedule': {
                'scenario_type': scenario_type,
                'system_file_name': 'wh_schedule',
                'front_name': 'WH Schedule',
                'parameter': 'wh_schedule',
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
            }
        }

    class Tetris:
        scenario_type = ScenarioTypes.TYPE[Ptype.TETRIS_NEW]

        TYPES = {
            'calendars': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Calendars',
                'front_name': 'Календари',
                'parameter': 'calendars',
                'obligatory': False,
                'upload_queue': 1,
                'calculation_block': ['sourcing', 'industry', 'milk']
            },
            'parameters': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Parameters',
                'front_name': 'Параметры',
                'parameter': 'parameters',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing', 'industry', 'milk']
            },
            'plants': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Plants',
                'front_name': 'Заводы',
                'parameter': 'plants',
                'obligatory': False,
                'upload_queue': 1,
                'calculation_block': ['sourcing', 'industry', 'milk']
            },
            'products': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Products',
                'front_name': 'Продукты',
                'parameter': 'products',
                'obligatory': False,
                'upload_queue': 1,
                'calculation_block': ['sourcing']
            },
            'innovations': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Innovations',
                'front_name': 'Инновации',
                'parameter': 'innovations',
                'obligatory': False,
                'upload_queue': 1,
                'calculation_block': ['sourcing']
            },
            'uoms': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Uoms',
                'front_name': 'Единицы измерения',
                'parameter': 'uoms',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing']
            },
            'warehouses': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Warehouses',
                'front_name': 'Склады',
                'parameter': 'warehouses',
                'obligatory': False,
                'upload_queue': 1,
                'calculation_block': ['sourcing']
            },
            'demand': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Demand',
                'front_name': 'План продаж',
                'parameter': 'demand',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing']
            },
            'sourcing_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Sourcing Scheme',
                'front_name': 'План распределения',
                'parameter': 'sourcing_scheme',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing']
            },
            'deliveries': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Deliveries',
                'front_name': 'Схема доставки',
                'parameter': 'deliveries',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing']
            },
            'itineraries': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Itineraries',
                'front_name': 'Маршруты',
                'parameter': 'itineraries',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing']
            },
            'shipments': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Shipments',
                'front_name': 'Мастер данные Т1',
                'parameter': 'shipments',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing']
            },
            'premade_volumes': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Premade Volumes',
                'front_name': 'Дополнительные объемы',
                'parameter': 'premade_volumes',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing', 'industry']
            },
            'rejections': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Rejections',
                'front_name': 'Альтернативные источники',
                'parameter': 'rejections',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing', 'industry']
            },
            'demand_options': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Demand Options',
                'front_name': 'Настройки плана продаж',
                'parameter': 'demand_options',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['sourcing']
            },
            'min_batches': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Min-batches',
                'front_name': 'Минимальные партии',
                'parameter': 'min_batches',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'industrial_costs': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Industrial Costs',
                'front_name': 'Индустриальные затраты',
                'parameter': 'industrial_costs',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'line_capacities': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Line Capacities',
                'front_name': 'Мощности линий',
                'parameter': 'line_capacities',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'line_priorities': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Line Priorities',
                'front_name': 'Приоритеты линий',
                'parameter': 'line_priorities',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'mr_adjustments': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'MR Adjustments',
                'front_name': 'Корректировки ПП',
                'parameter': 'mr_adjustments',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'line_bindings': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Line Bindings',
                'front_name': 'Завод-линия-скю',
                'parameter': 'line_bindings',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'material_contents': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Material Contents',
                'front_name': 'Характеристики материалов',
                'parameter': 'material_contents',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'base_formulas': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Base Formulas',
                'front_name': 'Базовые рецепты',
                'parameter': 'base_formulas',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'reco_formulas': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Reco Formulas',
                'front_name': 'Рецепты восстановления',
                'parameter': 'reco_formulas',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['industry']
            },
            'materials': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Materials',
                'front_name': 'Материалы',
                'parameter': 'materials',
                'obligatory': False,
                'upload_queue': 1,
                'calculation_block': ['industry', 'milk']
            },
            'material_groups': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Material Groups',
                'front_name': 'Группы материалов',
                'parameter': 'material_groups',
                'obligatory': False,
                'upload_queue': 2,
                'calculation_block': ['milk']
            },
            'table_parameters': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Table Parameters',
                'front_name': 'Табличные параметры',
                'parameter': 'table_parameters',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'contracts': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Contracts',
                'front_name': 'Контракты поставщиков',
                'parameter': 'contracts',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'supply_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Supply Scheme',
                'front_name': 'ТЗР ферма-завод',
                'parameter': 'supply_scheme',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'farm_sales_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Farm Sales Scheme',
                'front_name': 'ТЗР ферма-покупатель',
                'parameter': 'farm_sales_scheme',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'plant_sales_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Plant Sales Scheme',
                'front_name': 'ТЗР завод-покупатель',
                'parameter': 'plant_sales_scheme',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'movement_scheme': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Movement Scheme',
                'front_name': 'ТЗР завод-завод',
                'parameter': 'movement_scheme',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'buyers_contracts': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Buyers contracts',
                'front_name': 'Контракты покупателей',
                'parameter': 'buyers_contracts',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'reco_capabilities': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Reco Capabilities',
                'front_name': 'Возможности восстановления',
                'parameter': 'reco_capabilities',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'derivation': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Derivation',
                'front_name': 'Производство ингридиентов',
                'parameter': 'derivation',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'mb_adjustments': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'MB Adjustments',
                'front_name': 'Корректировки МБ',
                'parameter': 'mb_adjustments',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'separation': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Separation',
                'front_name': 'Сепарация',
                'parameter': 'separation',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'inbound_capacity': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Inbound Capacity',
                'front_name': 'Возможности приемки',
                'parameter': 'inbound_capacity',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'outbound_capacity': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Outbound Capacity',
                'front_name': 'Возможности отгрузки',
                'parameter': 'outbound_capacity',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            },
            'stock_bounds': {
                'scenario_type': scenario_type,
                'url_path': None,
                'system_file_name': 'Stock Bounds',
                'front_name': 'Уровни стоков ЖС',
                'parameter': 'stock_bounds',
                'obligatory': False,
                'upload_queue': 3,
                'calculation_block': ['milk']
            }
        }

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
            # 'delta_fa_bias': {
            #     'scenario_type': scenario_type,
            #     'system_file_name': 'delta_fa_bias',
            #     'front_name': 'Delta FA bias',
            #     'parameter': 'delta_fa_bias',
            #     'url_path': None,
            #     'obligatory': True,
            #     'optimization_type': itemgetter('demand_randomizer')(opti_type['rnd_mode'])
            # },
            'filters': {
                'scenario_type': scenario_type,
                'system_file_name': 'filters',
                'front_name': 'Filters',
                'parameter': 'filters',
                'url_path': None,
                'obligatory': False,
                'optimization_type': all_opti_type
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
            # 'frozen_horizon': {
            #     'scenario_type': scenario_type,
            #     'system_file_name': 'frozen_horizon',
            #     'front_name': 'Frozen horizon',
            #     'parameter': 'frozen_horizon',
            #     'url_path': None,
            #     'obligatory': False,
            #     'optimization_type': all_opti_type
            # },
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
