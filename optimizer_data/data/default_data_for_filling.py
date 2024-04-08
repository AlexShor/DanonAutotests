from datetime import date


class DefaultDataFill:
    @staticmethod
    def get(data_type, validity=True):
        types = {
            True: {
                str: 'string',
                date: '01-01-2023',
                float: '111.45',
                int: '222',
                bool: '1|TRUE:0|FALSE'
            },
            False: {
                str: '555',
                date: 'date',
                float: 'float',
                int: 'int',
                bool: '888'
            }
        }

        return types.get(validity).get(data_type)


class ErrorLogText:
    @staticmethod
    def get(language: str = 'eng'):

        log_text = {
            'rus': {
                'obligation': 'Ошибки касающийся обязательных полей:',
                'type': 'Ошибки по типам полей:',
                'negative': 'Ошибки по неотрицательным значениям:',
                'row': 'строка',
                'col': 'колонка'
            },
            'eng': {
                'obligation': 'Errors regarding obligatory fields:',
                'type': 'Type errors:',
                'negative': 'Errors with non-negative values:',
                'row': 'row',
                'col': 'column'
            }
        }

        return log_text[language]
