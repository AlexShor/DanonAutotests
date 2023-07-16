google_sheets_url = 'https://docs.google.com/spreadsheets/d/'


class Spreadsheets:
    class Promo:
        CHECK_INPUT = f'{google_sheets_url}1Nlmr4xCBhdXUBRx-l8bUjVlL2SkOTZcA9Uo_UVgbcS8' + '/'
        INPUT_PROMO = f'{google_sheets_url}18adE7GVnQPOD_ZL7SnhR6kkup8fshWzrYzbDrcYi2K8' + '/'

    class RTM:
        CHECK_INPUT = f'{google_sheets_url}1eH7CeUgACj3WYSA_xovhiqNsJl9VWVH8DWS-lKTiAHM' + '/'
        INPUT_RTM = f'{google_sheets_url}1zvN0SjpV3OSUu4x1PD-bDwX2jWc4rd0DXc6wkjIQPCw' + '/'

    class Tetris:
        check_input_sp_sheet = '1rF_hqm--YdjBioPpThBmaPpf8efkrge3LLkvu1Mo194' + '/'

        CHECK_INPUT = {'milk_balance': f'{google_sheets_url}{check_input_sp_sheet}/edit#gid=1179607784',
                       'industry': f'{google_sheets_url}{check_input_sp_sheet}/edit#gid=1755984529',
                       'md': f'{google_sheets_url}{check_input_sp_sheet}/edit#gid=276097005',
                       'sourcing': f'{google_sheets_url}{check_input_sp_sheet}/edit#gid=101905169'}
        INPUT_MILK_BALANCE = f'{google_sheets_url}1S3vHAcGubdZfONUaLOE9cba34_TupuIi1Lt-JVe0LWY' + '/'
        INPUT_MD = f'{google_sheets_url}1okMXXYudAmdC237OOHcqL5J42TBd2ljUnCci4axm-Y4' + '/'
        INPUT_INDUSTRY = f'{google_sheets_url}1VVMkc81PHvUV_eaG9iI0VPWepJQS6IYHib72TT2_DvU' + '/'
        INPUT_SOURCING = f'{google_sheets_url}1IoRK54hkNA9y42eN4F9sd69miP5mIigkDv513G-gGX0' + '/'


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
