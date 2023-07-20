google_sheets_url = 'https://docs.google.com/spreadsheets/d/'


class Spreadsheets:
    class Promo:
        CHECK_INPUT = f'{google_sheets_url}1uYnl-r1F9AIMgAE4PNJSBXVmgvhcnu8PNcjWArUMYSI' + '/'
        INPUT_PROMO = f'{google_sheets_url}1fn4PxFE6bbyOTe0aPRUpYhEVC9uTDslF' + '/'

    class RTM:
        CHECK_INPUT = f'{google_sheets_url}1VYYQiF7ftxTdFj40cw1aPS_nTAvSBFWq' + '/'
        INPUT_RTM = f'{google_sheets_url}1gKS4J3tPOn1y-s9t5W5Mnf-SChoGTbJJ' + '/'

    class Tetris:
        CHECK_INPUT = f'{google_sheets_url}1YERmUHZL-cEIbWDW3NUGAnU6I8LhZcn-' + '/'
        INPUT_MILK_BALANCE = f'{google_sheets_url}1KleiyYpvy_LxdklVIjBY18NGo2ygB36n' + '/'
        INPUT_MD = f'{google_sheets_url}1YL6eHd61hlxaDdIypljwGtp8BAIDstbQ' + '/'
        INPUT_INDUSTRY = f'{google_sheets_url}1GOyAx82lEWSb5MsdSIgj48CKlX8zxSJ-' + '/'
        INPUT_SOURCING = f'{google_sheets_url}1vz9V5l4bta_UDHa7NpersgI6I5ve3Y_h' + '/'


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


# class InputNameMatch:
#     PROMO = {'GPS': 'gps',
#              'Distribution Mapping': 'distr_mapping',
#              'Combine Products': 'combine_products',
#              'Combine Chains': 'combine_chains',
#              'Up/Down Size': 'up_down_size',
#              'Product Masterdata': 'prod_md',
#              'Customer Masterdata': 'cust_md',
#              'Promo Library': 'lib'}


