from datetime import date, time


from project_data.main_data import ProjectType


class Spreadsheets:
    __GOOGLE_EXPORT_URL = 'https://docs.google.com/uc?export=download&confirm=1'

    __spreadsheet_id = {
        ProjectType.PROMO: {
            'validation_rules': {
                'id': '1uYnl-r1F9AIMgAE4PNJSBXVmgvhcnu8PNcjWArUMYSI',
                'params': {
                    'worksheet_name': 'update',
                    'skip_footer_rows': 0
                }
            },
            'preview_rules': None
        },
        ProjectType.RTM: {
            'validation_rules': {
                'id': '14LQ_3TwsgQ8K69AEBR5IcnbCXxJHUqSj',
                'params': {
                    'worksheet_name': 'Sheet1',
                    'skip_footer_rows': 0
                }
            },
            'preview_rules': None
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
            'validation_rules': {
                'id': '1szjepPIIj3qt2B5aLqncG2yegI50-_t2',
                'params': {
                    'worksheet_name': 'cfr_check_data',
                    'skip_footer_rows': 0
                }
            },
            'preview_rules': None
        }
    }

    @classmethod
    def get(cls, optimizer_type: str, type_id: str):
        return cls.__GOOGLE_EXPORT_URL, cls.__spreadsheet_id[optimizer_type].get(type_id)


class ValidateRules:
    __rules = {
        ProjectType.PROMO: {
            'col_names': {
                'system_file_name': 'Source',
                'col': 'Column name',
                'data_type': 'Type',
                'negativity': 'Negative**',
                'obligatory': 'NaN(default value)*',
                'key': 'key'
            },
            'data_type': {'VARCHAR': 'str', 'DECIMAL': 'float', 'INT': 'int', 'DATE': 'date'},
            'negativity': {'': True, 'FALSE': False, 'False': False},
            'obligatory': {'FALSE': True, 'TRUE': False, 'False': True},
            'key': {'': None, '1': 1}
        },
        ProjectType.RTM: {
            'col_names': {
                'system_file_name': 'Source',
                'col': 'Column name',
                'data_type': 'Type',
                'negativity': 'Negative**',
                'obligatory': 'NaN(default value)*',
                'key': 'Key'
            },
            'data_type': {'VARCHAR': 'str', 'STR': 'str', 'DECIMAL': 'float', 'INT': 'int', 'DATE': 'date', 'TIME': 'time'},
            'negativity': {'': True, 'True': True, 'FALSE': False, 'False': False},
            'obligatory': {'TRUE': False, 'True': False, 'FALSE': True, 'False': True},
            'key': {'': None, '1': 1}
        },
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
            'data_type': {'str': 'str', 'float': 'float', 'int': 'int'},
            'negativity': {'': True, '+': False},
            'obligatory': {'': False, '+': True},
            'key': {'': None, '1': 1},
            'only_for_download_and_preview': {'': None, '1': True}
        },
        ProjectType.CFR: {
            'col_names': {
                'system_file_name': 'Source',
                'col': 'Column name',
                'data_type': 'Type',
                'negativity': 'Negative**',
                'obligatory': 'NaN(default value)*',
                'key': 'Key'
            },
            'data_type': {'VARCHAR': 'str', 'DECIMAL': 'float', 'INT': 'int', 'DATE': 'date', 'TIME': 'time'},
            'negativity': {'': True, 'True': True, 'FALSE': False, 'False': False},
            'obligatory': {'TRUE': False, 'True': False, 'FALSE': True, 'False': True},
            'key': {'': None, '1': 1}
        }
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__rules[optimizer_type]


class PreviewRules:
    __rules = {
        ProjectType.PROMO: None,
        ProjectType.RTM: None,
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
        ProjectType.CFR: None
    }

    @classmethod
    def get(cls, optimizer_type: str):
        return cls.__rules[optimizer_type]
