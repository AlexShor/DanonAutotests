class CheckInputUrls:
    PROMO = 'https://docs.google.com/spreadsheets/d/1uYnl-r1F9AIMgAE4PNJSBXVmgvhcnu8PNcjWArUMYSI/edit?usp=sharing'


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
