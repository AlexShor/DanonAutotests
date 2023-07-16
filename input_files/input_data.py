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


class FillData(DataTypes):
    @staticmethod
    def get_value(data_type, validity=True):
        types = {True: {DataTypes.VARCHAR: 'varchar',
                        DataTypes.DATE: '01-01-2023',
                        DataTypes.DECIMAL: '111.45',
                        DataTypes.INT: '222'},
                 False: {DataTypes.VARCHAR: '555',
                         DataTypes.DATE: 'date',
                         DataTypes.DECIMAL: 'decimal',
                         DataTypes.INT: 'int'}}
        return types.get(validity).get(data_type)


class InputNameMatch:
    PROMO = {'GPS': 'gps',
             'Distribution Mapping': 'distr_mapping',
             'Combine Products': 'combine_products',
             'Combine Chains': 'combine_chains',
             'Up/Down Size': 'up_down_size',
             'Product Masterdata': 'prod_md',
             'Customer Masterdata': 'cust_md',
             'Promo Library': 'lib'}
