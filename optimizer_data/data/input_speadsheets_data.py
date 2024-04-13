from project_data.main_data import ProjectType


class Spreadsheets:
    __GOOGLE_EXPORT_URL = 'https://docs.google.com/uc?export=download&confirm=1'

    __spreadsheet_id = {
        ProjectType.PROMO: {
            'validation_rules': '1uYnl-r1F9AIMgAE4PNJSBXVmgvhcnu8PNcjWArUMYSI',
            'inputs': '1fn4PxFE6bbyOTe0aPRUpYhEVC9uTDslF'
        },
        ProjectType.RTM: {
            'validation_rules': '1mtOKERdwfvMzt9BYuv5hFiiSBV7JZGRqXS-XQSdjo70',
            'inputs': '1L9juBdFeFfuP0k2gr9P-S1QQYEf4SHBw'
        },
        ProjectType.TETRIS: {
            'validation_rules': {
                'id': '1i2Z1yXfFoqofzOp467YZG0_rVrtmo5G4',
                'params': {
                    'worksheet_name': 'Validation rules',
                    'skip_footer_rows': 291
                }
            },
            'preview_rules': {
                'id': '1bp9O6oAG5jXWJyegybjkbTVZHZHAoQVa',
                'params': {
                    'worksheet_name': 'Правила отображения в preview',
                    'skip_footer_rows': 0
                }
            },
            'inputs': ''
        },
        ProjectType.CFR: {
            'validation_rules': '14irOmFBvcSye3_yg9VkA51Ku_vw93yjaky8_LVo2pe8',
            'inputs': '1RlZwjrDmh0xecyDm9RrA0qXPI66k532f'
        }
    }

    @classmethod
    def get(cls, optimizer_type: str, type_id: str):
        return cls.__GOOGLE_EXPORT_URL, cls.__spreadsheet_id[optimizer_type][type_id]


class ValidateRules:
    __rules = {
        ProjectType.PROMO: {},
        ProjectType.RTM: {},
        ProjectType.TETRIS: {
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
        ProjectType.CFR: {}
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__rules[optimizer_type]


class PreviewRules:
    __rules = {
        ProjectType.PROMO: {},
        ProjectType.RTM: {},
        ProjectType.TETRIS: {
            'col_names': {
                'col': 'Название столбца',
                'data_type': 'Тип данных',
                'decimal_places': 'Знаков после запятой',
                'percentage': 'Процентный формат с 2 знаками после запятой (пример 3,80%)',
                'separator': 'Разделитель тысяч',
            },
            'data_type': {'str': 'str', 'float': 'float', 'int': 'int'},
            'percentage': {'No': False, 'Yes': True},
            'separator': {'No': False, 'Yes': True}
        },
        ProjectType.CFR: {}
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__rules[optimizer_type]
