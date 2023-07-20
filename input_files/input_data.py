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
    class Promo:
        OBLIGATION = 'Errors regarding obligatory fields:'
        TYPE = 'Type errors:'
        NEGATIVE = 'Errors with non-negative values:'
        ROW = 'row'
        COLUMN = 'column'

    class Rtm:
        OBLIGATION = 'Errors regarding obligatory fields:'
        TYPE = 'Type errors:'
        NEGATIVE = 'Errors with non-negative values:'
        ROW = 'row'
        COLUMN = 'column'

    class Tetris:
        OBLIGATION = 'Ошибки касающийся обязательных полей:'
        TYPE = 'Ошибки по типам полей:'
        NEGATIVE = 'Ошибки по неотрицательным значениям:'
        ROW = 'строка'
        COLUMN = 'колонка'


class InputNameMatch:
    PROMO = {'GPS': 'gps',
             'Distribution Mapping': 'distr_mapping',
             'Combine Products': 'combine_products',
             'Combine Chains': 'combine_chains',
             'Up/Down Size': 'up_down_size',
             'Product Masterdata': 'prod_md',
             'Customer Masterdata': 'cust_md',
             'Promo Library': 'lib'}


class InputTypeNameMatch:
    class Tetris:
        input_type_md = ['md', 'master-data']
        input_type_sourcing = ['sourcing', 'sourcing-logistics']
        input_type_industry = ['industry', 'industry']
        input_type_optimilk = ['milkbalance', 'optimilk']

        TYPES = [
            [*input_type_md, 'alt_names_locations', 'AlternativeLocations'],
            [*input_type_md, 'alt_names_materials', 'AlternativeMaterials'],
            [*input_type_md, 'alt_names_products', 'AlternativeProducts'],
            [*input_type_md, 'alt_names_vendors', 'AlternativeVendors'],
            [*input_type_md, 'calendars', 'Calendars'],
            [*input_type_md, 'locations', 'Locations'],
            [*input_type_md, 'material_groups', 'MaterialGroups'],
            [*input_type_md, 'materials', 'Materials'],
            [*input_type_md, 'products', 'Products'],
            [*input_type_md, 'vendors', 'VendorsBuyers'],
            [*input_type_sourcing, 'demand', 'OP(Demand)'],
            [*input_type_sourcing, 'premade_volumes', 'Premade'],
            [*input_type_sourcing, 'product_terms', 'Product Terms'],
            [*input_type_sourcing, 'rejections', 'Rejects'],
            [*input_type_sourcing, 't1_adjustments', 'T1 Adjustments'],
            [*input_type_sourcing, 't1_legs', 'T1 Legs'],
            [*input_type_sourcing, 't1_scheme', 'Транспортная схема'],
            [*input_type_sourcing, 'trade_terms', 'Trade Terms'],
            [*input_type_sourcing, 'sourcing_scheme', 'BP19DCPlant(сорсинг матрица)'],
            [*input_type_sourcing, 'sourcing_settings', 'Settings'],
            [*input_type_industry, 'bom', 'BOM'],
            [*input_type_industry, 'bom_replacements', 'BOMSubstitutions'],
            [*input_type_industry, 'line_capacity', 'LineCapacity'],
            [*input_type_industry, 'material_contents', 'MaterialContents'],
            [*input_type_industry, 'min_batches', 'MinBatches'],
            [*input_type_industry, 'mr_adjustments', 'MRAdjustments'],
            [*input_type_industry, 'line_bindings', 'PlantLineSKU'],
            [*input_type_optimilk, 'separation', 'BomSeparation'],
            [*input_type_optimilk, 'regular_supplies', 'Commitments_M'],
            [*input_type_optimilk, 'derivation_material', 'DerivationMaterial'],
            [*input_type_optimilk, 'co_packers', 'DisposalsCopacker'],
            [*input_type_optimilk, 'stop_buyers', 'DisposalsSpot'],
            [*input_type_optimilk, 'inbound_capacity', 'InboundCapacities'],
            [*input_type_optimilk, 'mb_adjustments', 'MBAdjustments'],
            [*input_type_optimilk, 'new_farms', 'NewFarms_M'],
            [*input_type_optimilk, 'outbound_capacity', 'OutboundCapacities'],
            [*input_type_optimilk, 'reco_material', 'RecoMaterial'],
            [*input_type_optimilk, 'shortage', 'Shortage'],
            [*input_type_optimilk, 'spot_supplies', 'Spot_M'],
            [*input_type_optimilk, 'material_stocks', 'Stock'],
            [*input_type_optimilk, 'ts_farm_to_buyer', 'TSFarmToBuyer'],
            [*input_type_optimilk, 'ts_farm_to_plant', 'TSFarmToPlant'],
            [*input_type_optimilk, 'ts_plant_to_buyer', 'TSPlantToBuyer'],
            [*input_type_optimilk, 'ts_plant_to_plant', 'TSPlantToPlant']]
