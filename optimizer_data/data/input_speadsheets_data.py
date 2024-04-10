class Spreadsheets:
    GOOGLE_EXPORT_URL = 'https://docs.google.com/uc?export=download&confirm=1'

    class Promo:
        CHECK_INPUT_ID = f'1uYnl-r1F9AIMgAE4PNJSBXVmgvhcnu8PNcjWArUMYSI'
        INPUT_PROMO_ID = f'1fn4PxFE6bbyOTe0aPRUpYhEVC9uTDslF'

    class RTM:
        CHECK_INPUT_ID = f'1mtOKERdwfvMzt9BYuv5hFiiSBV7JZGRqXS-XQSdjo70'
        INPUT_RTM_ID = f'1L9juBdFeFfuP0k2gr9P-S1QQYEf4SHBw'

    class Tetris:
        CHECK_INPUT_ID = f'1i2Z1yXfFoqofzOp467YZG0_rVrtmo5G4'
        INPUT_MILK_ID = f'1WMJuYwMva13dKtmRWw2g4EXckbdYImgr'
        INPUT_SOURCING_ID = f'15zY1rJFOlmnwTXH9ZLfH4ZaBfX1xsUI4'

    class CFR:
        CHECK_INPUT_ID = f'14irOmFBvcSye3_yg9VkA51Ku_vw93yjaky8_LVo2pe8' + '/'
        INPUT_CFR_ID = f'1RlZwjrDmh0xecyDm9RrA0qXPI66k532f' + '/'


# class ValidateRules:
#     class Promo:
#         pass
#
#     class RTM:
#         pass
#
#     class Tetris:
#         _valid_rules_col_names = {'system_file_name': 'Файл',
#                                   'col': 'Столбцы',
#                                   'data_type': 'Тип данных',
#                                   'negativity': 'Значение>=0',
#                                   'obligatory': 'Отсутствие пустых полей'}
#
#         _valid_rules_data_type = {'str': str, 'float': float, 'int': int}
#         _valid_rules_negativity = {'': True, '+': False}
#         _valid_rules_obligatory = {'': False, '+': True}
#
#         VALID_RULES = {'col_names': _valid_rules_col_names,
#                        'data_type': _valid_rules_data_type,
#                        'negativity': _valid_rules_negativity,
#                        'obligatory': _valid_rules_obligatory}
#
#     class CFR:
#         pass


class ValidateRules:
    __rules = {
        'promo': {},
        'rtm': {},
        'tetris': {
            'file_params': {
                'worksheet_name': 'Validation rules',
                'skip_footer_rows': 291
            },
            'col_names': {
                'system_file_name': 'Файл',
                'col': 'Столбцы',
                'data_type': 'Тип данных',
                'negativity': 'Значение>=0',
                'obligatory': 'Отсутствие пустых полей',
                'key': 'Ключ',
                'validation': 'Валидация',
                'only_for_download_and_preview': 'Только для выгрзуки и превью (нет в input)',
                'auto_mapping': 'Автоматический маппинг из источника для выгрузки'
            },
            'data_type': {'str': str, 'float': float, 'int': int},
            'negativity': {'': True, '+': False},
            'obligatory': {'': False, '+': True},
            'key': {'': None, '1': 1},
            'only_for_download_and_preview': {'': None, '1': True}
        },
        'cfr': {}
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__rules[optimizer_type]