class InputTypeNameMatch:
    class Promo:
        TYPES = {
            'gps': {
                'url_path': 'promo-gps',
                'file_name': 'gps',
                'front_name': 'GPS'
            },
            'distr_mapping': {
                'url_path': 'promo-distr-mappings',
                'file_name': 'distr_mapping',
                'front_name': 'Distribution Mapping'
            },
            'combine_products': {
                'url_path': 'promo-combine-products',
                'file_name': 'combine_products',
                'front_name': 'Combine Products'
            },
            'combine_chains': {
                'url_path': 'promo-combine-chains',
                'file_name': 'combine_chains',
                'front_name': 'Combine Chains'
            },
            'up_down_size': {
                'url_path': 'promo-up-down-sizes',
                'file_name': 'up_down_size',
                'front_name': 'Up/Down Size'
            },
            'prod_md': {
                'url_path': 'promo-product-mds',
                'file_name': 'prod_md',
                'front_name': 'Product Masterdata'
            },
            'cust_md': {
                'url_path': 'promo-customer-mds',
                'file_name': 'cust_md',
                'front_name': 'Customer Masterdata'
            },
            'lib': {
                'url_path': 'promo-libs',
                'file_name': 'lib',
                'front_name': 'Promo Library'
            }
        }

    class Tetris:
        url_path_md = 'master-data'
        url_path_sourcing = 'sourcing-logistics'
        url_path_industry = 'industry'
        url_path_optimilk = 'optimilk'

        TYPES_MD = {
            'alt_names_locations': {
                'url_path': url_path_md,
                'file_name': 'AlternativeLocations',
                'front_name': '',
                'parameter': 'alt_names_locations'
            },
            'alt_names_materials': {
                'url_path': url_path_md,
                'file_name': 'AlternativeMaterials',
                'front_name': '',
                'parameter': 'alt_names_materials'
            },
            'alt_names_products': {
                'url_path': url_path_md,
                'file_name': 'AlternativeProducts',
                'front_name': '',
                'parameter': 'alt_names_products'
            },
            'alt_names_vendors': {
                'url_path': url_path_md,
                'file_name': 'AlternativeVendors',
                'front_name': '',
                'parameter': 'alt_names_vendors'
            },
            'calendars': {
                'url_path': url_path_md,
                'file_name': 'Calendars',
                'front_name': '',
                'parameter': 'calendars'
            },
            'locations': {
                'url_path': url_path_md,
                'file_name': 'Locations',
                'front_name': '',
                'parameter': 'locations'
            },
            'material_groups': {
                'url_path': url_path_md,
                'file_name': 'MaterialGroups',
                'front_name': '',
                'parameter': 'material_groups'
            },
            'materials': {
                'url_path': url_path_md,
                'file_name': 'Materials',
                'front_name': '',
                'parameter': 'materials'
            },
            'products': {
                'url_path': url_path_md,
                'file_name': 'Products',
                'front_name': '',
                'parameter': 'products'
            },
            'vendors': {
                'url_path': url_path_md,
                'file_name': 'VendorsBuyers',
                'front_name': '',
                'parameter': 'vendors'
            }
        }

        TYPES_SOURCING = {
            'demand': {
                'url_path': url_path_sourcing,
                'file_name': 'OP(Demand)',
                'front_name': '',
                'parameter': 'demand'
            },
            'premade_volumes': {
                'url_path': url_path_sourcing,
                'file_name': 'Premade',
                'front_name': '',
                'parameter': 'premade_volumes'
            },
            'product_terms': {
                'url_path': url_path_sourcing,
                'file_name': 'Product Terms',
                'front_name': '',
                'parameter': 'product_terms'
            },
            'rejections': {
                'url_path': url_path_sourcing,
                'file_name': 'Rejects',
                'front_name': '',
                'parameter': 'rejections'
            },
            't1_adjustments': {
                'url_path': url_path_sourcing,
                'file_name': 'T1 Adjustments',
                'front_name': '',
                'parameter': 't1_adjustments'
            },
            't1_legs': {
                'url_path': url_path_sourcing,
                'file_name': 'T1 Legs',
                'front_name': '',
                'parameter': 't1_legs'
            },
            't1_scheme': {
                'url_path': url_path_sourcing,
                'file_name': 'Транспортная схема',
                'front_name': '',
                'parameter': 't1_scheme'
            },
            'trade_terms': {
                'url_path': url_path_sourcing,
                'file_name': 'Trade Terms',
                'front_name': '',
                'parameter': 'trade_terms'
            },
            'sourcing_scheme': {
                'url_path': url_path_sourcing,
                'file_name': 'BP19DCPlant(сорсинг матрица)',
                'front_name': '',
                'parameter': 'sourcing_scheme'
            },
            'sourcing_settings': {
                'url_path': url_path_sourcing,
                'file_name': 'Settings',
                'front_name': '',
                'parameter': 'sourcing_settings'
            }
        }

        TYPES_INDUSTRY = {
            'bom': {
                'url_path': url_path_industry,
                'file_name': 'BOM',
                'front_name': '',
                'parameter': 'bom'
            },
            'bom_replacements': {
                'url_path': url_path_industry,
                'file_name': 'BOMSubstitutions',
                'front_name': '',
                'parameter': 'bom_replacements'
            },
            'line_capacity': {
                'url_path': url_path_industry,
                'file_name': 'LineCapacity',
                'front_name': '',
                'parameter': 'line_capacity'
            },
            'material_contents': {
                'url_path': url_path_industry,
                'file_name': 'MaterialContents',
                'front_name': '',
                'parameter': 'material_contents'
            },
            'min_batches': {
                'url_path': url_path_industry,
                'file_name': 'MinBatches',
                'front_name': '',
                'parameter': 'min_batches'
            },
            'mr_adjustments': {
                'url_path': url_path_industry,
                'file_name': 'MRAdjustments',
                'front_name': '',
                'parameter': 'mr_adjustments'
            },
            'line_bindings': {
                'url_path': url_path_industry,
                'file_name': 'PlantLineSKU',
                'front_name': '',
                'parameter': 'line_bindings'
            }
        }

        TYPES_OPTIMILK = {
            'separation': {
                'url_path': url_path_optimilk,
                'file_name': 'BomSeparation',
                'front_name': '',
                'parameter': 'separation'
            },
            'regular_supplies': {
                'url_path': url_path_optimilk,
                'file_name': 'Commitments_M',
                'front_name': '',
                'parameter': 'regular_supplies'
            },
            'derivation_material': {
                'url_path': url_path_optimilk,
                'file_name': 'DerivationMaterial',
                'front_name': '',
                'parameter': 'derivation_material'
            },
            'co_packers': {
                'url_path': url_path_optimilk,
                'file_name': 'DisposalsCopacker',
                'front_name': '',
                'parameter': 'co_packers'
            },
            'stop_buyers': {
                'url_path': url_path_optimilk,
                'file_name': 'DisposalsSpot',
                'front_name': '',
                'parameter': 'stop_buyers'
            },
            'inbound_capacity': {
                'url_path': url_path_optimilk,
                'file_name': 'InboundCapacities',
                'front_name': '',
                'parameter': 'inbound_capacity'
            },
            'mb_adjustments': {
                'url_path': url_path_optimilk,
                'file_name': 'MBAdjustments',
                'front_name': '',
                'parameter': 'mb_adjustments'
            },
            'new_farms': {
                'url_path': url_path_optimilk,
                'file_name': 'NewFarms_M',
                'front_name': '',
                'parameter': 'new_farms'
            },
            'outbound_capacity': {
                'url_path': url_path_optimilk,
                'file_name': 'OutboundCapacities',
                'front_name': '',
                'parameter': 'outbound_capacity'
            },
            'reco_material': {
                'url_path': url_path_optimilk,
                'file_name': 'RecoMaterial',
                'front_name': '',
                'parameter': 'reco_material'
            },
            'shortage': {
                'url_path': url_path_optimilk,
                'file_name': 'Shortage',
                'front_name': '',
                'parameter': 'shortage'
            },
            'spot_supplies': {
                'url_path': url_path_optimilk,
                'file_name': 'Spot_M',
                'front_name': '',
                'parameter': 'spot_supplies'
            },
            'material_stocks': {
                'url_path': url_path_optimilk,
                'file_name': 'Stock',
                'front_name': '',
                'parameter': 'material_stocks'
            },
            'ts_farm_to_buyer': {
                'url_path': url_path_optimilk,
                'file_name': 'TSFarmToBuyer',
                'front_name': '',
                'parameter': 'ts_farm_to_buyer'
            },
            'ts_farm_to_plant': {
                'url_path': url_path_optimilk,
                'file_name': 'TSFarmToPlant',
                'front_name': '',
                'parameter': 'ts_farm_to_plant'
            },
            'ts_plant_to_buyer': {
                'url_path': url_path_optimilk,
                'file_name': 'TSPlantToBuyer',
                'front_name': '',
                'parameter': 'ts_plant_to_buyer'
            },
            'ts_plant_to_plant': {
                'url_path': url_path_optimilk,
                'file_name': 'TSPlantToPlant',
                'front_name': '',
                'parameter': 'ts_plant_to_plant'
            }
        }


